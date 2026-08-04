# Target Dashboard Information Architecture — Phase 11.2

**Date:** August 4, 2026  
**Status:** **ARCHITECTURE SPECIFICATION APPROVED**  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. Consolidated Menu Hierarchy

```text
Dashboards (Top-Level Launcher Application Menu — ID: 177)
│
├── OBIDSS Operational Dashboards (Group: OBIDSS Operational BI)
│   ├── Executive Operations (Summary Cards, Sales vs Purchase, Stock Overview)
│   ├── Sales Operations (Live Graph/Pivot/List: 740 SOs, Top Customers, Categories)
│   ├── Purchase & Suppliers (Live Graph/Pivot/List: 251 POs, Top Vendors, Lead Times)
│   ├── Inventory Operations (Live Stock Quantities, 24 Transfers, 12 Scraps)
│   ├── Finance & Invoicing (Customer Invoices, Vendor Bills, Payment Status)
│   └── Data Quality & Reconciliation (Source vs DW Mart Row Counts & Integrity)
│
└── Technical Baseline Dashboards (Admin / Baseline Only — Hidden for Target Users)
    ├── Invoicing (ID 1)
    ├── Warehouse Metrics (ID 2)
    ├── Sales (ID 3)
    └── Product (ID 4)
```

---

## 2. Rationalization Rules

1. **Top-Level Launcher Consolidation**: Standalone top-level application menu `OBIDSS` (ID 377) is removed from the main app launcher. All 6 operational dashboards are reparented under `Dashboards` (ID 177).
2. **Operational Drill-down Preservation**: Standard operational app icons (`Sales`, `Purchase`, `Inventory`, `Invoicing`, `Contacts`) remain visible on the app launcher based on user roles (`group_obidss_sales`, `group_obidss_purchase`, `group_obidss_inventory`, `group_obidss_finance`) to enable 1-click drill-down to individual transaction forms.
3. **Irrelevant App Hiding**: Non-operational applications (`Discuss`, `Email Marketing`, `Surveys`, `Employees`) are restricted via `groups_id` and hidden from operational users without uninstalling any modules.
