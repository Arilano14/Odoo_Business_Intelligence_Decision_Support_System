# Detailed Technical Implementation Plan V2 — Phase 11.2 Revision

**Date:** August 4, 2026  
**Status:** **STAGE 1 READ-ONLY REVISION COMPLETE — AWAITING STAGE 2 APPROVAL**  
**Author:** Senior Odoo Solution Architect & Data Architect  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)  
**Target Database:** `Business_Intelegent_Project_v2` (PostgreSQL)  
**Target Addon Path:** `custom_addons/obidss_operational_bi/`

---

## 1. Executive Summary & Strategy Revision Overview

Phase 11.2 Revision incorporates all empirical data findings and fixes structural flaws identified in the preliminary plan:
1. **Dataset Discrepancies Resolved**: Database totals are verified as **740 Sales Orders** (677 confirmed, 33 drafts, 29 cancelled, 1 sent) totaling Rp 17.55B, **251 Purchase Orders** (225 confirmed, 16 drafts, 9 cancelled, 1 sent) totaling Rp 30.08B, and **283 Product Variants** (spanning 277 templates, of which 96 belong specifically to the heavy equipment & consumables portfolio).
2. **Dashboard Object Model Corrected**: Sidebar registration in Odoo 18's Dashboards app requires a `spreadsheet.dashboard.group` record titled `OBIDSS Operational BI` and `spreadsheet.dashboard` records linked to that group. Reparenting `ir.ui.menu` alone is insufficient.
3. **No Direct SQL Hierarchy Updates**: All raw SQL `UPDATE ir_ui_menu SET parent_path = ...` proposals have been **DELETED**. Hierarchy fields will be computed natively by Odoo ORM during XML module data loading.
4. **Dashboard Status Reset**: All dashboard statuses are reset to `IMPLEMENTATION PENDING` or `BLOCKED BY ACCOUNTING AUDIT`. Zero dashboards are marked PASS prior to Stage 2 verification.

---

## 2. File & Record Level Task Breakdown

### TASK 11.2.1: Register OBIDSS Dashboard Group & Sidebar Records in XML

| Field | Content / Specification |
|---|---|
| **Task ID** | `TASK-11.2.1-V2` |
| **Objective** | Register `spreadsheet.dashboard.group` titled `OBIDSS Operational BI` and `spreadsheet.dashboard` records in custom addon XML data to populate Odoo 18's native Dashboards app sidebar. |
| **Current evidence** | Audit query confirms `spreadsheet.dashboard.group` records exist for Sales, Finance, Logistics, etc., but not yet for OBIDSS. |
| **Root cause** | Odoo 18 Dashboards app client action (`action_spreadsheet_dashboard`) renders its sidebar from `spreadsheet.dashboard.group` and `spreadsheet.dashboard` models. |
| **Strategy** | XML Data Record Creation (`data/dashboard_groups.xml`). |
| **Possible** | Yes |
| **Exact files** | `custom_addons/obidss_operational_bi/data/dashboard_groups.xml`, `__manifest__.py` |
| **Exact records** | `spreadsheet.dashboard.group` (`dashboard_group_obidss`), `spreadsheet.dashboard` (`dashboard_executive`) |
| **Exact change** | Add `<record id="dashboard_group_obidss" model="spreadsheet.dashboard.group">`. |
| **Technical method** | XML Data Load via standard Odoo module upgrade. |
| **Dependencies** | `spreadsheet_dashboard` module |
| **Test** | Open `http://localhost:8069/odoo/dashboards`; verify `OBIDSS Operational BI` sidebar section appears. |
| **Browser proof** | Screenshot of Dashboards sidebar showing `OBIDSS Operational BI`. |
| **Rollback** | Module uninstall / XML ID removal. |
| **Risk** | Low |
| **Destructive** | No |
| **Approval** | Required |

---

### TASK 11.2.2: Reparent OBIDSS Submenus & Bind to Live Operational Views

| Field | Content / Specification |
|---|---|
| **Task ID** | `TASK-11.2.2-V2` |
| **Objective** | Reparent OBIDSS submenus under `spreadsheet_dashboard.spreadsheet_dashboard_menu_root` (ID 177) and bind to live Graph/Pivot/List actions (`sale.action_orders`, `purchase.purchase_form_action`, `stock.action_inventory_at_date`). |
| **Current evidence** | Audit query confirms window actions exist for `sale.order` (ID 446), `purchase.order` (ID 413), `stock.quant` (ID 349). |
| **Root cause** | Operational submenus require explicit action bindings to display live transactions. |
| **Strategy** | XML Data Record Update (`views/obidss_menus.xml`). |
| **Possible** | Yes |
| **Exact files** | `custom_addons/obidss_operational_bi/views/obidss_menus.xml` |
| **Exact records** | `ir.ui.menu` IDs 378, 379, 380, 381, 382, 383, 384 |
| **Exact change** | Set `parent_id = "spreadsheet_dashboard.spreadsheet_dashboard_menu_root"` and `action = "sale.action_orders"` etc. |
| **Technical method** | Standard Odoo XML data loading (ORM computes `parent_path` natively). |
| **Dependencies** | `TASK-11.2.1-V2` |
| **Test** | Click `Sales Operations` -> displays 740 SOs; Click `Purchase & Suppliers` -> displays 251 POs. |
| **Browser proof** | Screenshots of live Graph/Pivot views for Sales, Purchase, and Inventory. |
| **Rollback** | Reset parent and action attributes via XML data load. |
| **Risk** | Low |
| **Destructive** | No |
| **Approval** | Required |

---

### TASK 11.2.3: Restrict Irrelevant Applications via Dedicated Security Groups

| Field | Content / Specification |
|---|---|
| **Task ID** | `TASK-11.2.3-V2` |
| **Objective** | Restrict `Discuss`, `Email Marketing`, `Surveys`, `Employees` for portfolio reviewer & operational users via group assignments without uninstalling modules. |
| **Current evidence** | Audit shows `Discuss` (ID 82), `Email Marketing` (ID 338), `Surveys` (ID 312), `Employees` (ID 319) open to all users. |
| **Root cause** | Standard module menu items lack restrictive `groups_id`. |
| **Strategy** | Create dedicated `OBIDSS Portfolio Reviewer` user role and apply menu restrictions in `views/menu_restructure.xml`. |
| **Possible** | Yes |
| **Exact files** | `custom_addons/obidss_operational_bi/views/menu_restructure.xml`, `security/security_groups.xml` |
| **Exact records** | `ir.ui.menu` IDs 82, 338, 312, 319 |
| **Exact change** | Assign restrictive `groups` attribute on XML menu overrides. |
| **Technical method** | Standard Odoo XML data loading. |
| **Dependencies** | `TASK-11.2.1-V2` |
| **Test** | Log in as `reviewer`; verify launcher displays only `Dashboards`, `Sales`, `Purchase`, `Inventory`, `Invoicing`, `Contacts`. |
| **Browser proof** | App launcher screenshot for `reviewer` user. |
| **Rollback** | Remove `groups` attribute from menu overrides. |
| **Risk** | Low |
| **Destructive** | No |
| **Approval** | Required |

---

### TASK 11.2.4: Module Update Rehearsal on Isolated Clone Database

| Field | Content / Specification |
|---|---|
| **Task ID** | `TASK-11.2.4-V2` |
| **Objective** | Perform CLI module update rehearsal on clone database `Business_Intelegent_Project_v2_clone` to verify zero errors before primary execution. |
| **Current evidence** | Clone DB exists and is restored from production dump. |
| **Root cause** | Mandatory safety gate prior to production execution. |
| **Strategy** | Isolated CLI execution with `--stop-after-init --no-http`. |
| **Possible** | Yes |
| **Exact files** | `docs/phase11_2_revision/upgrade_rehearsal.log` |
| **Exact records** | All XML IDs in `obidss_operational_bi` |
| **Exact change** | Execute module upgrade CLI command on clone DB. |
| **Technical method** | `odoo-bin -c odoo.conf -d Business_Intelegent_Project_v2_clone -u obidss_operational_bi --stop-after-init --no-http`. |
| **Dependencies** | `TASK-11.2.1-V2`, `TASK-11.2.2-V2`, `TASK-11.2.3-V2` |
| **Test** | Check `upgrade_rehearsal.log` for 0 Errors and Exit Code 0. |
| **Browser proof** | N/A (CLI log verification). |
| **Rollback** | N/A (Clone DB). |
| **Risk** | Low |
| **Destructive** | No |
| **Approval** | Required |

---

### TASK 11.2.5: Primary Database Execution & 6-Layer Validation

| Field | Content / Specification |
|---|---|
| **Task ID** | `TASK-11.2.5-V2` |
| **Objective** | Execute module update on primary database `Business_Intelegent_Project_v2` and perform 6-layer validation. |
| **Current evidence** | Primary database `Business_Intelegent_Project_v2` running on port 8069. |
| **Root cause** | Production execution stage post-user approval. |
| **Strategy** | XML-RPC ORM `button_immediate_upgrade` on `ir.module.module`. |
| **Possible** | Yes |
| **Exact files** | All custom addon files in `custom_addons/obidss_operational_bi/` |
| **Exact records** | `ir.module.module` record for `obidss_operational_bi` |
| **Exact change** | Upgrade custom addon on primary database. |
| **Technical method** | XML-RPC ORM call `button_immediate_upgrade`. |
| **Dependencies** | `TASK-11.2.4-V2` |
| **Test** | Complete 6-layer validation contract in `validation_contract.md`. |
| **Browser proof** | Screenshots for all 10 UI test cases. |
| **Rollback** | Restore DB from `Business_Intelegent_Project_v2_backup.dump`. |
| **Risk** | Medium |
| **Destructive** | No |
| **Approval** | Required |
