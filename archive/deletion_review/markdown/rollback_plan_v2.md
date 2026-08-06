# Rollback & Recovery Plan V2 — Phase 11.2 Revision

**Date:** August 4, 2026  
**Status:** **REVISED ROLLBACK SPECIFICATION APPROVED**  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. Revised Rollback Protocols (ORM & XML Safe)

### Protocol 1: Revert Custom Addon XML Changes via ORM
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
    print('Uninstalled obidss_operational_bi cleanly via ORM!')
"
```

### Protocol 2: Full Database Restore from PostgreSQL Binary Dump
```powershell
dropdb -h localhost -p 5432 -U openpg Business_Intelegent_Project_v2
createdb -h localhost -p 5432 -U openpg -O openpg Business_Intelegent_Project_v2
pg_restore -h localhost -p 5432 -U openpg -d Business_Intelegent_Project_v2 -v "Business_Intelegent_Project_v2_backup.dump"
```
