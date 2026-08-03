# Expanded Risk Register & Rollback Procedures — Phase 11.0 v2

**Date:** August 3, 2026  
**Project:** Odoo Business Intelligence Decision Support System (OBIDSS)

---

## Risk Matrix

| Risk ID | Risk Description | Probability | Impact | Detection Method | Prevention Strategy | Rollback Trigger | Rollback Procedure |
|---|---|---|---|---|---|---|---|
| **R-01** | Missing or Orphaned Attachment | Low | High | `ir_attachment` SQL count audit | Audit `res_model` links before upgrade | `spreadsheet_data` remains 0 Bytes | Restore DB snapshot dump |
| **R-02** | Module Data Marked `noupdate=True` | Low | Medium | Audit `ir_model_data` table | Checked `noupdate` flag; confirmed `False` | Module upgrade skips record | Use ORM attachment update script |
| **R-03** | Module Update Overwrites Custom Records | Low | Medium | Compare `create_uid` and XML ID | Rehearse on clone DB first | Custom layout lost | Restore clone DB filestore & DB |
| **R-04** | Clone Filestore Mismatch | Low | High | SHA1 Checksum comparison | Copy filestore synchronously with DB dump | File missing error | Re-sync filestore directory |
| **R-05** | Missing Purchase Dashboard Module | High | Low | Check `ir_module_module` state | Design custom `OBIDSS Purchase Operations` dashboard | Purchase UI menu missing | Build custom Odoo Spreadsheet view |
| **R-06** | Stale Browser Assets / Cache | Medium | Low | Inspection of QWeb HTTP responses | Clear Odoo asset cache via web client | Old JS asset error | Force browser hard reload (`Ctrl+F5`) |
| **R-07** | Power BI Stale Connection / 2024 Filters | Low | High | Execute Power BI Truth Query comparison | Audit Power Query M code | Revenue mismatch | Re-point connection string to `mart` schema |
