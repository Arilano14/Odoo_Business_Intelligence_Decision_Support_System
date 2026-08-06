# Custom Odoo Operational BI Build Specification — Phase 11.0

**Date:** August 3, 2026  
**Project:** Odoo Business Intelligence Decision Support System (OBIDSS)

---

## 1. Custom Operational Dashboards Strategy

To avoid modifying standard Odoo dashboards directly, custom operational dashboards will be built by duplicating validated standard dashboards and configuring custom Odoo Spreadsheet views.

---

## 2. Planned OBIDSS Operational Dashboards

| Dashboard Name | Target Visual / KPI | Odoo Source Model | Filter Scope | Drill-down Target View | Security Group |
|---|---|---|---|---|---|
| **OBIDSS Executive Operations** | Confirmed Sales Value, Confirmed Purchase Value, Pending Delivery Count, Pending Receipt Count | `sale.report`, `purchase.report`, `stock.picking` | `company_id = 2`, FY 2026 | `sale.order.tree`, `purchase.order.tree` | `base.group_user` |
| **OBIDSS Sales Operations** | Monthly Confirmed Sales, Top 10 Customers, Top 10 Products, SO Status Breakdown | `sale.order`, `sale.order.line` | `state = 'sale'`, FY 2026 | `sale.order.form` | `sales_team.group_sale_salesman` |
| **OBIDSS Purchase Operations** | Monthly Confirmed Purchases, Top Vendors, Planned vs Actual Lead Time, Pending POs | `purchase.order`, `purchase.order.line` | `state = 'purchase'`, FY 2026 | `purchase.order.form` | `purchase.group_purchase_user` |
| **OBIDSS Inventory Operations** | On-Hand Stock Value, Stock In/Out Movements, Transfers, Scrap Operations Count | `stock.quant`, `stock.move` | `location_id.usage = 'internal'` | `stock.quant.tree` | `stock.group_stock_user` |

---

## 3. Investigation of Missing Purchase Dashboard

- **Finding**: Standard Odoo Community Edition 18 includes `spreadsheet_dashboard_sale`, `spreadsheet_dashboard_account`, and `spreadsheet_dashboard_stock_account`, but omits `spreadsheet_dashboard_purchase`.
- **Solution**: OBIDSS will build `OBIDSS Purchase Operations` dashboard using custom Odoo Spreadsheet dashboard views built directly on `purchase.order` and `purchase.report` models.
