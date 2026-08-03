# Comprehensive Rollback Plan — Phase 11.0 v2

**Date:** August 3, 2026  
**Project:** Odoo Business Intelligence Decision Support System (OBIDSS)

---

## 1. Trigger Conditions for Immediate Rollback

1. Any CLI command error during module update on clone or primary database.
2. `spreadsheet_data` evaluation failure or `JSONDecodeError` persisting after rehearsal.
3. Loss or corruption of transactional records in `public` schema (`sale_order`, `purchase_order`, `stock_move`).
4. Regression in ETL pipeline execution or `validate_phase10.py` failure (score $< 15/15$).

---

## 2. Emergency Recovery Steps

```powershell
# 1. Stop Odoo Service
Stop-Service odoo-server-18.0

# 2. Drop and Restore PostgreSQL Primary Database
dropdb -U openpg -h localhost Business_Intelegent_Project_v2
createdb -U openpg -h localhost Business_Intelegent_Project_v2
pg_restore -U openpg -h localhost -d Business_Intelegent_Project_v2 "c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\docs\phase11_0\Business_Intelegent_Project_v2_backup.dump"

# 3. Restore Filestore Directory
Copy-Item -Recurse -Force "c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo_data_backup\*" "c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo_data\"

# 4. Restart Odoo Service & Re-verify
Start-Service odoo-server-18.0
.venv\Scripts\python.exe validation/validate_phase10.py
```
