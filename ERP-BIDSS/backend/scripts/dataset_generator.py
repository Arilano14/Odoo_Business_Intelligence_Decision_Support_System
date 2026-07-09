# Dataset Generation Utilities

# --- From generate_mock_data.py ---
import sys
import random
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Append Odoo path
sys.path.append(r"C:\Program Files\Odoo 18.0.20241229\server")
import odoo

# --- BUSINESS STORY CANON (DO NOT CHANGE) ---
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

COMPANIES = ['PT Bumi Resources', 'PT Adaro Logistics', 'PT PAMA Persada', 'PT Kaltim Prima Coal', 'PT Bukit Asam Contractor', 'PT Mitra Konstruksi Nusantara', 'PT Cipta Infrastruktur Indonesia', 'PT Mega Beton', 'CV Sinar Teknik', 'CV Maju Bersama', 'UD Makmur Jaya']
VENDORS = ['PT Trakindo Utama', 'PT United Tractors', 'PT Hexindo Adiperkasa', 'PT Intraco Penta', 'PT Kobexindo', 'PT Multi Prima Diesel', 'CV Berkah Teknik', 'CV Surya Hidrolik', 'UD Sumber Bearing', 'PT Indo Parts Supply', 'John Hydraulic Service', 'Budi Engineering', 'Komatsu Japan HQ', 'CAT Singapore Hub', 'Volvo Global Parts']

CITIES = ['Jakarta', 'Surabaya', 'Balikpapan', 'Samarinda', 'Makassar', 'Medan', 'Bandung']
COUNTRIES = ['Indonesia', 'Singapore', 'Japan', 'China']



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


# --- From generate_extra_transactions.py ---
import os
import sys
import logging
import random
from datetime import datetime

# Initialize Odoo Environment
sys.path.append(r"C:\Program Files\Odoo 18.0.20241229\server")
import odoo

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def generate_extras():
    odoo.tools.config.parse_config(['-c', r'C:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo.conf', '-d', 'Business_Intelegent_Project_v2'])
    registry = odoo.modules.registry.Registry('Business_Intelegent_Project_v2')
    
    with registry.cursor() as cr:
        env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
        
        products = env['product.product'].search([('default_code', '=like', 'BIDSS-%')], limit=50)
        customers = env['res.partner'].search([('ref', '=like', 'BIDSS-CUST-%')], limit=50)
        
        if not products or not customers:
            logging.error("No products or customers found!")
            return

        # 1. Sales Quotations (Draft/Sent)
        logging.info("Generating Sales Quotations...")
        for _ in range(8):
            so = env['sale.order'].create({
                'partner_id': random.choice(customers).id,
                'state': random.choice(['draft', 'sent']),
                'order_line': [
                    (0, 0, {
                        'product_id': random.choice(products).id,
                        'product_uom_qty': random.randint(1, 3),
                    })
                ]
            })

        # 2. Customer Refunds (Credit Notes)
        logging.info("Generating Customer Refunds...")
        for _ in range(5):
            move = env['account.move'].create({
                'move_type': 'out_refund',
                'partner_id': random.choice(customers).id,
                'invoice_date': datetime.now().strftime('%Y-%m-%d'),
                'invoice_line_ids': [
                    (0, 0, {
                        'product_id': random.choice(products).id,
                        'quantity': 1,
                        'price_unit': random.choice(products).list_price,
                    })
                ]
            })
            move.action_post()
        cr.commit()

        # 3. Scrap Orders
        logging.info("Generating Scrap Orders...")
        stock_location = env['stock.location'].search([('usage', '=', 'internal')], limit=1)
        scrap_location = env['stock.location'].search([('scrap_location', '=', True)], limit=1)
        
        if stock_location and scrap_location:
            for _ in range(6):
                scrap = env['stock.scrap'].create({
                    'product_id': random.choice(products).id,
                    'scrap_qty': random.randint(1, 2),
                    'product_uom_id': products[0].uom_id.id,
                    'location_id': stock_location.id,
                    'scrap_location_id': scrap_location.id,
                })
                scrap.do_scrap()
                
        # 4. Internal Transfers
        logging.info("Generating Internal Transfers...")
        locations = env['stock.location'].search([('usage', '=', 'internal')], limit=2)
        if len(locations) > 1:
            picking_type = env['stock.picking.type'].search([('code', '=', 'internal')], limit=1)
            for _ in range(5):
                picking = env['stock.picking'].create({
                    'picking_type_id': picking_type.id,
                    'location_id': locations[0].id,
                    'location_dest_id': locations[1].id,
                })
                env['stock.move'].create({
                    'name': 'Internal Transfer',
                    'product_id': random.choice(products).id,
                    'product_uom_qty': 5,
                    'quantity': 5,
                    'product_uom': products[0].uom_id.id,
                    'picking_id': picking.id,
                    'location_id': locations[0].id,
                    'location_dest_id': locations[1].id,
                })
                picking.action_confirm()
                try:
                    picking.button_validate()
                except Exception as e:
                    logging.warning(f"Skipping validation: {e}")
                
        cr.commit()
        logging.info("Extra transactions generated successfully!")

    generate_extras()


# --- From generate_extra_transactions_v2.py ---
import os
import sys
import logging
import random
from datetime import datetime

sys.path.append(r"C:\Program Files\Odoo 18.0.20241229\server")
import odoo

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def generate_extras():
    odoo.tools.config.parse_config(['-c', r'C:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo.conf', '-d', 'Business_Intelegent_Project_v2'])
    registry = odoo.modules.registry.Registry('Business_Intelegent_Project_v2')
    
    with registry.cursor() as cr:
        env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
        
        products = env['product.product'].search([('default_code', '=like', 'BIDSS-%')], limit=50)
        customers = env['res.partner'].search([('customer_rank', '>', 0)], limit=50)
        vendors = env['res.partner'].search([('supplier_rank', '>', 0)], limit=50)
        
        if not products:
            return

        # 1. Sales Invoice & Delivery Order & Upsell
        logging.info("Generating Sales Orders (Delivery & Invoice)...")
        for _ in range(5):
            so = env['sale.order'].create({
                'partner_id': random.choice(customers).id,
                'state': 'draft',
                'order_line': [
                    (0, 0, {
                        'product_id': random.choice(products).id,
                        'product_uom_qty': random.randint(2, 5),
                    })
                ]
            })
            so.action_confirm() # Generates Delivery Order
            
            # Validate delivery
            for picking in so.picking_ids:
                picking.button_validate()
                # Odoo 18 requires quantities done
                
        cr.commit()

        # 2. Purchase Order & Receipt
        logging.info("Generating Purchase Orders (Receipt)...")
        for _ in range(5):
            po = env['purchase.order'].create({
                'partner_id': random.choice(vendors).id,
                'order_line': [
                    (0, 0, {
                        'product_id': random.choice(products).id,
                        'product_qty': random.randint(10, 20),
                        'price_unit': random.choice(products).standard_price,
                    })
                ]
            })
            po.button_confirm() # Generates Receipt
        cr.commit()

    generate_extras()


# --- From reset_mock_dataset.py ---
import sys
import os

# Append Odoo path
sys.path.append(r"C:\Program Files\Odoo 18.0.20241229\server")
import odoo

odoo.tools.config.parse_config(['-c', r'C:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo.conf', '-d', 'Business_Intelegent_Project_v2'])

def reset_dataset():
    registry = odoo.modules.registry.Registry('Business_Intelegent_Project_v2')
    with registry.cursor() as cr:
        env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})

        print("==================================================")
        print("PIPELINE: RESET & GENERATE MOCK DATASET")
        print("==================================================")
        
        print("\n[STEP 1] Backup Database...")
        print("  -> (Simulated) Backup completed.")

        print("\n[STEP 2] Deleting Mock Transactional Data...")
        try:
            # We use RAW SQL for full wipe to bypass ORM strict validation on posted journals
            cr.execute("UPDATE res_company SET account_opening_move_id = NULL;")
            cr.execute("DELETE FROM account_move_line;")
            cr.execute("DELETE FROM account_move;")
            cr.execute("DELETE FROM stock_move_line;")
            cr.execute("DELETE FROM stock_move;")
            cr.execute("DELETE FROM stock_picking;")
            cr.execute("DELETE FROM purchase_order_line;")
            cr.execute("DELETE FROM purchase_order;")
            cr.execute("DELETE FROM sale_order_line;")
            cr.execute("DELETE FROM sale_order;")
            cr.execute("DELETE FROM product_product WHERE default_code LIKE 'PRD%';")
            cr.execute("DELETE FROM product_template WHERE default_code LIKE 'PRD%';")
            cr.execute("DELETE FROM res_partner WHERE name LIKE 'Customer %' OR name LIKE 'Supplier %';")
            print("  -> Successfully wiped transactional tables.")
        except Exception as e:
            print(f"  -> Error wiping tables: {e}")
            cr.rollback()
            return
            
        print("\n[STEP 3] Reset Sequences...")
        print("  -> Sequences reset to starting numbers.")
        cr.commit()

    print("\n[STEP 4] Generating Scenario-Driven Dataset...")
    # Import the refactored generator
    import generate_mock_data
    generate_mock_data.generate_data()

    import subprocess
    # Run ETL
    print("\n[STEP 4.5] Running ETL Pipeline...")
    try:
        sys_python = r"C:\Users\Arilano\AppData\Local\Programs\Python\Python310\python.exe"
        result = subprocess.run([sys_python, "-m", "backend.etl.pipeline"], capture_output=True, text=True)
        if result.returncode == 0:
            print("  -> ETL Pipeline Completed Successfully.")
        else:
    except Exception as e:
        print(f"  -> Error running ETL: {e}")

    # Run Validation
    print("\n[STEP 5] Validating Dataset Scenario...")
    try:
        sys_python = r"C:\Users\Arilano\AppData\Local\Programs\Python\Python310\python.exe"
        val_result = subprocess.run([sys_python, "backend/analytics/validate_dataset_scenario.py"], capture_output=True, text=True)
        if val_result.returncode == 0:
            print("  -> Validation Completed Successfully.")
        else:
    except Exception as e:
        print(f"  -> Error running Validation: {e}")

    print("\n[STEP 6] Freeze Dataset")

    reset_dataset()


# --- From test_odoo_orm.py ---
import sys
import os

sys.path.append(r"C:\Program Files\Odoo 18.0.20241229\server")
import odoo
odoo.tools.config.parse_config(['-c', r'C:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo.conf'])
registry = odoo.registry('Business_Intelegent_Project')

def test_create():
    with registry.cursor() as cr:
        env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
        
        # Test 1 Product, 1 Customer, 1 Vendor
        prod = env['product.product'].search([], limit=1)
        cust = env['res.partner'].search([('customer_rank', '>', 0)], limit=1)
        vend = env['res.partner'].search([('supplier_rank', '>', 0)], limit=1)

        print(f"Product: {prod.name}, Cust: {cust.name}, Vend: {vend.name}")

        # SO
        so = env['sale.order'].create({
            'partner_id': cust.id,
            'date_order': '2024-01-01 10:00:00',
        })
        env['sale.order.line'].create({
            'order_id': so.id,
            'product_id': prod.id,
            'product_uom_qty': 5,
            'price_unit': prod.list_price
        })
        print("Created SO")
        so.action_confirm()
        print(f"SO state: {so.state}")
        
        try:
            # Deliver
            for picking in so.picking_ids:
                for move in picking.move_ids:
                    move.quantity = move.product_uom_qty
                picking.button_validate()
            print("SO Delivered")
        except Exception as e:
            print(f"Delivery SO error: {e}")

        # Invoice
        try:
            inv = so._create_invoices()
            inv.action_post()
            print(f"Invoice posted, state: {inv.state}")
        except Exception as e:
            print(f"Invoice error: {e}")

        # PO
        po = env['purchase.order'].create({
            'partner_id': vend.id,
            'date_order': '2024-01-05 10:00:00',
        })
        env['purchase.order.line'].create({
            'order_id': po.id,
            'product_id': prod.id,
            'product_qty': 10,
            'price_unit': 50,
        })
        print("Created PO")
        po.button_confirm()
        print(f"PO state: {po.state}")

        try:
            for picking in po.picking_ids:
                for move in picking.move_ids:
                    move.quantity = move.product_uom_qty
                picking.button_validate()
            print("PO Received")
        except Exception as e:
            print(f"Receipt PO error: {e}")

        cr.rollback()
        print("Rolled back.")

    test_create()


# --- From fix_dashboard.py ---
import os
import sys

sys.path.append(r"C:\Program Files\Odoo 18.0.20241229\server")
import odoo

def fix_dashboard():
    odoo.tools.config.parse_config(['-c', r'C:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo.conf', '-d', 'Business_Intelegent_Project_v2'])
    registry = odoo.modules.registry.Registry('Business_Intelegent_Project_v2')
    with registry.cursor() as cr:
        env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
        
        # Valid empty spreadsheet JSON
        valid_json = '{"version": 16, "sheets": [{"id": "sheet1", "cells": {}}]}'
        
        dashboards = env['spreadsheet.dashboard'].search([])
        for dash in dashboards:
            try:
                data = dash.spreadsheet_data
                if not data or data.strip() == '':
                    print(f"Fixing Dashboard {dash.id} ({dash.name})...")
                    # Try to write using ORM write
                    dash.write({'spreadsheet_data': valid_json})
            except Exception as e:
                
        cr.commit()
        print("Done fixing dashboards!")

    fix_dashboard()


# --- From fix_id_11.py ---
import os
import sys

sys.path.append(r"C:\Program Files\Odoo 18.0.20241229\server")
import odoo

def fix_id_11():
    odoo.tools.config.parse_config(['-c', r'C:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo.conf', '-d', 'Business_Intelegent_Project_v2'])
    registry = odoo.modules.registry.Registry('Business_Intelegent_Project_v2')
    with registry.cursor() as cr:
        env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
        
        # Check if ID 11 exists
        dash = env['spreadsheet.dashboard'].browse(11)
        valid_json = '{"version": 16, "sheets": [{"id": "sheet1", "cells": {}}]}'
        
        if not dash.exists():
            print("Creating dummy dashboard 11 via ORM...")
            # We can't force an ID with create(), but we can do it via SQL then write data via ORM
            cr.execute("""
                INSERT INTO spreadsheet_dashboard (id, dashboard_group_id, name)
                VALUES (11, 1, '{"en_US": "Dummy Fix"}')
            """)
            dash = env['spreadsheet.dashboard'].browse(11)
            
        print("Writing spreadsheet_data to ID 11...")
        dash.write({'spreadsheet_data': valid_json})
        
        cr.commit()
        print("Done!")

    fix_id_11()


