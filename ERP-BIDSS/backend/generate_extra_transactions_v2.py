"""
Generate additional Odoo transactions to fill empty dashboard sections.
Targets: Purchase Trend, Invoicing Trend, Receipts (visible), Delivery Orders (done).
Does NOT touch the frozen ELT mart data.
"""
import os
import sys
import logging
import random
from datetime import datetime, timedelta

sys.path.append(r"C:\Program Files\Odoo 18.0.20241229\server")
import odoo

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def generate_odoo_visible_transactions():
    odoo.tools.config.parse_config([
        '-c', r'C:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo.conf',
        '-d', 'Business_Intelegent_Project_v2'
    ])
    registry = odoo.modules.registry.Registry('Business_Intelegent_Project_v2')

    with registry.cursor() as cr:
        env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})

        products = env['product.product'].search([('default_code', '=like', 'BIDSS-%')], limit=30)
        customers = env['res.partner'].search([('customer_rank', '>', 0)], limit=30)
        vendors = env['res.partner'].search([('supplier_rank', '>', 0)], limit=30)

        if not products or not customers or not vendors:
            logging.error("Missing master data!")
            return

        # ============================================================
        # 1. PURCHASE ORDERS (Recent - for Purchase Trend visibility)
        # ============================================================
        logging.info("=== Creating 8 Purchase Orders (recent dates) ===")
        today = datetime.now()
        for i in range(8):
            order_date = today - timedelta(days=random.randint(0, 30))
            prod = random.choice(products)
            po = env['purchase.order'].create({
                'partner_id': random.choice(vendors).id,
                'date_order': order_date.strftime('%Y-%m-%d %H:%M:%S'),
                'order_line': [(0, 0, {
                    'product_id': prod.id,
                    'name': prod.name or 'Product',
                    'product_qty': random.randint(5, 20),
                    'price_unit': prod.standard_price or 100000,
                    'date_planned': (order_date + timedelta(days=5)).strftime('%Y-%m-%d'),
                })]
            })
            po.button_confirm()
            logging.info(f"  PO #{po.name} confirmed ({order_date.strftime('%Y-%m-%d')})")

            # Validate the receipt (incoming picking)
            for picking in po.picking_ids:
                for move in picking.move_ids:
                    move.quantity = move.product_uom_qty
                try:
                    picking.button_validate()
                    logging.info(f"    Receipt validated for PO #{po.name}")
                except Exception as e:
                    logging.warning(f"    Receipt validation skipped: {e}")

        cr.commit()
        logging.info("Purchase Orders committed.")

        # ============================================================
        # 2. VENDOR BILLS (for Invoicing Trend)
        # ============================================================
        logging.info("=== Creating 6 Vendor Bills ===")
        for i in range(6):
            bill_date = today - timedelta(days=random.randint(0, 25))
            prod = random.choice(products)
            bill = env['account.move'].create({
                'move_type': 'in_invoice',
                'partner_id': random.choice(vendors).id,
                'invoice_date': bill_date.strftime('%Y-%m-%d'),
                'invoice_line_ids': [(0, 0, {
                    'product_id': prod.id,
                    'quantity': random.randint(1, 5),
                    'price_unit': prod.standard_price or 50000,
                })]
            })
            bill.action_post()
            logging.info(f"  Vendor Bill #{bill.name} posted ({bill_date.strftime('%Y-%m-%d')})")

        cr.commit()
        logging.info("Vendor Bills committed.")

        # ============================================================
        # 3. CUSTOMER INVOICES (for Invoicing Trend)
        # ============================================================
        logging.info("=== Creating 6 Customer Invoices ===")
        for i in range(6):
            inv_date = today - timedelta(days=random.randint(0, 25))
            prod = random.choice(products)
            invoice = env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': random.choice(customers).id,
                'invoice_date': inv_date.strftime('%Y-%m-%d'),
                'invoice_line_ids': [(0, 0, {
                    'product_id': prod.id,
                    'quantity': random.randint(1, 3),
                    'price_unit': prod.list_price or 100000,
                })]
            })
            invoice.action_post()
            logging.info(f"  Invoice #{invoice.name} posted ({inv_date.strftime('%Y-%m-%d')})")

        cr.commit()
        logging.info("Customer Invoices committed.")

        # ============================================================
        # 4. SALES ORDERS with completed Delivery (for Delivery Orders done)
        # ============================================================
        logging.info("=== Creating 6 Sales Orders with Deliveries ===")
        for i in range(6):
            order_date = today - timedelta(days=random.randint(0, 20))
            prod = random.choice(products)
            so = env['sale.order'].create({
                'partner_id': random.choice(customers).id,
                'date_order': order_date.strftime('%Y-%m-%d %H:%M:%S'),
                'order_line': [(0, 0, {
                    'product_id': prod.id,
                    'product_uom_qty': random.randint(1, 3),
                })]
            })
            so.action_confirm()
            logging.info(f"  SO #{so.name} confirmed ({order_date.strftime('%Y-%m-%d')})")

            # Validate delivery
            for picking in so.picking_ids:
                for move in picking.move_ids:
                    move.quantity = move.product_uom_qty
                try:
                    picking.button_validate()
                    logging.info(f"    Delivery validated for SO #{so.name}")
                except Exception as e:
                    logging.warning(f"    Delivery validation skipped: {e}")

        cr.commit()
        logging.info("Sales Orders committed.")

        # ============================================================
        # 5. INTERNAL TRANSFERS (visible recent)
        # ============================================================
        logging.info("=== Creating 4 Internal Transfers ===")
        internal_locations = env['stock.location'].search([('usage', '=', 'internal')], limit=3)
        if len(internal_locations) >= 2:
            picking_type = env['stock.picking.type'].search([('code', '=', 'internal')], limit=1)
            for i in range(4):
                prod = random.choice(products)
                picking = env['stock.picking'].create({
                    'picking_type_id': picking_type.id,
                    'location_id': internal_locations[0].id,
                    'location_dest_id': internal_locations[1].id,
                })
                move = env['stock.move'].create({
                    'name': f'Internal Transfer {i+1}',
                    'product_id': prod.id,
                    'product_uom_qty': random.randint(2, 8),
                    'product_uom': prod.uom_id.id,
                    'picking_id': picking.id,
                    'location_id': internal_locations[0].id,
                    'location_dest_id': internal_locations[1].id,
                })
                picking.action_confirm()
                for m in picking.move_ids:
                    m.quantity = m.product_uom_qty
                try:
                    picking.button_validate()
                    logging.info(f"  Internal Transfer #{picking.name} validated")
                except Exception as e:
                    logging.warning(f"  Transfer validation skipped: {e}")

        cr.commit()
        logging.info("Internal Transfers committed.")

        # ============================================================
        # 6. SCRAP ORDERS (visible recent)
        # ============================================================
        logging.info("=== Creating 4 Scrap Orders ===")
        stock_loc = env['stock.location'].search([('usage', '=', 'internal')], limit=1)
        scrap_loc = env['stock.location'].search([('scrap_location', '=', True)], limit=1)
        if stock_loc and scrap_loc:
            for i in range(4):
                prod = random.choice(products)
                scrap = env['stock.scrap'].create({
                    'product_id': prod.id,
                    'scrap_qty': random.randint(1, 2),
                    'product_uom_id': prod.uom_id.id,
                    'location_id': stock_loc.id,
                    'scrap_location_id': scrap_loc.id,
                })
                try:
                    scrap.do_scrap()
                    logging.info(f"  Scrap #{scrap.name} validated")
                except Exception as e:
                    logging.warning(f"  Scrap skipped: {e}")

        cr.commit()
        logging.info("Scrap Orders committed.")

        # ============================================================
        # 7. CUSTOMER REFUNDS (Credit Notes)
        # ============================================================
        logging.info("=== Creating 4 Customer Refunds ===")
        for i in range(4):
            refund_date = today - timedelta(days=random.randint(0, 15))
            prod = random.choice(products)
            refund = env['account.move'].create({
                'move_type': 'out_refund',
                'partner_id': random.choice(customers).id,
                'invoice_date': refund_date.strftime('%Y-%m-%d'),
                'invoice_line_ids': [(0, 0, {
                    'product_id': prod.id,
                    'quantity': 1,
                    'price_unit': prod.list_price or 50000,
                })]
            })
            refund.action_post()
            logging.info(f"  Refund #{refund.name} posted ({refund_date.strftime('%Y-%m-%d')})")

        cr.commit()
        logging.info("Customer Refunds committed.")

        # ============================================================
        # DONE
        # ============================================================
        logging.info("")
        logging.info("=" * 50)
        logging.info("ALL EXTRA TRANSACTIONS GENERATED SUCCESSFULLY!")
        logging.info("=" * 50)


if __name__ == "__main__":
    generate_odoo_visible_transactions()
