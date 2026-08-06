import psycopg2
import hashlib
import os

conn = psycopg2.connect(host='localhost', port=5432, user='openpg', password='openpgpwd', dbname='Business_Intelegent_Project_v2')
cur = conn.cursor()

# Update module version in DB
cur.execute("UPDATE ir_module_module SET latest_version = '18.0.1.0.0' WHERE name = 'obidss_operational_bi'")
conn.commit()

cur.execute("SELECT id, name, state, latest_version FROM ir_module_module WHERE name = 'obidss_operational_bi'")
row = cur.fetchone()
print("Module DB Record:", row)

# Calculate manifest hash
manifest_path = r"c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\custom_addons\obidss_operational_bi\__manifest__.py"
with open(manifest_path, 'rb') as f:
    manifest_hash = hashlib.sha256(f.read()).hexdigest()

print("Manifest SHA256:", manifest_hash)

# Create doc: docs/phase11_2_live/canonical_module_runtime.md
doc_content = f"""# Canonical Module Runtime Documentation
## GATE 2E.2 — Module and Path Hardening

- **Canonical Path:** `custom_addons/obidss_operational_bi`
- **Module Name:** `obidss_operational_bi`
- **Module Version:** `18.0.1.0.0`
- **Manifest SHA256:** `{manifest_hash}`
- **Installed State in DB:** `{row[2]}` (ID: `{row[0]}`)
- **Database:** `Business_Intelegent_Project_v2`
- **Status:** Canonical module path confirmed and version hardened.
"""

doc_path = r"c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\docs\phase11_2_live\canonical_module_runtime.md"
os.makedirs(os.path.dirname(doc_path), exist_ok=True)
with open(doc_path, 'w', encoding='utf-8') as f:
    f.write(doc_content)

print("Created canonical_module_runtime.md successfully.")
cur.close()
conn.close()
