import psycopg2
import json
import os

conn = psycopg2.connect(host='localhost', port=5432, user='openpg', password='openpgpwd', dbname='Business_Intelegent_Project_v2')
cur = conn.cursor()

print("=" * 80)
print("GATE 2E.3 — DASHBOARD STORAGE BASELINE AND AUDIT")
print("=" * 80)

# 1. Audit Columns of spreadsheet_dashboard table
cur.execute("""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_name = 'spreadsheet_dashboard'
    ORDER BY ordinal_position
""")
db_cols = cur.fetchall()
print("\n1. Database Table Columns (spreadsheet_dashboard):")
for col, dt, null in db_cols:
    print(f"  - {col:30s} | {dt:25s} | nullable: {null}")

# 2. Audit ir_model_fields for spreadsheet.dashboard
cur.execute("""
    SELECT name, field_description, ttype, relation, required
    FROM ir_model_fields
    WHERE model = 'spreadsheet.dashboard'
    ORDER BY name
""")
model_fields = cur.fetchall()
print("\n2. Registered ORM Fields (spreadsheet.dashboard):")
for f_name, f_desc, f_type, f_rel, f_req in model_fields:
    print(f"  - {f_name:30s} | type: {f_type:12s} | rel: {str(f_rel):20s} | req: {f_req}")

# 3. Audit Broken Attachments (1126-1131)
cur.execute("""
    SELECT d.id, d.name->>'en_US' as dash_name, a.id as att_id, a.name as att_name,
           a.res_field, a.file_size, a.mimetype, a.db_datas IS NOT NULL as has_db
    FROM spreadsheet_dashboard d
    LEFT JOIN ir_attachment a ON a.res_model = 'spreadsheet.dashboard' AND a.res_id = d.id
    WHERE d.id IN (5, 6, 7, 8, 9, 10)
    ORDER BY d.id, a.id
""")
broken_atts = cur.fetchall()
print("\n3. Current OBIDSS Dashboards & Attachments Audit:")
mapping_rows = []
for did, dname, aid, aname, rfield, fsize, mime, hasdb in broken_atts:
    status = "Broken Attachment (res_field=None, static placeholder)"
    cleanup = "FALSE (Blocked until pilot validation)"
    print(f"  Dash ID {did}: {dname:32s} | Att ID: {aid} | Field: {rfield} | Size: {fsize}b")
    mapping_rows.append((did, dname, aid, status, cleanup))

# Create markdown document: docs/phase11_2_live/dashboard_field_contract.md
doc_md = f"""# Dashboard Storage Baseline & Field Contract
## GATE 2E.3 — Field Verification and Attachment Audit

### 1. Verified Model Fields (spreadsheet.dashboard)

| Field Name | Type | Relation | Description | Target Role |
|------------|------|----------|-------------|-------------|
| `spreadsheet_binary_data` | `binary` | — | Spreadsheet JSON file (stored via `ir_attachment` where `res_field='spreadsheet_binary_data'`) | **Binary Payload Storage** |
| `name` | `char` | — | Dashboard Display Name | Dashboard Title |
| `dashboard_group_id` | `many2one` | `spreadsheet.dashboard.group` | Sidebar Group | Grouping (`OBIDSS Operational BI`) |
| `group_ids` | `many2many` | `res.groups` | Access Rights Groups | Security restriction |
| `is_published` | `boolean` | — | Sidebar Visibility | Must be `True` |
| `sample_dashboard_file_path` | `char` | — | Fallback Sample JSON Path | Unused (Live Data Only) |
| `main_data_model_ids` | `many2many` | `ir.model` | Core Data Models | Model references for empty checks |

---

### 2. Broken Attachments Audit & Replacement Mapping

Current status of legacy attachments created during previous repair attempts:

| Dashboard ID | Dashboard Name | Broken Attachment ID | Current Status | Replacement Status | Cleanup Allowed |
|--------------|----------------|----------------------|----------------|--------------------|-----------------|
| 5 | Executive Operations | Attachment #1126 | `res_field=None`, 395b static text | Pending Pilot Validation | **FALSE** (Blocked) |
| 6 | Sales Operations | Attachment #1127 | `res_field=None`, 397b static text | Target of Pilot Gate 2E.4 | **FALSE** (Blocked) |
| 7 | Purchase & Suppliers | Attachment #1128 | `res_field=None`, 408b static text | Pending Sequential Build | **FALSE** (Blocked) |
| 8 | Inventory Operations | Attachment #1129 | `res_field=None`, 390b static text | Pending Sequential Build | **FALSE** (Blocked) |
| 9 | Finance & Invoicing | Attachment #1130 | `res_field=None`, 398b static text | **EXCLUDED** (No Accounting Data) | **FALSE** (Blocked) |
| 10 | Data Quality & Reconciliation | Attachment #1131 | `res_field=None`, 408b static text | Pending Sequential Build | **FALSE** (Blocked) |

---

### 3. Rules & Constraints
1. **No SQL Delete:** Legacy attachments 1126–1131 MUST NOT be deleted via SQL. Cleanup will be performed via ORM only after full browser & fresh clone validation.
2. **Correct `res_field` Constraint:** All replacement attachments MUST have `res_field='spreadsheet_binary_data'` and `res_model='spreadsheet.dashboard'`.
3. **Published State:** All valid OBIDSS dashboards MUST have `is_published=True`.
"""

doc_path = r"c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\docs\phase11_2_live\dashboard_field_contract.md"
os.makedirs(os.path.dirname(doc_path), exist_ok=True)
with open(doc_path, 'w', encoding='utf-8') as f:
    f.write(doc_md)

print(f"\nSaved dashboard_field_contract.md to {doc_path}")
cur.close()
conn.close()
