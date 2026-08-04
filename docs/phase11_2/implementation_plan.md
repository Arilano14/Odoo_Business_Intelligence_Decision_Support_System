# Detailed Technical Implementation Plan — Phase 11.2

**Date:** August 4, 2026  
**Status:** **STAGE 1 READ-ONLY AUDIT COMPLETE — AWAITING USER APPROVAL**  
**Author:** Senior Odoo Technical Consultant & Data Architect  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)  
**Target Database:** `Business_Intelegent_Project_v2` (PostgreSQL)  
**Target Addon:** `custom_addons/obidss_operational_bi/`

---

## 1. Executive Summary & Strategy Overview

Phase 11.2 consolidates the Odoo 18 dashboard layer for **PT Prima Alat Nusantara (Company ID: 2, FY 2026)**. Based on the read-only environment, menu, and data source audit, the standalone `OBIDSS` launcher icon will be consolidated into the host `Dashboards` application (`spreadsheet_dashboard_menu_root`), and all operational dashboards will open live Graph/Pivot/List views connected directly to the 740 Sales Orders, 251 Purchase Orders, 283 Product Variants, 24 Transfers, and 12 Scraps of PT Prima Alat Nusantara.

---

## 2. File & Record Level Task Breakdown

### TASK 11.2.1: Reparent OBIDSS Dashboards under `Dashboards` Application Menu

| Field | Content / Specification |
|---|---|
| **Task ID** | `TASK-11.2.1` |
| **Objective** | Remove standalone top-level `OBIDSS` app icon and place all OBIDSS operational dashboards inside the host `Dashboards` application. |
| **Current evidence** | Audit query shows `OBIDSS` (ID 377) at top-level launcher (`parent_id = NULL`). |
| **Root cause** | OBIDSS menu was created as top-level `menuitem` without parent pointer. |
| **Strategy** | Reparenting under `spreadsheet_dashboard.spreadsheet_dashboard_menu_root` (ID 177). |
| **Possible** | Yes |
| **Exact files** | `custom_addons/obidss_operational_bi/views/menu_restructure.xml` |
| **Exact records** | `ir.ui.menu` ID 377 (`obidss_operational_bi.menu_obidss_root`), Parent ID 177 |
| **Exact change** | Update `parent_id` of `menu_obidss_root` to `spreadsheet_dashboard.spreadsheet_dashboard_menu_root`. |
| **Technical method** | XML Data record update (`<record id="menu_obidss_root" model="ir.ui.menu">`). |
| **Dependencies** | Module manifest update. |
| **Test** | SQL Query `SELECT parent_id FROM ir_ui_menu WHERE id = 377` returns `177`. |
| **Browser proof** | App launcher screenshot showing `OBIDSS` icon removed; `Dashboards` sidebar showing `OBIDSS` section. |
| **Rollback** | Reset `parent_id = NULL` on menu ID 377. |
| **Risk** | Low |
| **Destructive** | No |
| **Approval** | Required |

---

### TASK 11.2.2: Restrict Irrelevant Applications for Operational Users

| Field | Content / Specification |
|---|---|
| **Task ID** | `TASK-11.2.2` |
| **Objective** | Hide `Discuss`, `Email Marketing`, `Surveys`, `Employees` from operational users via security groups without uninstalling modules. |
| **Current evidence** | Audit shows `Discuss` (ID 82), `Email Marketing` (ID 338), `Surveys` (ID 312), `Employees` (ID 319) open to all users. |
| **Root cause** | Standard module menu items lack restrictive `groups_id`. |
| **Strategy** | Role-based menu access restriction using `group_obidss_admin` / `base.group_system`. |
| **Possible** | Yes |
| **Exact files** | `custom_addons/obidss_operational_bi/views/menu_restructure.xml` |
| **Exact records** | `ir.ui.menu` IDs 82, 338, 312, 319 |
| **Exact change** | Add `<menuitem id="..." menu_xml_id="..." groups="base.group_system"/>`. |
| **Technical method** | XML `eval` write on `groups_id` field of target menu XML IDs. |
| **Dependencies** | `TASK-11.2.1` |
| **Test** | Log in as `group_obidss_user`; verify `Discuss`, `Mass Mailing`, `Survey`, `HR` icons are invisible. |
| **Browser proof** | App launcher screenshot showing clean launcher for operational users. |
| **Rollback** | Remove `groups` attribute from menu records. |
| **Risk** | Low |
| **Destructive** | No |
| **Approval** | Required |

---

### TASK 11.2.3: Link Operational Submenus to Live Odoo Graph/Pivot/List Views

| Field | Content / Specification |
|---|---|
| **Task ID** | `TASK-11.2.3` |
| **Objective** | Link Sales, Purchase, Inventory, Finance, & Data Quality submenus to live Odoo models (`sale.order`, `purchase.order`, `stock.quant`, `account.move`, `obidss.data.quality`). |
| **Current evidence** | Audit query confirms window actions exist for `sale.order` (ID 446), `purchase.order` (ID 413), `stock.quant` (ID 349), `account.move` (ID 261). |
| **Root cause** | Submenus need explicit window action links to display live database transactions. |
| **Strategy** | Direct Action Binding in XML (`action="sale.action_orders"` etc.). |
| **Possible** | Yes |
| **Exact files** | `custom_addons/obidss_operational_bi/views/obidss_menus.xml` |
| **Exact records** | `ir.ui.menu` IDs 378, 379, 380, 381, 382, 383, 384 |
| **Exact change** | Update `action` field on all 7 OBIDSS submenus to target live Window/Client Actions. |
| **Technical method** | XML `<menuitem id="..." action="..." />`. |
| **Dependencies** | `TASK-11.2.1` |
| **Test** | Click `Sales Operations` -> opens 740 SOs; Click `Purchase & Suppliers` -> opens 251 POs. |
| **Browser proof** | Screenshots of Sales, Purchase, Inventory live Graph/Pivot views. |
| **Rollback** | Reset `action` values on target menus. |
| **Risk** | Low |
| **Destructive** | No |
| **Approval** | Required |

---

### TASK 11.2.4: Module Update Rehearsal on Isolated Clone DB

| Field | Content / Specification |
|---|---|
| **Task ID** | `TASK-11.2.4` |
| **Objective** | Perform CLI module update rehearsal on clone database `Business_Intelegent_Project_v2_clone` to verify zero errors before primary execution. |
| **Current evidence** | Clone DB exists and is restored from production dump. |
| **Root cause** | Mandatory safety gate prior to production execution. |
| **Strategy** | Isolated CLI execution with `--stop-after-init --no-http`. |
| **Possible** | Yes |
| **Exact files** | `docs/phase11_2/upgrade_rehearsal.log` |
| **Exact records** | All XML IDs in `obidss_operational_bi` |
| **Exact change** | Execute module upgrade CLI command on clone DB. |
| **Technical method** | `odoo-bin -c odoo.conf -d Business_Intelegent_Project_v2_clone -u obidss_operational_bi --stop-after-init --no-http`. |
| **Dependencies** | `TASK-11.2.1`, `TASK-11.2.2`, `TASK-11.2.3` |
| **Test** | Check `upgrade_rehearsal.log` for 0 Errors and Exit Code 0. |
| **Browser proof** | N/A (CLI log verification). |
| **Rollback** | N/A (Clone DB). |
| **Risk** | Low |
| **Destructive** | No |
| **Approval** | Required |

---

### TASK 11.2.5: Primary Database Execution & Verification

| Field | Content / Specification |
|---|---|
| **Task ID** | `TASK-11.2.5` |
| **Objective** | Execute module update on primary database `Business_Intelegent_Project_v2` and verify browser UI. |
| **Current evidence** | Database `Business_Intelegent_Project_v2` running on port 8069. |
| **Root cause** | Primary execution stage post-user approval. |
| **Strategy** | XML-RPC ORM `button_immediate_upgrade` on `ir.module.module`. |
| **Possible** | Yes |
| **Exact files** | All custom addon files in `custom_addons/obidss_operational_bi/` |
| **Exact records** | `ir.module.module` record for `obidss_operational_bi` |
| **Exact change** | Upgrade custom addon on primary database. |
| **Technical method** | XML-RPC ORM call `button_immediate_upgrade`. |
| **Dependencies** | `TASK-11.2.4` |
| **Test** | All 10 UI tests in `ui_test_plan.md` pass; 0 critical browser console errors. |
| **Browser proof** | 10 required screenshots in `ui_test_plan.md`. |
| **Rollback** | Restore DB from `Business_Intelegent_Project_v2_phase11_2.dump`. |
| **Risk** | Medium |
| **Destructive** | No |
| **Approval** | Required |
