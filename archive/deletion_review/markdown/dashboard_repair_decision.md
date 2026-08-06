# Dashboard Repair Decision Tree — Phase 11.0

**Date:** August 3, 2026  
**Project:** Odoo Business Intelligence Decision Support System (OBIDSS)

---

## Decision Tree Cases

### Case A: Module update on clone restores valid data
- **Condition**: CLI module update on clone succeeds, `spreadsheet_data` computes to valid JSON (> 20 KB), `get_readonly_dashboard()` returns status 200, browser loads dashboard without RPC error.
- **Action**: Document before/after evidence; prepare controlled update on primary database.

### Case B: Module update runs but data remains empty
- **Condition**: CLI update completes without traceback, but `spreadsheet_data` remains empty string.
- **Action**: Inspect `noupdate` flags and `ir.attachment` linkages; do NOT re-run `-u`; prepare supported ORM binary attachment restoration script from sample JSON files on disk.

### Case C: Module update overwrites custom dashboard data
- **Condition**: Module update resets user-customized dashboard layouts back to default samples.
- **Action**: Stop immediately; restore clone from backup; separate standard records (IDs 1-4) from custom records; preserve custom records separately.

### Case D: Module update creates new records or duplicates
- **Condition**: Module update creates duplicate `spreadsheet.dashboard` records with new IDs instead of updating IDs 1-4.
- **Action**: Stop; reconcile XML IDs in `ir_model_data`; perform dependency analysis before any record cleanup.

### Case E: JSON becomes valid but dashboard has broken models or fields
- **Condition**: `spreadsheet_data` is valid JSON, but opening dashboard in UI displays missing model/field warnings.
- **Action**: Classify as dependency data-source error; inspect missing model/field references in sample JSON and ensure required Odoo modules are installed.

### Case F: Repair fails or introduces regressions
- **Condition**: Module update causes server traceback or registry load failure.
- **Action**: Rollback clone DB immediately; mark Phase 11.0 dashboard recovery as `BLOCKED`; preserve operational transactions.
