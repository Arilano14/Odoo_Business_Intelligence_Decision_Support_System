# Current Menu Inventory Report — Phase 11.2

**Date:** August 4, 2026  
**Status:** **READ-ONLY AUDIT PASSED**  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. App Launcher Top-Level Menus Inventory

| Menu Name | Record ID | XML ID | Module Owner | Parent ID | Action | Children Count | Recommended Action |
|---|---:|---|---|---|---|---:|---|
| **Discuss** | 82 | `mail.menu_root_discuss` | `mail` | None | `ir.actions.client,120` | 2 | **HIDE FOR TARGET USERS** |
| **OBIDSS** | 377 | `obidss_operational_bi.menu_obidss_root` | `obidss_operational_bi` | None | None | 7 | **CONSOLIDATE INTO DASHBOARDS** |
| **Contacts** | 290 | `contacts.menu_contacts` | `contacts` | None | `ir.actions.act_window,486` | 2 | **RESTRICT TO MASTER DATA USERS** |
| **Sales** | 249 | `sale.sale_menu_root` | `sale` | None | `ir.actions.act_window,446` | 5 | **RETAIN OPERATIONAL** |
| **Dashboards** | 177 | `spreadsheet_dashboard.spreadsheet_dashboard_menu_root` | `spreadsheet_dashboard` | None | `ir.actions.client,309` | 2 | **RETAIN CORE DASHBOARD HOST** |
| **Invoicing** | 124 | `account.menu_finance` | `account` | None | `ir.actions.act_window,261` | 6 | **RESTRICT TO FINANCE USERS** |
| **Email Marketing** | 338 | `mass_mailing.mass_mailing_menu_root` | `mass_mailing` | None | `ir.actions.act_window,554` | 5 | **HIDE FOR TARGET USERS** |
| **Surveys** | 312 | `survey.menu_surveys` | `survey` | None | `ir.actions.act_window,519` | 3 | **HIDE FOR TARGET USERS** |
| **Purchase** | 229 | `purchase.menu_purchase_root` | `purchase` | None | `ir.actions.act_window,413` | 4 | **RETAIN OPERATIONAL** |
| **Inventory** | 181 | `stock.menu_stock_root` | `stock` | None | `ir.actions.act_window,349` | 5 | **RETAIN OPERATIONAL** |
| **Employees** | 319 | `hr.menu_hr_root` | `hr` | None | `ir.actions.act_window,528` | 7 | **HIDE FOR TARGET USERS** |
| **Apps** | 15 | `base.menu_management` | `base` | None | `ir.actions.act_window,15` | 4 | **RESTRICT TO ADMIN ONLY** |
| **Settings** | 1 | `base.menu_administration` | `base` | None | `ir.actions.act_window,1` | 7 | **RESTRICT TO ADMIN ONLY** |

---

## 2. Decision Rule Audit for Top-Level OBIDSS Application

* **Current Contents of OBIDSS**: Contains 7 submenus (`Executive Operations`, `Sales Operations`, `Purchase & Suppliers`, `Inventory Operations`, `Finance & Invoicing`, `Data Quality & Reconciliation`, `Configuration`). All submenus serve analytical reporting and monitoring functions.
* **Decision**: **MOVE OBIDSS INTO DASHBOARDS**.
  Reparent all OBIDSS operational dashboards directly inside the existing `Dashboards` application (`spreadsheet_dashboard_menu_root`), removing the redundant standalone `OBIDSS` icon from the top-level launcher.
