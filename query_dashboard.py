import sys
sys.path.append(r"C:\Program Files\Odoo 18.0.20241229\server")
import odoo
from odoo.tools import config

config.parse_config([
    '-c', r"c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\clone_odoo.conf",
    '-d', 'Business_Intelegent_Project_v2_fresh_clone',
    '--no-http'
])

odoo.cli.server.report_configuration()
odoo.service.server.start(preload=[], stop=True)

registry = odoo.registry('Business_Intelegent_Project_v2_fresh_clone')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # 1. Check spreadsheet_dashboard module
    module = env['ir.module.module'].search([('name', '=', 'spreadsheet_dashboard')])
    print(f"Spreadsheet Dashboard State: {module.state}")
    
    # 2. Look for Sales Operations dashboard
    sales_dashboards = env['spreadsheet.dashboard'].search([('name', '=', 'Sales Operations')])
    print(f"Sales Operations Dashboards Found: {len(sales_dashboards)}")
    for sd in sales_dashboards:
        print(f"ID: {sd.id}, XML ID: {sd.get_external_id().get(sd.id)}")
        print(f"Data Length: {len(sd.spreadsheet_binary_data or '')}")
        
    # 3. Look for the action for Dashboards
    action = env['ir.actions.client'].search([('tag', 'ilike', 'spreadsheet')], limit=5)
    for act in action:
        print(f"Action ID: {act.id}, Tag: {act.tag}, XML ID: {act.get_external_id().get(act.id)}")
        
    # Also find spreadsheet_dashboard action in act_window just in case
    action_w = env['ir.actions.act_window'].search([('res_model', 'ilike', 'spreadsheet')], limit=5)
    for act in action_w:
        print(f"Window Action ID: {act.id}, Model: {act.res_model}, XML ID: {act.get_external_id().get(act.id)}")
