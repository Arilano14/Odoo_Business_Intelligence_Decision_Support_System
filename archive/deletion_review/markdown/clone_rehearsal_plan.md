# Clone Rehearsal Plan & Isolated Command Template — Phase 11.0

**Date:** August 3, 2026  
**Project:** Odoo Business Intelligence Decision Support System (OBIDSS)

---

## 1. 14-Step Rehearsal Protocol

1. **Verify PostgreSQL Primary DB Identity**: Confirm active DB is `Business_Intelegent_Project_v2`.
2. **Full Database & Filestore Backup**: Create PostgreSQL dump `Business_Intelegent_Project_v2_backup.dump`.
3. **Verify Backup Integrity**: Check non-zero file size and valid SQL dump header.
4. **Create Clone Database**: Restore dump into isolated test database `Business_Intelegent_Project_v2_clone`.
5. **Duplicate Filestore**: Copy filestore directory for clone database.
6. **Isolated Configuration Setup**: Configure dedicated port / isolated parameters for clone execution.
7. **Pre-Repair Baseline Tests on Clone**: Run ORM read test on clone to confirm starting state.
8. **Execute Isolated Module Update on Clone**: Run CLI module update command for the 3 target modules.
9. **Post-Repair ORM Tests on Clone**: Inspect `spreadsheet.dashboard` records and `spreadsheet_data` evaluation.
10. **RPC & API Tests on Clone**: Call `get_readonly_dashboard()` via XML-RPC.
11. **Browser UI Tests on Clone**: Open Odoo web client on clone and verify dashboard rendering.
12. **Compare Before/After Hashes**: Verify attachment SHA1 checksums and DB integrity.
13. **Safety Assessment**: Decide whether repair passed 100% of criteria without regressions.
14. **Request Separate User Approval**: Present clone rehearsal findings before applying to primary DB.

---

## 2. Isolated Module Update Command Template

```powershell
& "C:\Program Files\Odoo 18.0.20241229\python\python.exe" "C:\Program Files\Odoo 18.0.20241229\server\odoo-bin" `
  -c "c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo.conf" `
  -d "Business_Intelegent_Project_v2_clone" `
  -u "spreadsheet_dashboard_sale,spreadsheet_dashboard_account,spreadsheet_dashboard_stock_account" `
  --stop-after-init `
  --no-http `
  --logfile "c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\docs\phase11_0\clone_upgrade.log"
```

> [!CAUTION]
> **READ-ONLY NOTICE**: Command template di atas HANYA disiapkan untuk dieksekusi di Stage 2 pada database clone setelah user memberikan persetujuan eksplisit.
