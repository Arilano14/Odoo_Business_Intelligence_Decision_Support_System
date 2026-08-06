# Odoo & Power BI Dashboard Alignment Specification — Phase 11.0

**Date:** August 3, 2026  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. Role Separation Framework

- **Odoo Dashboard**: Real-time Operational BI for transactional monitoring, pending order alerts, current stock levels, and direct record drill-down.
- **Power BI**: Historical & Executive BI for time-series trends, MA3 demand forecasting, EOQ/ROP optimization, supplier performance scoring, and strategic management analysis.

---

## 2. KPI Terminology & Definition Matrix

| KPI Business Name | Odoo Source Model & Field | Source Filter | Odoo Mart Field | Power BI Measure | Measurement Unit | Status / Limitation |
|---|---|---|---|---|---|---|
| **Confirmed Sales Value** | `sale_order.amount_total` | `state = 'sale'`, `company_id = 2`, FY 2026 | `fact_sales.revenue` | `[Total Confirmed Sales]` | IDR (Rp) | **Active** (Not Recognized Revenue) |
| **Recognized Revenue** | `account_move.amount_total` | `move_type = 'out_invoice'`, `state = 'posted'` | `fact_accounting.debit` | `[Total Recognized Revenue]` | IDR (Rp) | **NOT AVAILABLE IN CURRENT MVP** (Documented limitation) |
| **Confirmed Purchase Value** | `purchase_order.amount_total` | `state = 'purchase'`, `company_id = 2`, FY 2026 | `fact_purchase.subtotal` | `[Total Confirmed Purchase]` | IDR (Rp) | **Active** (Not Cash Expenditure) |
| **Planned Lead Time** | `date_planned - date_order` | `purchase_order` | `fact_purchase.lead_time_days` | `[Avg Planned Lead Time]` | Days | **Active** |
| **Actual Lead Time** | Completed receipt date - PO confirmation date | `stock_move` + `purchase_order` | `fact_purchase.lead_time_days` | `[Avg Actual Lead Time]` | Days | **Active** |
| **Delivery Delay** | Completed receipt date - Planned receipt date | `stock_move` | `fact_purchase.lead_time_days` | `[Avg Delivery Delay]` | Days | **Active** |
| **On-Hand Inventory Value** | `stock_quant.quantity` $\times$ `standard_price` | `location_id.usage = 'internal'` | `fact_inventory.value` | `[Total Inventory Value]` | IDR (Rp) | **Active** |
