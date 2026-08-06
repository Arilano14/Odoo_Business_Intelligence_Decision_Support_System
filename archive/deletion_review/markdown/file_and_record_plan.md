# File and Record Level Plan — Phase 11.2 Revision

**Date:** August 4, 2026  
**Status:** **SPECIFICATION APPROVED**  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)  
**Target Addon:** `custom_addons/obidss_operational_bi/`

---

## 1. Required File Plan

| File Path | Existing / New | Exact Responsibility | Loaded by Manifest Order | Automated Test File |
|---|---|---|---|---|
| `__manifest__.py` | Existing | Addon configuration & manifest data loading sequence | Root | CLI Manifest Test |
| `__init__.py` | Existing | Root package initialization | Order 1 | Python Import Test |
| `models/__init__.py` | Existing | Models package initialization | Order 2 | Python Import Test |
| `models/obidss_data_quality.py` | Existing | Read-only SQL View model `obidss.data.quality` (`_auto = False`) | Order 3 | DB View Test |
| `security/security_groups.xml` | Existing | Defines security groups for OBIDSS roles | Data Order 1 | Group Existence Test |
| `security/ir.model.access.csv` | Existing | Model access rights for `obidss.data.quality` | Data Order 2 | Access Rights Test |
| `views/dashboard_groups.xml` | **New** | Registers `spreadsheet.dashboard.group` titled `OBIDSS Operational BI` | Data Order 3 | Group Registration Test |
| `views/menu_restructure.xml` | **New** | Reparents OBIDSS dashboards & restricts launcher menus | Data Order 4 | Menu Tree Test |
| `views/obidss_menus.xml` | Existing | Binds submenus to live Graph/Pivot/List actions | Data Order 5 | Action Binding Test |
| `views/obidss_data_quality_views.xml` | Existing | Tree & Form view for data quality bridge | Data Order 6 | View Rendering Test |

---

## 2. Required Record Plan

| Model Name | XML ID | Purpose | Parent / Group | Action / Data Source | Security Group |
|---|---|---|---|---|---|
| `spreadsheet.dashboard.group` | `dashboard_group_obidss` | Sidebar category in Dashboards app | Host App | `spreadsheet.dashboard.group` | `group_obidss_user` |
| `spreadsheet.dashboard` | `dashboard_executive` | Executive dashboard record | `dashboard_group_obidss` | Live Pivot (`sale.report`, `purchase.report`) | `group_obidss_user` |
| `ir.ui.menu` | `menu_obidss_sales` | Operational Sales submenu | `spreadsheet_dashboard_menu_root` | `sale.action_orders` (740 SOs) | `group_obidss_sales` |
| `ir.ui.menu` | `menu_obidss_purchase` | Operational Purchase submenu | `spreadsheet_dashboard_menu_root` | `purchase.purchase_form_action` (251 POs) | `group_obidss_purchase` |
| `ir.ui.menu` | `menu_obidss_inventory` | Operational Inventory submenu | `spreadsheet_dashboard_menu_root` | `stock.action_inventory_at_date` (283 Products) | `group_obidss_inventory` |
| `ir.ui.menu` | `menu_obidss_data_quality` | Data Quality bridge submenu | `spreadsheet_dashboard_menu_root` | `action_obidss_data_quality` | `group_obidss_reviewer` |
