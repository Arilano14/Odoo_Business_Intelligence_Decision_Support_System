# Risk Register — Phase 11.2

**Date:** August 4, 2026  
**Status:** **RISK ASSESSMENT APPROVED**  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. Risk Evaluation & Mitigation Matrix

| Risk ID | Risk Event / Vulnerability | Probability | Severity | Severity Score | Impact Analysis | Mitigation Strategy | Contingency Plan |
|---|---|---|---|---|---|---|---|
| **RSK-01** | `parent_path` NULL on `ir_ui_menu` causing 500 Error | Low | High | **Medium** | Odoo web client crashes during menu load (`load_menus()`). | Enforce automatic `parent_path` computation in XML & Python data loading. | Execute SQL `UPDATE ir_ui_menu SET parent_path = parent_id || '/' || id || '/'`. |
| **RSK-02** | Menu reparenting breaks administrative settings access | Low | Medium | **Low** | Admins lose access to `Settings` or `Apps`. | Retain `base.group_system` access to `Apps` (ID 15) & `Settings` (ID 1). | Restore admin XML IDs via `ir_model_data`. |
| **RSK-03** | Standard dashboards showing sample mock data | Low | Medium | **Low** | Users get confused by "GlideSync Mouse" or "TitanForge Chair". | Reparent OBIDSS dashboards to live Graph/Pivot views; hide standard sample dashboards. | Restore core sample JSON files. |
| **RSK-04** | Odoo demo data modal triggered by user click | Low | Medium | **Low** | Risk of irreversibly loading demo data. | Never click "Yes, I understand the risks"; use native live models. | Revert database to `Business_Intelegent_Project_v2.dump`. |
| **RSK-05** | RPC or XML-RPC timeout during module upgrade | Low | Low | **Low** | Module upgrade halts midway. | Use isolated CLI upgrade with `--stop-after-init --no-http`. | Re-run upgrade command on clone DB first. |
