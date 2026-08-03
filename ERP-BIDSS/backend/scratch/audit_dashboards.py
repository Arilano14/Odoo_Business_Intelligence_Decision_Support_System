import sys
import os
import json
import base64

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from odoo.connection import get_connection

uid, models, odoo_db, password = get_connection()
print("Odoo XML-RPC Auth OK, UID:", uid)

fields_info = models.execute_kw(odoo_db, uid, password, 'spreadsheet.dashboard', 'fields_get', [], {'attributes': ['type', 'string']})
print("\n--- Available Fields in spreadsheet.dashboard ---")
for f_name in sorted(fields_info.keys()):
    print(f"  {f_name:<30}: {fields_info[f_name]['type']} ({fields_info[f_name].get('string')})")

dashboards = models.execute_kw(
    odoo_db, uid, password,
    'spreadsheet.dashboard',
    'search_read',
    [[]],
    {'fields': ['id', 'name', 'dashboard_group_id', 'is_published', 'spreadsheet_data', 'sample_dashboard_file_path']}
)

print(f"\n--- Found {len(dashboards)} Dashboard Records ---")
for d in dashboards:
    d_id = d['id']
    d_name = d['name']
    group = d['dashboard_group_id']
    pub = d['is_published']
    sample_path = d.get('sample_dashboard_file_path')
    
    # spreadsheet_data is binary (base64 encoded JSON in Odoo ORM)
    raw_b64 = d.get('spreadsheet_data')
    
    data_len = 0
    is_empty = True
    json_valid = False
    json_err = None
    
    if raw_b64:
        try:
            if isinstance(raw_b64, str):
                decoded_bytes = base64.b64decode(raw_b64)
            else:
                decoded_bytes = base64.b64decode(raw_b64.data)
            
            data_len = len(decoded_bytes)
            is_empty = not bool(decoded_bytes.strip())
            
            if not is_empty:
                try:
                    parsed_json = json.loads(decoded_bytes.decode('utf-8'))
                    json_valid = True
                except Exception as e:
                    json_err = str(e)
        except Exception as b64_err:
            json_err = f"Base64 Decode Error: {b64_err}"
            
    status_str = "VALID_JSON" if json_valid else ("EMPTY_DATA" if is_empty else f"MALFORMED ({json_err})")
    
    print(f"ID {d_id:2d} | Name: {str(d_name):<30} | Group: {str(group):<25} | Pub: {str(pub):<5} | Data Size: {data_len:6d} B | Status: {status_str}")
    if sample_path:
        print(f"      -> Sample Path: {sample_path}")
