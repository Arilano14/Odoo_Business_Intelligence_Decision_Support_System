# Power BI Manual Validation Instructions & Truth Queries — Phase 11.1

**Date:** August 3, 2026  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)  
**Validation Status:** **PENDING MANUAL VALIDATION**

---

## 1. Truth Query Benchmarks

```sql
-- Total Confirmed Revenue
SELECT SUM(revenue) FROM mart.fact_sales;
-- Benchmark: Rp 1,572,400,000.00

-- Total Confirmed Purchase Value
SELECT SUM(subtotal) FROM mart.fact_purchase;
-- Benchmark: Rp 1,120,800,000.00
```

---

## 2. Manual Refresh Checklist

1. Open Power BI file `Odoo DSS_v2.pbix`.
2. Click **Refresh** to load PostgreSQL schema `mart` data.
3. Confirm `[Total Revenue]` measure matches Rp 1,572,400,000.00.
4. Confirm `[Total Purchase]` measure matches Rp 1,120,800,000.00.
