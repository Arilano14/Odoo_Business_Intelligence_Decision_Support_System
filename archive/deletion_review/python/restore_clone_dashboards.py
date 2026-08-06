import xmlrpc.client
import base64
import os

url = 'http://localhost:8069'
db = 'Business_Intelegent_Project_v2_clone'
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, 'admin', 'admin', {})
print('XML-RPC Auth on Clone DB, UID:', uid)

models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
dashboards = models.execute_kw(db, uid, 'admin', 'spreadsheet.dashboard', 'search_read', [[]], {'fields': ['id', 'name', 'sample_dashboard_file_path']})

base_addons = r'C:\Program Files\Odoo 18.0.20241229\server\odoo\addons'

for d in dashboards:
    d_id = d['id']
    d_name = d['name']
    rel_path = d.get('sample_dashboard_file_path')
    if rel_path:
        full_path = os.path.join(base_addons, rel_path)
        if os.path.exists(full_path):
            with open(full_path, 'rb') as f:
                content_bytes = f.read()
            b64_val = base64.b64encode(content_bytes).decode('utf-8')
            models.execute_kw(db, uid, 'admin', 'spreadsheet.dashboard', 'write', [[d_id], {'spreadsheet_binary_data': b64_val}])
            print(f"Successfully restored spreadsheet_binary_data for Dashboard ID {d_id} ({d_name}) from {rel_path}")

updated = models.execute_kw(db, uid, 'admin', 'spreadsheet.dashboard', 'search_read', [[]], {'fields': ['id', 'name', 'spreadsheet_data']})
print('\n--- Post-Restoration Verification on Clone DB ---')
for u in updated:
    raw = u.get('spreadsheet_data')
    d_id = u['id']
    d_name = u['name']
    has_data = bool(raw)
    data_len = len(raw) if raw else 0
    print(f"ID {d_id:2d} | Name: {str(d_name):<25} | Has Data: {str(has_data):<5} | Data Length: {data_len:6d} B")
