# Dashboard Storage Baseline & Field Contract
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
