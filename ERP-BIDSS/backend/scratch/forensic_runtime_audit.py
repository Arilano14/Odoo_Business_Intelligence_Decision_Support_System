import sys
import os
import json
import urllib.request
import urllib.parse
import psycopg2

print("============================================================")
print("PHASE 11.2 STAGE 2C — FORENSIC RUNTIME & UI AUDIT")
print("============================================================")

primary_db = "Business_Intelegent_Project_v2"
conn_params = {
    "host": "localhost",
    "port": 5432,
    "user": "openpg",
    "password": "openpgpwd",
    "dbname": primary_db
}

# 1. Gate 2C.1 & 2C.2: Web Session & Active Configuration Audit
url = "http://localhost:8069/web/session/get_session_info"
req = urllib.request.Request(url, headers={"Content-Type": "application/json"}, data=json.dumps({"jsonrpc": "2.0", "method": "call", "params": {}}).encode())

try:
    with urllib.request.urlopen(req) as resp:
        res_data = json.loads(resp.read().decode())
        result = res_data.get("result", {})
        db_name = result.get("db")
        server_version = result.get("server_version")
        user_context = result.get("user_context", {})
        company_id = user_context.get("allowed_company_ids", [])
        print(f"1. RUNNING WEB SESSION IDENTITY:")
        print(f"   Database Name : {db_name}")
        print(f"   Server Version: {server_version}")
        print(f"   User ID       : {result.get('uid')}")
        print(f"   User Name     : {result.get('name')}")
        print(f"   Allowed Comps : {company_id}")
except Exception as e:
    print("Web Session Error:", e)

# 2. Gate 2C.3: Addon Copies Audit
paths_to_check = [
    r"c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\custom_addons\obidss_operational_bi",
    r"c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo\addons\obidss_operational_bi",
    r"C:\Program Files\Odoo 18.0.20241229\server\odoo\addons\obidss_operational_bi"
]

print("\n2. ADDON COPIES AUDIT:")
for p in paths_to_check:
    exists = os.path.exists(p)
    manifest_p = os.path.join(p, "__manifest__.py") if exists else None
    has_manifest = os.path.exists(manifest_p) if manifest_p else False
    groups_p = os.path.join(p, "data", "dashboard_groups.xml") if exists else None
    has_groups = os.path.exists(groups_p) if groups_p else False
    print(f"   Path: {p}")
    print(f"     Exists: {exists} | Manifest: {has_manifest} | Dashboard Groups XML: {has_groups}")

# 3. Gate 2C.5, 2C.6, 2C.7: Database Dashboard & Attachment Inspection
conn = psycopg2.connect(**conn_params)
cursor = conn.cursor()

cursor.execute("""
    SELECT d.id, d.name->>'en_US', d.dashboard_group_id, g.name->>'en_US', 
           d.spreadsheet_binary_data IS NOT NULL as has_data,
           LENGTH(COALESCE(d.spreadsheet_binary_data, '')) as data_len
    FROM spreadsheet_dashboard d
    LEFT JOIN spreadsheet_dashboard_group g ON d.dashboard_group_id = g.id
    ORDER BY d.id
""")
dashes = cursor.fetchall()
print(f"\n3. PRIMARY DB DASHBOARD RECORDS (Total: {len(dashes)}):")
for d in dashes:
    print(f"   Dash ID: {d[0]:2d} | Name: {d[1]:30s} | Group: {str(d[3]):25s} | Has Binary: {d[4]} | Length: {d[5]}")

cursor.execute("""
    SELECT id, name->>'en_US', sequence FROM spreadsheet_dashboard_group ORDER BY sequence
""")
groups = cursor.fetchall()
print(f"\n4. PRIMARY DB DASHBOARD GROUPS (Total: {len(groups)}):")
for g in groups:
    print(f"   Group ID: {g[0]:2d} | Name: {g[1]:30s} | Seq: {g[2]}")

# 5. Check ir.attachment linked to spreadsheet.dashboard
cursor.execute("""
    SELECT id, name, res_model, res_id, file_size, checksum
    FROM ir_attachment
    WHERE res_model = 'spreadsheet.dashboard'
""")
attachments = cursor.fetchall()
print(f"\n5. SPREADSHEET ATTACHMENTS (Total: {len(attachments)}):")
for a in attachments:
    print(f"   Attach ID: {a[0]:2d} | Name: {a[1]:30s} | Res ID: {a[3]} | Size: {a[4]} bytes")

cursor.close()
conn.close()
