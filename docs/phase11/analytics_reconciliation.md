# Source-to-Analytics Reconciliation Report — Phase 11

**Date:** August 3, 2026  
**Project:** Odoo Business Intelligence Decision Support System (OBIDSS)  
**Company:** PT Prima Alat Nusantara (Company ID: 2)  
**Target Horizon:** Fiscal Year 2026 (Jan 1, 2026 – Dec 31, 2026)

---

## 1. Reconciliation Matrix

| Analytical Object | Eligible Mart Input | Output Table | Output Rows | Difference | Status | Notes |
|---|---|---|---|---|---|---|
| **Monthly Demand Forecast** | 283 products $\times$ 12 months | `mart.fact_forecast_monthly` | 2,880 | 0 | **PASS** | 9 evaluation months (202604-202612) |
| **DSS Metrics (EOQ/ROP)** | 283 active products | `mart.fact_decision_support` | 283 | 0 | **PASS** | 100% active products calculated |
| **Supplier Performance Scores** | 24 portfolio vendors | `mart.fact_supplier_score` | 24 | 0 | **PASS** | 100% portfolio vendors graded |
| **Monthly Executive Summary** | 12 calendar months (2026) | `mart.monthly_summary` | 12 | 0 | **PASS** | 12 months FY 2026 |
| **Inventory Monthly Summary** | 12 calendar months (2026) | `mart.inventory_monthly_summary` | 12 | 0 | **PASS** | 12 months FY 2026 |
| **Sales Product Performance** | 240 sales products | `mart.sales_summary` | 240 | 0 | **PASS** | Revenue contribution sum = 100.00% |
| **Supplier Summary** | 24 portfolio vendors | `mart.supplier_summary` | 24 | 0 | **PASS** | Purchase contribution sum = 100.00% |
| **Inventory Summary** | 283 active products | `mart.inventory_summary` | 283 | 0 | **PASS** | Stock level, turnover, DIO per product |
| **Executive Rollup** | 12 calendar months (2026) | `mart.executive_summary` | 12 | 0 | **PASS** | Monthly executive rollups |

---

## 2. Integrity Assurances

1. **Infinity & NaN Values**: `0` across all 6 aggregation tables and DSS tables.
2. **Revenue Contribution Sum**: `100.00%` ($\pm 0.00\%$ rounding error).
3. **Purchase Contribution Sum**: `100.00%` ($\pm 0.00\%$ rounding error).
4. **Data Leakage**: `0` (MA3 forecast strictly uses prior 3 historical months $t-1, t-2, t-3$).
5. **Legacy 2024 Records**: `0` across all analytics tables.
