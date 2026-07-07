import sys
import os
import random
from datetime import datetime, timedelta

# Append Odoo path
sys.path.append(r"C:\Program Files\Odoo 18.0.20241229\server")
import odoo

# Config is handled by the caller or at bottom of this file


# Business Scenario Engine (KPI Targets 12 Months)
# Baseline: ~33 POs, ~33 SOs per month. Qty per line ~20.
MONTH_WEIGHTS = {
    1:  {'so_count': 1.0, 'po_count': 1.0, 'po_qty': 1.0, 'so_qty': 1.0, 'lead_time': 5},    # Jan: Baseline Normal
    2:  {'so_count': 1.08, 'po_count': 1.0, 'po_qty': 1.0, 'so_qty': 1.08, 'lead_time': 5},  # Feb: Sales naik 8%
    3:  {'so_count': 0.95, 'po_count': 1.0, 'po_qty': 1.0, 'so_qty': 0.95, 'lead_time': 10}, # Mar: Supplier Delay (Lead Time 10), Stockout
    4:  {'so_count': 1.0, 'po_count': 1.4, 'po_qty': 1.4, 'so_qty': 1.0, 'lead_time': 6},    # Apr: Panic Buying (+40% purchase)
    5:  {'so_count': 0.9, 'po_count': 0.8, 'po_qty': 0.8, 'so_qty': 0.9, 'lead_time': 5},    # May: Overstock (Demand turun, stop purchase)
    6:  {'so_count': 0.9, 'po_count': 0.8, 'po_qty': 0.8, 'so_qty': 0.9, 'lead_time': 5},    # Jun: Warehouse Full
    7:  {'so_count': 0.8, 'po_count': 0.9, 'po_qty': 0.9, 'so_qty': 0.8, 'lead_time': 5},    # Jul: Slow Moving
    8:  {'so_count': 1.1, 'po_count': 1.0, 'po_qty': 1.0, 'so_qty': 1.1, 'lead_time': 5},    # Aug: Promosi (Sales naik)
    9:  {'so_count': 1.0, 'po_count': 1.0, 'po_qty': 1.0, 'so_qty': 1.0, 'lead_time': 5},    # Sep: Recovery
    10: {'so_count': 1.0, 'po_count': 1.0, 'po_qty': 1.0, 'so_qty': 1.0, 'lead_time': 5},    # Oct: Stabil
    11: {'so_count': 1.2, 'po_count': 1.2, 'po_qty': 1.2, 'so_qty': 1.2, 'lead_time': 5},    # Nov: Peak Mining Project
    12: {'so_count': 1.1, 'po_count': 1.1, 'po_qty': 1.1, 'so_qty': 1.1, 'lead_time': 5},    # Dec: Year End Closing
}

TOTAL_SO = 400
TOTAL_PO = 400
NUM_PROD = 500
NUM_CUST = 300
NUM_VEND = 300
YEAR = 2024

def generate_data():
    registry = odoo.modules.registry.Registry('Business_Intelegent_Project_v2')
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

        # Base values
        base_po_count = TOTAL_PO // 12
        base_so_count = TOTAL_SO // 12

        print("\n[2/4] Generating Purchase Orders (with delay simulation)...")
        for month, w in MONTH_WEIGHTS.items():
            month_pos = int(base_po_count * w['po_count'])
            lead_time = w['lead_time']
            po_qty_mult = w['po_qty']
            
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
                
                # 5 to 12 lines per PO
                for _ in range(random.randint(5, 12)):
                    prod = random.choice(products)
                    base_qty = random.randint(10, 40)
                    qty = int(base_qty * po_qty_mult)
                    po_vals['order_line'].append((0, 0, {
                        'product_id': prod.id,
                        'product_qty': max(1, qty),
                        'price_unit': prod.standard_price,
                    }))
                
                po = env['purchase.order'].create(po_vals)
                po.button_confirm()
                
                # FIX: Force date_planned back to our simulated date (Odoo overrides it on confirm)
                po.write({'date_planned': planned_date.strftime('%Y-%m-%d %H:%M:%S')})

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
            month_sos = int(base_so_count * w['so_count'])
            so_qty_mult = w['so_qty']
            
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
                
                for _ in range(random.randint(5, 12)):
                    prod = random.choice(products)
                    base_qty = random.randint(1, 10)
                    qty = int(base_qty * so_qty_mult)
                    so_vals['order_line'].append((0, 0, {
                        'product_id': prod.id,
                        'product_uom_qty': max(1, qty),
                        'price_unit': prod.list_price,
                    }))
                
                so = env['sale.order'].create(so_vals)
                so.action_confirm()
                
                # FIX: Force date_order back to our simulated date
                so.write({'date_order': order_date.strftime('%Y-%m-%d %H:%M:%S')})

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
    odoo.tools.config.parse_config(['-c', r'C:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo.conf', '-d', 'Business_Intelegent_Project_v2'])
    generate_data()
