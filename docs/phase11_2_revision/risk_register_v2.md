# Risk Register V2 — Phase 11.2 Revision

**Date:** August 4, 2026  
**Status:** **REVISED RISK ASSESSMENT APPROVED**  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. Revised Risk Assessment & Mitigation Matrix

| Risk ID | Risk Event | Probability | Severity | Severity Score | Impact Analysis | Mitigation Strategy | Contingency Plan |
|---|---|---|---|---|---|---|---|
| **RSK-01** | Manual SQL `UPDATE parent_path` breaks Odoo menu hierarchy | Low | High | **Medium** | Direct SQL updates skip ORM triggers, corrupting tree calculation. | **DELETED RAW SQL PROPOSAL**. Allow Odoo ORM / XML data loading to compute hierarchy natively. | Execute ORM `env['ir.ui.menu']._parent_store_compute()`. |
| **RSK-02** | Moving `ir.ui.menu` under `Dashboards` fails to create sidebar item | Medium | Medium | **Medium** | Menu appears in upper bar but not in Dashboard OWL sidebar. | Register `spreadsheet.dashboard.group` and `spreadsheet.dashboard` records in custom addon XML data. | Bind menu to native Graph/Pivot client action. |
| **RSK-03** | Standard dashboards showing sample mock items | Low | Medium | **Low** | Users get confused by "GlideSync Mouse". | Restrict standard sample dashboards to `base.group_system` (Admin Only). | Restore official core sample JSON files. |
| **RSK-04** | Odoo demo data modal triggered by user click | Low | Medium | **Low** | Risk of irreversibly loading demo data. | Never click "Yes, I understand the risks"; use native live models (`sale.order`, `purchase.order`). | Revert database to backup dump. |
