import os
import sys

sys.path.append(r"C:\Program Files\Odoo 18.0.20241229\server")
import odoo

def fix_dashboard():
    odoo.tools.config.parse_config(['-c', r'C:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo.conf', '-d', 'Business_Intelegent_Project_v2'])
    registry = odoo.modules.registry.Registry('Business_Intelegent_Project_v2')
    with registry.cursor() as cr:
        env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
        dashboards = env['spreadsheet.dashboard'].search([])
        for dash in dashboards:
            try:
                # Odoo 18 uses spreadsheet_data as text/jsonb
                if hasattr(dash, 'spreadsheet_data'):
                    data = dash.spreadsheet_data
                    if not data or data.strip() == '':
                        print(f"Fixing Dashboard {dash.id} ({dash.name})...")
                        dash.spreadsheet_data = '{}'
            except Exception as e:
                print(f"Failed to check/fix {dash.id}: {e}")
        cr.commit()
        print("Done fixing dashboards!")

if __name__ == "__main__":
    fix_dashboard()
