# Rollback Plan — Phase 11.1

**Date:** August 3, 2026  
**Project:** Odoo Business Intelligence Decision Support System (OBIDSS)

---

## Emergency Rollback Procedures

```powershell
# 1. Uninstall obidss_operational_bi addon if needed
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
"
```
