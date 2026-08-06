# Rollback & Recovery Plan — Phase 11.2

**Date:** August 4, 2026  
**Status:** **ROLLBACK SPECIFICATION APPROVED**  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. Rollback Scenarios & Emergency Action Protocols

### Scenario 1: Revert Menu Restructuring & Restore Top-Level OBIDSS App
```powershell
# Restore top-level OBIDSS menu root (ID 377)
.venv\Scripts\python.exe -c "
from config.database import db
from sqlalchemy import text
with db.source_engine.connect() as conn:
    conn.execute(text('UPDATE ir_ui_menu SET parent_id = NULL WHERE id = 377;'))
    conn.execute(text('UPDATE ir_ui_menu SET parent_path = id || \'/\' WHERE id = 377;'))
    conn.commit()
    print('Restored OBIDSS Root Menu parent_id = NULL!')
"
```

### Scenario 2: Restore Full Database Backup from PostgreSQL Dump
```powershell
# Drop and restore Business_Intelegent_Project_v2 from pre-phase backup
dropdb -h localhost -p 5432 -U openpg Business_Intelegent_Project_v2
createdb -h localhost -p 5432 -U openpg -O openpg Business_Intelegent_Project_v2
pg_restore -h localhost -p 5432 -U openpg -d Business_Intelegent_Project_v2 -v "Business_Intelegent_Project_v2_backup.dump"
```

### Scenario 3: Rollback Custom Addon `obidss_operational_bi`
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
    models.execute_kw(db, uid, 'admin', 'ir.module.module', 'button_immediate_uninstall', [[mods[0]['id']]])
    print('Uninstalled obidss_operational_bi addon successfully!')
"
```
