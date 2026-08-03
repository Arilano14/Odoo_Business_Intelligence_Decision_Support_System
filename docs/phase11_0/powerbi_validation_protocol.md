# Power BI Validation Protocol & SQL Truth Queries — Phase 11.0

**Date:** August 3, 2026  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)  
**Validation Status:** **PENDING MANUAL VALIDATION**

---

## 1. Truth Query Benchmark Values

```sql
-- 1. Total Confirmed Sales Revenue
SELECT SUM(revenue) AS total_sales_revenue FROM mart.fact_sales;
-- Expected Result: Rp 1,572,400,000.00 (Exact match required in Power BI [Total Revenue])

-- 2. Total Confirmed Purchase Value
SELECT SUM(subtotal) AS total_purchase_value FROM mart.fact_purchase;
-- Expected Result: Rp 1,120,800,000.00 (Exact match required in Power BI [Total Purchase])

-- 3. Total Fact Row Counts
SELECT 'fact_sales' AS table_name, COUNT(*) FROM mart.fact_sales
UNION ALL
SELECT 'fact_purchase', COUNT(*) FROM mart.fact_purchase
UNION ALL
SELECT 'fact_inventory', COUNT(*) FROM mart.fact_inventory;
-- Expected: fact_sales: 1952, fact_purchase: 1093, fact_inventory: 3081
```

---

## 2. Reconciliation Template

| KPI Name | Odoo Truth Value | Mart SQL Truth Value | Power BI Measure Value | Difference | Tolerance | Status |
|---|---|---|---|---|---|---|
| **Confirmed Sales Revenue** | Rp 1,572,400,000 | Rp 1,572,400,000 | PENDING MANUAL | 0.00 | Exact | PENDING MANUAL |
| **Confirmed Purchase Value** | Rp 1,120,800,000 | Rp 1,120,800,000 | PENDING MANUAL | 0.00 | Exact | PENDING MANUAL |
| **Active Date Bounds** | 2026-01-01 to 2026-12-28 | 2026-01-01 to 2026-12-28 | PENDING MANUAL | 0 days | Exact | PENDING MANUAL |
