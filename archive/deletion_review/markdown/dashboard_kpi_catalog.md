# Dashboard KPI Catalog — Phase 11.1

**Date:** August 3, 2026  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. Catalog of Operational KPIs

| KPI ID | KPI Business Name | Source Model & Field | Filter Scope | Target Dashboard | Visual Type |
|---|---|---|---|---|---|
| **KPI-01** | Confirmed Sales Value | `sale_order.amount_total` | `state = 'sale'`, `company_id = 2`, FY 2026 | Executive & Sales | Metric Card / Line Chart |
| **KPI-02** | Confirmed Purchase Value | `purchase_order.amount_total` | `state = 'purchase'`, `company_id = 2`, FY 2026 | Executive & Purchase | Metric Card / Bar Chart |
| **KPI-03** | Confirmed Sales Order Count | `sale_order.id` | `state = 'sale'`, FY 2026 | Sales | Metric Card |
| **KPI-04** | Confirmed Purchase Order Count | `purchase_order.id` | `state = 'purchase'`, FY 2026 | Purchase | Metric Card |
| **KPI-05** | Planned Lead Time | `date_planned - date_order` | `purchase_order` | Purchase | Metric Card / Table |
| **KPI-06** | Actual Lead Time | Receipt Date - Approval Date | `stock_move` + `purchase_order` | Purchase | Metric Card / Table |
| **KPI-07** | Delivery Delay | Receipt Date - Planned Date | `stock_move` | Purchase | Metric Card |
| **KPI-08** | On-Hand Inventory Value | `stock_quant.quantity` $\times$ price | `location_id.usage = 'internal'` | Inventory | Metric Card / Bar Chart |
