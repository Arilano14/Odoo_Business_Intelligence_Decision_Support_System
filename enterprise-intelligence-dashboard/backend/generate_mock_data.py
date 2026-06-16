import sys
import os
import random
from datetime import datetime, timedelta

# Append Odoo path so we can import it
sys.path.append(r"C:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo")
import odoo

# Initialize Odoo
odoo.tools.config.parse_config(['-c', r'C:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo.conf'])
registry = odoo.registry('Business_Intelegent_Project')

def generate_mock_data():
    with registry.cursor() as cr:
        env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
        
        print("Installing required modules...")
        modules_to_install = ['sale_management', 'stock', 'purchase', 'account', 'crm', 'contacts', 'hr']
        modules = env['ir.module.module'].search([('name', 'in', modules_to_install), ('state', '!=', 'installed')])
        if modules:
            modules.button_immediate_install()
            print("Modules installed. Please restart the script to apply changes.")
            return
            
        print("Generating mock data for 12 months...")
        
        # Ensure some partners exist
        partners = env['res.partner'].search([('customer_rank', '>', 0)], limit=10)
        if not partners:
            for i in range(10):
                partners += env['res.partner'].create({'name': f'Mock Customer {i}'})
                
        # Ensure some products exist
        products = env['product.product'].search([('sale_ok', '=', True)], limit=5)
        if not products:
            for i in range(5):
                products += env['product.product'].create({'name': f'Mock Product {i}', 'list_price': random.randint(100, 1000)})
                
        # Generate Sales for the last 365 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        for i in range(100): # Create 100 random sales orders
            order_date = start_date + timedelta(days=random.randint(0, 365))
            partner = random.choice(partners)
            
            order = env['sale.order'].create({
                'partner_id': partner.id,
                'date_order': order_date.strftime('%Y-%m-%d %H:%M:%S'),
                'state': 'sale'
            })
            
            for j in range(random.randint(1, 3)):
                product = random.choice(products)
                env['sale.order.line'].create({
                    'order_id': order.id,
                    'product_id': product.id,
                    'product_uom_qty': random.randint(1, 10),
                    'price_unit': product.list_price
                })
        
        # Generate CRM Leads
        for i in range(50):
            create_date = start_date + timedelta(days=random.randint(0, 365))
            env['crm.lead'].create({
                'name': f'Opportunity {i}',
                'expected_revenue': random.randint(1000, 50000),
                'probability': random.randint(10, 90),
                'create_date': create_date.strftime('%Y-%m-%d %H:%M:%S')
            })
            
        print("Mock data generated successfully!")

if __name__ == "__main__":
    generate_mock_data()
