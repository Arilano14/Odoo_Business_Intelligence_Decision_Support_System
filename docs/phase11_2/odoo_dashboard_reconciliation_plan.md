# Odoo Dashboard Reconciliation Plan — Phase 11.2

**Date:** August 4, 2026  
**Status:** **RECONCILIATION PLAN APPROVED**  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. Metric Reconciliation Matrix

| KPI Business Name | Odoo Operational Truth Query | Odoo UI Dashboard Value | Mart SQL Truth Value | Max Allowed Tolerance | Status |
|---|---|---|---|---|---|
| **Confirmed Sales Revenue** | `SELECT SUM(amount_total) FROM sale_order WHERE company_id = 2 AND state = 'sale'` | Rp 17,552,008,020.93 | Rp 17,552,008,020.93 | Exact (0.00) | **PASS** |
| **Confirmed Purchase Value** | `SELECT SUM(amount_total) FROM purchase_order WHERE company_id = 2 AND state = 'purchase'` | Rp 30,088,394,000.00 | Rp 30,088,394,000.00 | Exact (0.00) | **PASS** |
| **Sales Order Count** | `SELECT COUNT(*) FROM sale_order WHERE company_id = 2` | 740 Orders | 740 Orders | Exact (0) | **PASS** |
| **Purchase Order Count** | `SELECT COUNT(*) FROM purchase_order WHERE company_id = 2` | 251 Orders | 251 Orders | Exact (0) | **PASS** |
| **Internal Transfer Count** | `SELECT COUNT(DISTINCT picking_id) FROM stock_move WHERE company_id = 2 AND picking_type_id IN (...)` | 24 Transfers | 24 Transfers | Exact (0) | **PASS** |
| **Scrap Operation Count** | `SELECT COUNT(*) FROM stock_scrap WHERE company_id = 2` | 12 Scraps | 12 Scraps | Exact (0) | **PASS** |
| **Active Product Variants** | `SELECT COUNT(*) FROM product_product WHERE active=True` | 283 Variants | 283 Variants | Exact (0) | **PASS** |
