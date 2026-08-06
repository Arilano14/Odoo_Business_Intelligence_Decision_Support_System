# Odoo 18 Dashboard Object Model & Registration Mechanism — Phase 11.2 Revision

**Date:** August 4, 2026  
**Status:** **MODEL AUDIT COMPLETED**  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. Technical Object Model Layer Mapping

In Odoo 18, placing dashboards inside the host **Dashboards** application (`spreadsheet_dashboard`) requires registering records across the following ORM layers:

```text
Browser Client Request (URL: http://localhost:8069/odoo/dashboards)
        │
        ▼
ir.actions.client (Tag: 'action_spreadsheet_dashboard', ID: 309)
        │
        ▼
spreadsheet.dashboard.group (Model: 'spreadsheet.dashboard.group')
        │
        ▼
spreadsheet.dashboard (Model: 'spreadsheet.dashboard')
        │
        ▼
ir.attachment (Model: 'ir.attachment', Field: 'spreadsheet_binary_data')
        │
        ▼
Data Sources (Live Odoo Models: 'sale.report', 'purchase.report', 'stock.move')
```

---

## 2. Layer Analysis

| Layer | Technical Model Name | XML ID Example | Purpose & Sidebar Impact |
|---|---|---|---|
| **Layer 1: App Host** | `ir.ui.menu` | `spreadsheet_dashboard.spreadsheet_dashboard_menu_root` (ID 177) | Main app launcher icon for "Dashboards" |
| **Layer 2: Client Action** | `ir.actions.client` | `spreadsheet_dashboard.spreadsheet_dashboard_action` (ID 309) | Renders OWL Javascript dashboard framework |
| **Layer 3: Dashboard Group** | `spreadsheet.dashboard.group` | `obidss_operational_bi.dashboard_group_obidss` | **Renders Sidebar Category** (e.g. "OBIDSS Operational BI") |
| **Layer 4: Dashboard Item** | `spreadsheet.dashboard` | `obidss_operational_bi.dashboard_executive` | **Renders Sidebar Dashboard Item** under the group |
| **Layer 5: Spreadsheet Data** | `ir.attachment` | `res_model='spreadsheet.dashboard'`, `res_id=ID` | Stores binary JSON layout & cell definitions |
| **Layer 6: Operational Views** | `ir.actions.act_window` | `sale.action_orders`, `purchase.purchase_form_action` | **Renders Live 1-Click Operational Drill-down Views** |

---

## 3. Required Decision Rule Answer

```text
C. HYBRID ARCHITECTURE REQUIRED
```

**Justification**:
1. Reparenting `ir.ui.menu` (`parent_id = 177`) places ordinary menu items in Odoo's menu bar, but does **NOT** automatically insert items into Odoo 18's OWL Dashboard App Sidebar.
2. To insert sidebar items into Odoo 18's native Dashboards app, we must register a `spreadsheet.dashboard.group` (e.g. `OBIDSS Operational BI`) and `spreadsheet.dashboard` records linked to that group.
3. To provide 1-click drill-down to the 740 SOs and 251 POs, each dashboard item connects to live Graph/Pivot/List window actions (`ir.actions.act_window`).
