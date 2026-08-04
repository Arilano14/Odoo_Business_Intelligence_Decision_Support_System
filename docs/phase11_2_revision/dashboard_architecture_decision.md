# Dashboard Architecture Decision Matrix — Phase 11.2 Revision

**Date:** August 4, 2026  
**Status:** **ARCHITECTURE DECISION APPROVED**  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. Comparative Evaluation Matrix

| Decision Criterion | Option 1: Native Views | Option 2: Spreadsheet | Option 3: HYBRID (Recommended) | Option 4: Client Action |
|---|---|---|---|---|
| **Odoo 18 Compatibility** | 🟢 Excellent | 🟢 High | 🟢 **EXCELLENT** | 🟡 Moderate |
| **Live Data Connection** | 🟢 100% Live ORM | 🟡 Snapshot Dependent | 🟢 **100% LIVE ORM** | 🟢 100% Live |
| **Executive Visual Quality** | 🟡 Separate Views | 🟢 High | 🟢 **HIGH** | 🟢 Custom |
| **1-Click Transaction Drill-down** | 🟢 Native | 🟡 Complex | 🟢 **NATIVE (740 SOs / 251 POs)** | 🟡 Complex |
| **Security & Group Filtering** | 🟢 Native ORM | 🟡 Hardcoded Groups | 🟢 **NATIVE ORM** | 🟡 Custom JS |
| **Maintainability & Stability** | 🟢 0 JS Risk | 🔴 JS Render Risk | 🟢 **0 JS RISK** | 🔴 High JS Effort |
| **Automated Testing** | 🟢 Simple ORM Test | 🟡 Complex JSON Audit | 🟢 **SIMPLE ORM TEST** | 🔴 Complex |
| **S2 Portfolio Presentation** | 🟢 High | 🟢 High | 🌟 **MAXIMUM S2 QUALITY** | 🟢 High |

---

## 2. Final Architectural Recommendation

```text
HYBRID DASHBOARD ARCHITECTURE (OPTION 3)
```

1. **Dashboard Host & Sidebar**: Register a custom `spreadsheet.dashboard.group` titled `OBIDSS Operational BI` inside the host **Dashboards** application (`spreadsheet_dashboard_menu_root`).
2. **Executive Overview**: High-level executive KPI cards hosted within a valid Odoo Spreadsheet Dashboard format.
3. **Operational Dashboards**: Native Odoo Live Reporting Views (`view_mode="graph,pivot,list"`) for Sales, Purchase, Inventory, Finance, & Data Quality, enabling 1-click drill-down directly to the 740 SOs and 251 POs of PT Prima Alat Nusantara.
