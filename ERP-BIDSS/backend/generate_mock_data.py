import sys
import random
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Append Odoo path
sys.path.append(r"C:\Program Files\Odoo 18.0.20241229\server")
import odoo

# --- BUSINESS STORY CANON (DO NOT CHANGE) ---
# Baseline is daily base transaction count. We will scale it by the weights below.
MONTH_WEIGHTS = {
    1:  {'so_w': 1.0, 'po_w': 1.0, 'lt': 5},
    2:  {'so_w': 1.08, 'po_w': 1.0, 'lt': 5},
    3:  {'so_w': 0.95, 'po_w': 1.0, 'lt': 10},  # Supplier delay
    4:  {'so_w': 1.0, 'po_w': 1.4, 'lt': 6},    # Panic Buying
    5:  {'so_w': 0.9, 'po_w': 0.8, 'lt': 5},    # Overstock
    6:  {'so_w': 0.9, 'po_w': 0.8, 'lt': 5},
    7:  {'so_w': 0.8, 'po_w': 0.9, 'lt': 5},
    8:  {'so_w': 1.1, 'po_w': 1.0, 'lt': 5},
    9:  {'so_w': 1.0, 'po_w': 1.0, 'lt': 5},
    10: {'so_w': 1.0, 'po_w': 1.0, 'lt': 5},
    11: {'so_w': 1.2, 'po_w': 1.2, 'lt': 5},
    12: {'so_w': 1.1, 'po_w': 1.1, 'lt': 5},
}

YEAR = 2024
BASE_SO_PER_DAY = 5
BASE_PO_PER_DAY = 5

# --- MASTER DATA LISTS ---
CATEGORIES = {
    'Heavy Equipment': {'stock': (2, 15), 'cost': (1500000000, 2500000000), 'margin': 1.3},
    'Major Components': {'stock': (15, 80), 'cost': (15000000, 50000000), 'margin': 1.4},
    'Hydraulic Parts': {'stock': (30, 250), 'cost': (1500000, 15000000), 'margin': 1.5},
    'Engine Components': {'stock': (20, 180), 'cost': (2000000, 20000000), 'margin': 1.45},
    'Consumables': {'stock': (100, 1000), 'cost': (50000, 500000), 'margin': 1.6},
}

BRANDS = ['Komatsu', 'Caterpillar', 'Hitachi', 'Volvo', 'Doosan', 'Kobelco', 'JCB']
HE_TYPES = ['PC200 Excavator', '320GC Excavator', 'ZX210', 'EC210', 'DX225', 'Wheel Loader', 'Bulldozer', 'Motor Grader', 'Dump Truck', 'Forklift', 'Compactor', 'Crane', 'Generator Set', 'Mining Equipment']
PARTS = ['Hydraulic Pump', 'Hydraulic Cylinder', 'Track Roller', 'Carrier Roller', 'Track Shoe', 'Track Chain', 'Bucket Tooth', 'Cutting Edge', 'Oil Filter', 'Fuel Filter', 'Air Filter', 'Hydraulic Filter', 'Final Drive', 'Travel Motor', 'Swing Motor', 'Seal Kit', 'Radiator', 'Starter Motor', 'Alternator', 'Fan Belt', 'V-Belt', 'Battery', 'Turbocharger', 'Injector', 'Control Valve', 'Hydraulic Hose', 'Bearing', 'Gearbox', 'Engine Overhaul Kit']

COMPANIES = ['PT Bumi Resources', 'PT Adaro Logistics', 'PT PAMA Persada', 'PT Kaltim Prima Coal', 'PT Bukit Asam Contractor', 'PT Mitra Konstruksi Nusantara', 'PT Cipta Infrastruktur Indonesia', 'PT Mega Beton', 'CV Sinar Teknik', 'CV Maju Bersama', 'UD Makmur Jaya']
INDIVIDUALS = ['Andi Saputra', 'Budi Santoso', 'Rizky Pratama', 'Dedi Kurniawan', 'Agus Setiawan', 'Rahmat Hidayat', 'Siti Nurhaliza', 'Maya Putri', 'Nur Aisyah', 'Fajar Nugroho']
VENDORS = ['PT Trakindo Utama', 'PT United Tractors', 'PT Hexindo Adiperkasa', 'PT Intraco Penta', 'PT Kobexindo', 'PT Multi Prima Diesel', 'CV Berkah Teknik', 'CV Surya Hidrolik', 'UD Sumber Bearing', 'PT Indo Parts Supply', 'John Hydraulic Service', 'Budi Engineering', 'Komatsu Japan HQ', 'CAT Singapore Hub', 'Volvo Global Parts']

CITIES = ['Jakarta', 'Surabaya', 'Balikpapan', 'Samarinda', 'Makassar', 'Medan', 'Bandung']
COUNTRIES = ['Indonesia', 'Singapore', 'Japan', 'China']

WAREHOUSE_NAMES = ['Main Warehouse', 'Mining Warehouse', 'Project Warehouse', 'Sparepart Warehouse', 'Transit Warehouse']


def wipe_data(env, cr):
    logging.info("WIPING EXISTING TRANSACTION DATA SAFELY...")
    
    # We will use raw SQL for speed but NO CASCADE to avoid breaking users
    cr.execute("DELETE FROM account_payment_register")
    cr.execute("DELETE FROM account_partial_reconcile")
    cr.execute("DELETE FROM account_payment")
    cr.execute("DELETE FROM account_move_line WHERE move_id IN (SELECT id FROM account_move WHERE state != 'draft' OR name NOT LIKE 'INV/2019%')")
    cr.execute("DELETE FROM account_move WHERE state != 'draft' OR name NOT LIKE 'INV/2019%'")
    
    cr.execute("DELETE FROM stock_valuation_layer")
    cr.execute("DELETE FROM stock_quant")
    cr.execute("DELETE FROM stock_move_line")
    cr.execute("DELETE FROM stock_move")
    cr.execute("DELETE FROM stock_picking")
    
    cr.execute("DELETE FROM sale_order_line")
    cr.execute("DELETE FROM sale_order")
    
    cr.execute("DELETE FROM purchase_order_line")
    cr.execute("DELETE FROM purchase_order")
    
    # Delete BIDSS Master data
    cr.execute("DELETE FROM product_product WHERE default_code LIKE 'BIDSS-%'")
    cr.execute("DELETE FROM product_template WHERE default_code LIKE 'BIDSS-%'")
    cr.execute("DELETE FROM res_partner WHERE ref LIKE 'BIDSS-%'")
    
    cr.commit()

def generate_master_data(env):
    logging.info("GENERATING MASTER DATA...")
    
    # 1. Product Category with AVCO and Automated Valuation
    cat = env['product.category'].search([('name', '=', 'BIDSS Automated Valuation')], limit=1)
    if not cat:
        # Create category with AVCO
        # Note: in Odoo 18, property_cost_method is 'average' for AVCO, and property_valuation is 'real_time'
        cat = env['product.category'].create({
            'name': 'BIDSS Automated Valuation',
            'property_cost_method': 'average',
            'property_valuation': 'real_time'
        })
    
    # 2. Products (~550)
    prods = []
    # Heavy Equipments (~50)
    for _ in range(50):
        brand = random.choice(BRANDS)
        he = random.choice(HE_TYPES)
        name = f"{brand} {he} - {random.randint(100, 999)}"
        cost = random.randint(CATEGORIES['Heavy Equipment']['cost'][0], CATEGORIES['Heavy Equipment']['cost'][1])
        sell = int(cost * CATEGORIES['Heavy Equipment']['margin'])
        prods.append({
            'name': name,
            'default_code': f'BIDSS-HE-{random.randint(1000,9999)}',
            'categ_id': cat.id,
            'type': 'consu',
            'is_storable': True,
            'list_price': sell,
            'standard_price': cost,
            'weight': random.randint(5000, 30000),
            '_bidss_cat': 'Heavy Equipment'
        })
    
    # Parts (~500)
    cat_keys = list(CATEGORIES.keys())
    cat_keys.remove('Heavy Equipment')
    for i in range(500):
        part = random.choice(PARTS)
        c_type = random.choice(cat_keys)
        name = f"{part} {random.choice(BRANDS)} Type {random.randint(10, 99)}"
        cost = random.randint(CATEGORIES[c_type]['cost'][0], CATEGORIES[c_type]['cost'][1])
        sell = int(cost * CATEGORIES[c_type]['margin'])
        prods.append({
            'name': name,
            'default_code': f'BIDSS-PRT-{random.randint(10000,99999)}',
            'categ_id': cat.id,
            'type': 'consu',
            'is_storable': True,
            'list_price': sell,
            'standard_price': cost,
            'weight': random.randint(1, 100),
            '_bidss_cat': c_type
        })
        
    created_prods = []
    prod_cat_map = {}
    for p in prods:
        c_type = p.pop('_bidss_cat')
        prod_obj = env['product.product'].create(p)
        created_prods.append(prod_obj)
        prod_cat_map[prod_obj.id] = c_type
        
    # 3. Customers (~300)
    for i in range(300):
        is_company = random.random() < 0.6
        name = random.choice(COMPANIES) + f" {random.randint(1,99)}" if is_company else random.choice(INDIVIDUALS) + f" {random.randint(1,99)}"
        env['res.partner'].create({
            'name': name,
            'is_company': is_company,
            'ref': f'BIDSS-CUST-{i+1}',
            'city': random.choice(CITIES),
            'email': f"contact{i}@example.com",
            'phone': f"0812{random.randint(1000000, 9999999)}"
        })
        
    # 4. Vendors (~300)
    for i in range(300):
        env['res.partner'].create({
            'name': random.choice(VENDORS) + f" {random.randint(1,99)}",
            'is_company': True,
            'ref': f'BIDSS-VEND-{i+1}',
            'city': random.choice(CITIES),
        })

    # 5. Warehouses
    for wname in WAREHOUSE_NAMES:
        if not env['stock.warehouse'].search([('name', '=', wname)]):
            env['stock.warehouse'].create({
                'name': wname,
                'code': wname[:3].upper(),
            })

    return created_prods, prod_cat_map, env['res.partner'].search([('ref', '=like', 'BIDSS-CUST-%')]), env['res.partner'].search([('ref', '=like', 'BIDSS-VEND-%')]), env['stock.warehouse'].search([])

def generate_initial_inventory(env, products, prod_cat_map, warehouses):
    logging.info("GENERATING INITIAL INVENTORY...")
    locs = warehouses.mapped('lot_stock_id')
    
    quant_vals = []
    for prod in products:
        # Pick 1 or 2 warehouses to stock this product
        p_locs = random.sample(locs, random.randint(1, 2))
        c_type = prod_cat_map.get(prod.id, 'Consumables')
        stock_range = CATEGORIES.get(c_type, CATEGORIES['Consumables'])['stock']
        
        for loc in p_locs:
            qty = random.randint(stock_range[0], stock_range[1])
            quant_vals.append({
                'product_id': prod.id,
                'location_id': loc.id,
                'inventory_quantity': qty,
            })
            
    quants = env['stock.quant'].create(quant_vals)
    # Apply inventory immediately
    quants.action_apply_inventory()

def generate_transactions(env, products, customers, vendors, start_date):
    logging.info(f"GENERATING TRANSACTIONS (DAY BY DAY) STARTING FROM {start_date.strftime('%Y-%m-%d')}...")
    end_date = datetime(YEAR, 12, 31)
    
    current_date = start_date
    while current_date <= end_date:
        # Only weekdays for majority of transactions
        if current_date.weekday() > 4 and random.random() < 0.8:
            current_date += timedelta(days=1)
            continue
            
        month = current_date.month
        w = MONTH_WEIGHTS[month]
        
        # Calculate daily volume (0 to 8 per day, scaled by weight)
        # 20% chance of completely 0 transactions (holidays/no business)
        if random.random() < 0.2:
            base_so = 0
            base_po = 0
        else:
            base_so = random.randint(1, 8)
            base_po = random.randint(1, 8)
        
        so_vol = int(base_so * w['so_w'])
        po_vol = int(base_po * w['po_w'])
        
        date_str = current_date.strftime('%Y-%m-%d %H:%M:%S')
        
        # --- SALES ---
        for _ in range(so_vol):
            state_rand = random.random()
            status = 'sale'
            if state_rand < 0.1: status = 'draft'
            elif state_rand < 0.15: status = 'cancel'
            
            so = env['sale.order'].create({
                'partner_id': random.choice(customers).id,
                'date_order': date_str,
                'order_line': [
                    (0, 0, {
                        'product_id': p.id,
                        'product_uom_qty': random.randint(1, 5),
                        'price_unit': p.list_price,
                        'discount': random.choice([0, 0, 0, 5, 10])
                    }) for p in random.sample(products, random.randint(2, 6))
                ]
            })
            
            if status == 'sale':
                so.action_confirm()
                so.write({'date_order': date_str})
                
                # Deliver
                for picking in so.picking_ids:
                    picking.date_done = date_str
                    for move in picking.move_ids:
                        move.quantity = move.product_uom_qty
                        move.date = date_str
                    picking.button_validate()
                    
                # Invoice
                inv = so._create_invoices()
                if inv:
                    inv.invoice_date = current_date.strftime('%Y-%m-%d')
                    inv.action_post()
                    # Pay
                    env['account.payment.register'].with_context(active_model='account.move', active_ids=inv.ids).create({
                        'payment_date': current_date.strftime('%Y-%m-%d')
                    }).action_create_payments()
            elif status == 'cancel':
                so.action_cancel()

        # --- PURCHASE ---
        for _ in range(po_vol):
            state_rand = random.random()
            status = 'purchase'
            if state_rand < 0.1: status = 'draft'
            elif state_rand < 0.15: status = 'cancel'
            
            planned_date = current_date + timedelta(days=w['lt'] + random.randint(-2, 2))
            
            po = env['purchase.order'].create({
                'partner_id': random.choice(vendors).id,
                'date_order': date_str,
                'date_planned': planned_date.strftime('%Y-%m-%d %H:%M:%S'),
                'order_line': [
                    (0, 0, {
                        'product_id': p.id,
                        'product_qty': random.randint(5, 20),
                        'price_unit': p.standard_price,
                    }) for p in random.sample(products, random.randint(2, 8))
                ]
            })
            
            if status == 'purchase':
                po.button_confirm()
                po.write({'date_planned': planned_date.strftime('%Y-%m-%d %H:%M:%S')})
                
                # Receive
                for picking in po.picking_ids:
                    picking.date_done = planned_date.strftime('%Y-%m-%d %H:%M:%S')
                    for move in picking.move_ids:
                        move.quantity = move.product_uom_qty
                        move.date = planned_date.strftime('%Y-%m-%d %H:%M:%S')
                    picking.button_validate()
                    
                # Bill
                po.action_create_invoice()
                for bill in po.invoice_ids:
                    bill.invoice_date = planned_date.strftime('%Y-%m-%d')
                    bill.action_post()
                    # Pay
                    env['account.payment.register'].with_context(active_model='account.move', active_ids=bill.ids).create({
                        'payment_date': planned_date.strftime('%Y-%m-%d')
                    }).action_create_payments()
            elif status == 'cancel':
                po.button_cancel()

        env.cr.commit()
        current_date += timedelta(days=1)
        if current_date.day == 1:
            logging.info(f"Finished processing up to {current_date.strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    logging.info("Starting BIDSS Phase 6 Refactor Generator...")
    odoo.tools.config.parse_config(['-c', r'C:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo.conf', '-d', 'Business_Intelegent_Project_v2'])
    registry = odoo.modules.registry.Registry('Business_Intelegent_Project_v2')
    with registry.cursor() as cr:
        env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
        
        # Determine start date
        cr.execute("SELECT MAX(date_order) FROM sale_order WHERE partner_id IN (SELECT id FROM res_partner WHERE ref LIKE 'BIDSS-CUST-%')")
        res = cr.fetchone()
        max_so_date = res[0] if res else None
        
        if max_so_date:
            logging.info(f"RESUMING FROM {max_so_date}")
            start_date = max_so_date + timedelta(days=1)
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            
            prods = env['product.product'].search([('default_code', '=like', 'BIDSS-%')])
            custs = env['res.partner'].search([('ref', '=like', 'BIDSS-CUST-%')])
            vends = env['res.partner'].search([('ref', '=like', 'BIDSS-VEND-%')])
            generate_transactions(env, prods, custs, vends, start_date=start_date)
        else:
            logging.info("NO EXISTING DATA FOUND. STARTING FROM SCRATCH.")
            wipe_data(env, cr)
            prods, prod_cat_map, custs, vends, whs = generate_master_data(env)
            generate_initial_inventory(env, prods, prod_cat_map, whs)
            cr.commit()
            
            start_date = datetime(YEAR, 1, 1)
            generate_transactions(env, prods, custs, vends, start_date=start_date)
        
    logging.info("DATA GENERATION COMPLETE!")
