import sys
import os
import random
from datetime import datetime, timedelta

# Append Odoo path
sys.path.append(r"C:\Program Files\Odoo 18.0.20241229\server")
import odoo

odoo.tools.config.parse_config(['-c', r'C:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo.conf'])

# Scenario weights for 2024 (Jan - Dec)
# Used to distribute 2000 SOs and 2000 POs across the year
MONTH_WEIGHTS = {
    1:  {'so': 100, 'po': 100, 'lead_time': 5},   # Jan: Baseline
    2:  {'so': 108, 'po': 105, 'lead_time': 5},   # Feb: SO +8%, PO +5%
    3:  {'so': 103, 'po': 110, 'lead_time': 10},  # Mar: SO -5%, PO +5%, Delay
    4:  {'so': 113, 'po': 154, 'lead_time': 6},   # Apr: SO +10%, PO +40%
    5:  {'so': 102, 'po': 146, 'lead_time': 5},   # May: SO -10%, PO -5%
    6:  {'so': 102, 'po': 146, 'lead_time': 5},   # Jun: SO 0%, PO 0%
    7:  {'so': 107, 'po': 153, 'lead_time': 5},   # Jul: SO +5%, PO +5%
    8:  {'so': 112, 'po': 138, 'lead_time': 5},   # Aug: SO +5%, PO -10%
    9:  {'so': 123, 'po': 131, 'lead_time': 5},   # Sep: SO +10%, PO -5%
    10: {'so': 138, 'po': 144, 'lead_time': 5},   # Oct: SO +12%, PO +10%
    11: {'so': 159, 'po': 161, 'lead_time': 5},   # Nov: SO +15%, PO +12%
    12: {'so': 191, 'po': 185, 'lead_time': 5},   # Dec: SO +20%, PO +15%
}

TOTAL_SO = 2000
TOTAL_PO = 2000
NUM_PROD = 500
NUM_CUST = 300
NUM_VEND = 300
YEAR = 2024

def generate_data():
    registry = odoo.modules.registry.Registry('Business_Intelegent_Project')
    with registry.cursor() as cr:
        env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})

        print("--- PHASE 6: Odoo Scenario-Driven Data Generator ---")
        
        # 1. Master Data
        print("\n[1/4] Generating Master Data...")
        products = env['product.product'].search([('default_code', '=like', 'BIDSS-%')])
        if len(products) < NUM_PROD:
            print(f"Creating {NUM_PROD - len(products)} Products...")
            prod_vals = []
            for i in range(len(products), NUM_PROD):
                prod_vals.append({
                    'name': f'Alat Berat Part {i}',
                    'default_code': f'BIDSS-PROD-{i}',
                    'type': 'consu',  # Odoo 18 mechanism
                    'is_storable': True,
                    'list_price': random.randint(100, 500) * 1000,
                    'standard_price': random.randint(50, 400) * 1000,
                })
            products = env['product.product'].create(prod_vals)
        else:
            print("Products already exist.")

        customers = env['res.partner'].search([('ref', '=like', 'BIDSS-CUST-%')])
        if len(customers) < NUM_CUST:
            print(f"Creating {NUM_CUST - len(customers)} Customers...")
            cust_vals = []
            for i in range(len(customers), NUM_CUST):
                cust_vals.append({
                    'name': f'PT Tambang Konstruksi {i}',
                    'ref': f'BIDSS-CUST-{i}',
                    'customer_rank': 1,
                    'city': random.choice(['Jakarta', 'Surabaya', 'Balikpapan', 'Samarinda', 'Makassar'])
                })
            customers = env['res.partner'].create(cust_vals)
        else:
            print("Customers already exist.")

        vendors = env['res.partner'].search([('ref', '=like', 'BIDSS-VEND-%')])
        if len(vendors) < NUM_VEND:
            print(f"Creating {NUM_VEND - len(vendors)} Vendors...")
            vend_vals = []
            for i in range(len(vendors), NUM_VEND):
                vend_vals.append({
                    'name': f'Supplier Internasional {i}',
                    'ref': f'BIDSS-VEND-{i}',
                    'supplier_rank': 1,
                    'city': random.choice(['Tokyo', 'Shanghai', 'Seoul', 'Jakarta', 'Singapore'])
                })
            vendors = env['res.partner'].create(vend_vals)
        else:
            print("Vendors already exist.")

        # Ensure we use our BIDSS items
        products = env['product.product'].search([('default_code', '=like', 'BIDSS-%')])
        customers = env['res.partner'].search([('ref', '=like', 'BIDSS-CUST-%')])
        vendors = env['res.partner'].search([('ref', '=like', 'BIDSS-VEND-%')])

        # Pre-calculate counts per month
        so_weight_total = sum(m['so'] for m in MONTH_WEIGHTS.values())
        po_weight_total = sum(m['po'] for m in MONTH_WEIGHTS.values())

        print("\n[2/4] Generating Purchase Orders (with delay simulation)...")
        for month, w in MONTH_WEIGHTS.items():
            month_pos = int((w['po'] / po_weight_total) * TOTAL_PO)
            lead_time = w['lead_time']
            
            # Start and end of month
            start_date = datetime(YEAR, month, 1)
            end_date = (datetime(YEAR, month % 12 + 1, 1) - timedelta(days=1)) if month < 12 else datetime(YEAR, 12, 31)
            
            print(f"  Month {month}: {month_pos} POs (Lead Time: {lead_time} days)")
            
            for _ in range(month_pos):
                order_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
                planned_date = order_date + timedelta(days=lead_time + random.randint(-1, 2)) # Slight variance
                
                po_vals = {
                    'partner_id': random.choice(vendors).id,
                    'date_order': order_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'date_planned': planned_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'order_line': []
                }
                
                # 1 to 4 lines per PO
                for _ in range(random.randint(1, 4)):
                    prod = random.choice(products)
                    po_vals['order_line'].append((0, 0, {
                        'product_id': prod.id,
                        'product_qty': random.randint(10, 50),
                        'price_unit': prod.standard_price,
                    }))
                
                po = env['purchase.order'].create(po_vals)
                po.button_confirm()

                # Validate receipt to generate stock_move as done
                if hasattr(po, 'picking_ids'):
                    for picking in po.picking_ids:
                        picking.date_done = planned_date.strftime('%Y-%m-%d %H:%M:%S')
                        for move in picking.move_ids:
                            move.quantity = move.product_uom_qty
                            move.date = planned_date.strftime('%Y-%m-%d %H:%M:%S')
                        picking.button_validate()

                # Create Invoice
                po.action_create_invoice()
                if po.invoice_ids:
                    po.invoice_ids.invoice_date = planned_date.strftime('%Y-%m-%d')
                    po.invoice_ids.action_post()
            
            cr.commit()

        print("\n[3/4] Generating Sales Orders...")
        for month, w in MONTH_WEIGHTS.items():
            month_sos = int((w['so'] / so_weight_total) * TOTAL_SO)
            
            start_date = datetime(YEAR, month, 1)
            end_date = (datetime(YEAR, month % 12 + 1, 1) - timedelta(days=1)) if month < 12 else datetime(YEAR, 12, 31)
            
            print(f"  Month {month}: {month_sos} SOs")
            
            for _ in range(month_sos):
                order_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
                
                so_vals = {
                    'partner_id': random.choice(customers).id,
                    'date_order': order_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'order_line': []
                }
                
                for _ in range(random.randint(1, 4)):
                    prod = random.choice(products)
                    # Simulated stockout for March: Some SOs cannot be fulfilled immediately, but we will simplify
                    # by just making the orders smaller or less frequent via weights.
                    so_vals['order_line'].append((0, 0, {
                        'product_id': prod.id,
                        'product_uom_qty': random.randint(1, 10),
                        'price_unit': prod.list_price,
                    }))
                
                so = env['sale.order'].create(so_vals)
                so.action_confirm()

                # Validate delivery
                if hasattr(so, 'picking_ids'):
                    for picking in so.picking_ids:
                        picking.date_done = order_date.strftime('%Y-%m-%d %H:%M:%S')
                        for move in picking.move_ids:
                            move.quantity = move.product_uom_qty
                            move.date = order_date.strftime('%Y-%m-%d %H:%M:%S')
                        picking.button_validate()

                # Create Invoice
                inv = so._create_invoices()
                if inv:
                    inv.invoice_date = order_date.strftime('%Y-%m-%d')
                    inv.action_post()

            cr.commit()

        print("\n[4/4] Data Generation Complete!")

if __name__ == "__main__":
    generate_data()
