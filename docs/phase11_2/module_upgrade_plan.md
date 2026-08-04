# Module Upgrade & Rehearsal Plan — Phase 11.2

**Date:** August 4, 2026  
**Status:** **REHEARSAL PLAN APPROVED**  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. Rehearsal Environment Specifications

* **Isolated Rehearsal Database**: `Business_Intelegent_Project_v2_clone`
* **Primary Target Database**: `Business_Intelegent_Project_v2`
* **Odoo Python Executable**: `C:\Program Files\Odoo 18.0.20241229\python\python.exe`
* **Odoo Binary**: `C:\Program Files\Odoo 18.0.20241229\server\odoo-bin`
* **Configuration File**: `c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo.conf`
* **Logfile Target**: `docs/phase11_2/upgrade_rehearsal.log`

---

## 2. Sequential Execution Workflow

### Step 1: Backup & Clone Database Verification
```powershell
pg_dump -h localhost -p 5432 -U openpg -F c -b -v -f "Business_Intelegent_Project_v2_phase11_2.dump" Business_Intelegent_Project_v2
```

### Step 2: Isolated Rehearsal Command on Clone DB
```powershell
& "C:\Program Files\Odoo 18.0.20241229\python\python.exe" "C:\Program Files\Odoo 18.0.20241229\server\odoo-bin" `
  -c "c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo.conf" `
  -d "Business_Intelegent_Project_v2_clone" `
  -u "obidss_operational_bi" `
  --stop-after-init `
  --no-http `
  --logfile "c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\docs\phase11_2\upgrade_rehearsal.log"
```

### Step 3: Primary Database Module Upgrade (Post-Approval)
```powershell
.venv\Scripts\python.exe -c "
import xmlrpc.client
url = 'http://localhost:8069'
db = 'Business_Intelegent_Project_v2'
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, 'admin', 'admin', {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
mods = models.execute_kw(db, uid, 'admin', 'ir.module.module', 'search_read', [[['name', '=', 'obidss_operational_bi']]], {'fields': ['id']})
if mods:
    models.execute_kw(db, uid, 'admin', 'ir.module.module', 'button_immediate_upgrade', [[mods[0]['id']]])
"
```

---

## 3. Post-Upgrade Verification Checklist

1. **CLI Exit Code**: Must return `0` (clean execution).
2. **Logfile Audit**: Zero `ERROR` or `CRITICAL` lines in `upgrade_rehearsal.log`.
3. **Module State**: `SELECT state FROM ir_module_module WHERE name='obidss_operational_bi'` must return `'installed'`.
4. **Parent Path Integrity**: `parent_path` on `ir_ui_menu` must be populated (`id || '/'`).
5. **HTTP Web Response**: `http://localhost:8069` must return `200 OK`.
