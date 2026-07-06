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

if __name__ == "__main__":
    test_create()
