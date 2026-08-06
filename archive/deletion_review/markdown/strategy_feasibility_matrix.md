# Revision Strategy Feasibility Matrix — Phase 11.2

**Date:** August 4, 2026  
**Status:** **FEASIBILITY EVALUATION PASSED**  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. Feasibility Evaluation Matrix

| Strategy Code | Revision Strategy Description | Technically Possible | Safe for Production | Recommended | Rationale & Risk Assessment | Required Proof |
|---|---|---|---|---|---|---|
| **Strategy A** | Edit default Odoo core dashboard JSON directly | 🔴 No | 🔴 No | 🔴 **NOT ALLOWED** | Violates core ownership. Modifying core files causes git conflicts and upgrade failures. | File diff check |
| **Strategy B** | Modify Odoo core sample JSON files | 🔴 No | 🔴 No | 🔴 **NOT ALLOWED** | Violates core file immutability rule. Breaks standard Odoo modules. | File diff check |
| **Strategy C** | Load Odoo demo data | 🔴 No | 🔴 No | 🔴 **STRICTLY PROHIBITED** | Irreversible operation. Pollutes database with non-heavy equipment mock records. | DB check |
| **Strategy D** | Restore standard dashboards and leave them visible | 🟢 Yes | 🟢 Yes | 🟡 **BASELINE ONLY** | Keeps core dashboards intact but insufficient for OBIDSS operational requirements. | `spreadsheet.dashboard` query |
| **Strategy E** | Duplicate valid standard dashboards & customize via supported tools | 🟢 Yes | 🟢 Yes | 🟢 **PREFERRED FOR EXECUTIVES** | Safe custom spreadsheet creation for high-level executive KPI cards. | XML ID check |
| **Strategy F** | Build live Odoo Reporting Views (Graph + Pivot + List) | 🟢 Yes | 🟢 Yes | 🌟 **STRONGLY RECOMMENDED** | 100% stable, interactive, zero JS spreadsheet rendering risk, directly connected to 740 SOs & 251 POs. | Window Action query |
| **Strategy G** | Create read-only SQL View reporting models for DW bridge | 🟢 Yes | 🟢 Yes | 🟢 **RECOMMENDED FOR DATA QUALITY** | High-performance bridge for ETL & DW schema `mart` reconciliation without ORM write overhead. | `obidss.data.quality` query |
| **Strategy H** | Display PostgreSQL `mart` schema data directly inside Odoo | 🟡 Partial | 🔴 No | 🔴 **NOT RECOMMENDED** | Odoo operational dashboards must primarily query operational models (`sale_order`, `purchase_order`). | Architecture review |

---

## 2. Final Strategic Recommendation

Adopt a **Hybrid Operational Architecture (Strategy E + F + G)**:
1. **Executive Operations**: Valid Odoo Spreadsheet Dashboard host (`spreadsheet_dashboard_menu_root`) containing high-level executive KPI cards.
2. **Operational Submenus (Sales, Purchase, Inventory, Finance)**: Native Odoo Live Reporting Views (`view_mode="graph,pivot,list"`) connected directly to `sale.order`, `purchase.order`, `stock.quant`, `account.move` filtered for **Company ID 2** and **FY 2026**.
3. **Data Quality & Reconciliation**: Read-only SQL View reporting model `obidss.data.quality` (`_auto = False`) comparing PostgreSQL operational tables against schema `mart`.
