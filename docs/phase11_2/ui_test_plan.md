# UI Verification & Browser Test Plan — Phase 11.2

**Date:** August 4, 2026  
**Status:** **TEST SPECIFICATION APPROVED**  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. Required UI Evidence Screenshots

| Test ID | Visual Target / View Area | Expected Visual Result | Verification Criteria |
|---|---|---|---|
| **UI-01** | App Launcher (Before Changes) | Standard launcher icons visible | Baseline capture |
| **UI-02** | App Launcher (After Changes) | Standalone `OBIDSS` app icon **REMOVED**; `Dashboards`, `Sales`, `Purchase`, `Inventory` visible | Clean app launcher |
| **UI-03** | Dashboards App Sidebar | `OBIDSS Operational Dashboards` section visible under `Dashboards` app | Reparenting verified |
| **UI-04** | Executive Operations Dashboard | Executive KPI cards showing Rp 17.55B Sales & Rp 30.08B Purchase | 0 sample mock items |
| **UI-05** | Sales Operations Live View | Live Graph/Pivot view displaying **740 Sales Orders** | Active 2026 SOs |
| **UI-06** | Purchase Operations Live View | Live Graph/Pivot view displaying **251 Purchase Orders** | Active 2026 POs |
| **UI-07** | Inventory Operations Live View | Live Stock Quant view displaying **283 Product Variants** & **3,081 Movements** | Active 2026 Stock |
| **UI-08** | Finance & Invoicing View | Role-restricted view of Invoices & Vendor Bills | Controlled visibility |
| **UI-09** | Data Quality Bridge View | Reconciliation view comparing Odoo vs DW `mart` schema | 0 row discrepancy |
| **UI-10** | Browser Developer Console | **0 Critical JS Errors**, 0 `UncaughtPromiseError` | Clean console log |

---

## 2. Expected App Launcher Visibility Summary

- 🔴 Standalone `OBIDSS` launcher icon **REMOVED** (Dashboards moved inside `Dashboards` app).
- 🟢 `Dashboards` icon **VISIBLE**.
- 🟢 `Sales`, `Purchase`, `Inventory` icons **VISIBLE** for operational drill-down.
- 🟡 `Invoicing` & `Contacts` icons **RESTRICTED** to Finance & Master Data roles.
- 🔴 `Discuss`, `Email Marketing`, `Surveys`, `Employees` **HIDDEN** for target operational users.
- 🔴 `Apps` & `Settings` **RESTRICTED** to Administrators only.
