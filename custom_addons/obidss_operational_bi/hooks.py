from odoo import api, SUPERUSER_ID
import json
import base64

def post_init_hook(env):
    """
    Initialize custom dashboards with valid empty spreadsheet data.
    If spreadsheet_binary_data is empty or invalid, the UI crashes.
    This ensures they are editable natively via the Dashboards app.
    """
    data = env['spreadsheet.dashboard']._empty_spreadsheet_data()
    data_str = json.dumps(data)
    encoded_data = base64.b64encode(data_str.encode('utf-8'))
    
    dashboard_xml_ids = [
        'obidss_operational_bi.dashboard_executive',
        'obidss_operational_bi.dashboard_sales',
        'obidss_operational_bi.dashboard_purchase',
        'obidss_operational_bi.dashboard_inventory',
        'obidss_operational_bi.dashboard_data_quality',
        'obidss_operational_bi.dashboard_finance'
    ]
    
    for xml_id in dashboard_xml_ids:
        dashboard = env.ref(xml_id, raise_if_not_found=False)
        # Only initialize if it has no data
        if dashboard and not dashboard.spreadsheet_binary_data:
            dashboard.write({'spreadsheet_binary_data': encoded_data})
