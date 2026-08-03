import sys
import os
import json
import base64

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from odoo.connection import get_connection

print("============================================================")
print("RESTORING OFFICIAL ODOO CORE SPREADSHEET DASHBOARD JSONs")
print("============================================================")

uid, models, odoo_db, password = get_connection()

addons_dir = r"C:\Program Files\Odoo 18.0.20241229\server\odoo\addons"

files_map = {
    1: os.path.join(addons_dir, "spreadsheet_dashboard_account", "data", "files", "invoicing_sample_dashboard.json"),
    2: os.path.join(addons_dir, "spreadsheet_dashboard_stock", "data", "files", "warehouse_metrics_sample_dashboard.json"),
    3: os.path.join(addons_dir, "spreadsheet_dashboard_sale", "data", "files", "sales_sample_dashboard.json"),
    4: os.path.join(addons_dir, "spreadsheet_dashboard_sale", "data", "files", "product_sample_dashboard.json"),
}

for dash_id, fpath in files_map.items():
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
            b64_val = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            models.execute_kw(odoo_db, uid, password, 'spreadsheet.dashboard', 'write', [[dash_id], {'spreadsheet_binary_data': b64_val}])
            print(f"Restored Dashboard ID {dash_id} from {os.path.basename(fpath)} (Size: {len(content)} Bytes)")
    else:
        print(f"File NOT found for ID {dash_id}: {fpath}")

print("OFFICIAL CORE DASHBOARDS RESTORED SUCCESSFULLY!")
