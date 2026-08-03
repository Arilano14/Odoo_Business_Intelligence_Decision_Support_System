# KPI Alignment Matrix — Phase 11.1

**Date:** August 3, 2026  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. Cross-System Alignment Matrix

| KPI | Odoo Model | Odoo Fields | Mart Source | Power BI Measure | Unit | Filter | Tolerance |
|---|---|---|---|---|---|---|---|
| **Confirmed Sales Value** | `sale_order` | `amount_total` | `fact_sales.revenue` | `[Total Revenue]` | IDR (Rp) | `state = 'sale'`, `company_id = 2` | Exact (0.00) |
| **Confirmed Purchase Value** | `purchase_order` | `amount_total` | `fact_purchase.subtotal` | `[Total Purchase]` | IDR (Rp) | `state = 'purchase'`, `company_id = 2` | Exact (0.00) |
| **Sales Order Count** | `sale_order` | `id` | `fact_sales` (Distinct SO) | `[Total Sales Orders]` | Count | `state = 'sale'` | Exact (0) |
| **Purchase Order Count** | `purchase_order` | `id` | `fact_purchase` (Distinct PO) | `[Total Purchase Orders]` | Count | `state = 'purchase'` | Exact (0) |
| **On-Hand Inventory Value** | `stock_quant` | `quantity * price` | `fact_inventory.value` | `[Total Inventory Value]` | IDR (Rp) | `usage = 'internal'` | Exact (0.00) |
