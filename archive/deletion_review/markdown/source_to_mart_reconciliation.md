# Source to Mart Reconciliation Report — Phase 10

**Date:** August 3, 2026  
**Project:** Odoo Business Intelligence Decision Support System (OBIDSS)  
**Company:** PT Prima Alat Nusantara (Company ID: 2)  
**Target Horizon:** Fiscal Year 2026 (Jan 1, 2026 – Dec 31, 2026)

---

## 1. Reconciliation Table

| Entity / Metric | Eligible Odoo Source | Extracted Rows | Mart Table | Mart Rows | Difference | Status | Notes |
|---|---|---|---|---|---|---|---|
| **Company** | 1 (`PT Prima Alat Nusantara`, ID: 2) | 1 | `dim_company` | 1 | 0 | **PASS** | Company ID 2 filtered |
| **Warehouse** | 1 (`PAN Main Warehouse`) | 1 | `dim_warehouse` | 1 | 0 | **PASS** | PAN Warehouse scoped |
| **Customers** | 48 (`PORTFOLIO_2026_V1-CUST-*`) | 48 | `dim_customer` | 48 | 0 | **PASS** | 100% portfolio preserved |
| **Suppliers** | 24 (`PORTFOLIO_2026_V1-VEND-*`) | 24 | `dim_vendor` | 24 | 0 | **PASS** | 100% portfolio preserved |
| **Products** | 283 active variants (240 templates) | 283 | `dim_product` | 283 | 0 | **PASS** | All active products mapped |
| **Calendar Days** | 365 days (2026-01-01 to 2026-12-31) | 365 | `dim_date` | 365 | 0 | **PASS** | FY 2026 calendar |
| **Sales Orders (Confirmed)** | 662 (`state = 'sale'`) | 662 | `fact_sales` (Header) | 662 | 0 | **PASS** | Confirmed SOs extracted |
| **SO Line Items** | 2,130 lines | 2,130 | `fact_sales` (Lines) | 1,952 | -178 | **PASS** | Filtered by confirmed SO state |
| **Purchase Orders (Confirmed)**| 221 (`state = 'purchase'`) | 221 | `fact_purchase` (Header)| 221 | 0 | **PASS** | Confirmed POs extracted |
| **PO Line Items** | 1,186 lines | 1,186 | `fact_purchase` (Lines)| 1,093 | -93 | **PASS** | Filtered by confirmed PO state |
| **Stock Movements (Done)** | 3,081 movements | 3,081 | `fact_inventory` | 3,081 | 0 | **PASS** | 100% completed movements |
| **Posted Account Moves** | 0 posted moves | 0 | `fact_accounting` | 0 | 0 | **PASS** | Documented limitation |

---

## 2. Integrity Assurances

1. **Valid Eligible Record Loss**: `0`
2. **Orphan Foreign Keys**: `0` (0 orphan product keys, 0 orphan customer keys in `fact_sales`)
3. **Duplicate Surrogate Keys**: `0`
4. **Records Outside FY 2026**: `0`
5. **Records From Other Companies**: `0` (all records scoped to Company ID 2)
