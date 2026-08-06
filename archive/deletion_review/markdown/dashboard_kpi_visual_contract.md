# Dashboard KPI & Visual Contract — Phase 11.2

**Date:** August 4, 2026  
**Status:** **SPECIFICATION APPROVED**  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. Executive Operations Contract

| KPI / Visual | Target Metric / Visual Type | Target Odoo Model | Domain Filter | Grain | Unit | Drill-down Target | Empty-state Rule |
|---|---|---|---|---|---|---|---|
| **Confirmed Sales Value** | Metric Card | `sale.order` | `state = 'sale'`, `company_id = 2`, FY 2026 | Header | IDR (Rp) | `sale.order` list | Show `Rp 0.00` if no sales |
| **Confirmed Purchase Value** | Metric Card | `purchase.order` | `state = 'purchase'`, `company_id = 2`, FY 2026 | Header | IDR (Rp) | `purchase.order` list | Show `Rp 0.00` if no purchases |
| **Confirmed SO Count** | Metric Card | `sale.order` | `state = 'sale'`, `company_id = 2`, FY 2026 | Count | Orders | `sale.order` list | Show `0 Orders` |
| **Confirmed PO Count** | Metric Card | `purchase.order` | `state = 'purchase'`, `company_id = 2`, FY 2026 | Count | Orders | `purchase.order` list | Show `0 Orders` |
| **Monthly Sales vs Purchase** | Bar / Line Chart | `sale.report` vs `purchase.report` | `company_id = 2`, FY 2026 | Monthly | IDR (Rp) | Monthly Order list | Render empty axis |

---

## 2. Sales Operations Contract

| KPI / Visual | Target Metric / Visual Type | Target Odoo Model | Domain Filter | Grain | Unit | Drill-down Target | Empty-state Rule |
|---|---|---|---|---|---|---|---|
| **Confirmed Sales Revenue** | Metric Card | `sale.order` | `state = 'sale'`, `company_id = 2` | Total | IDR (Rp) | `sale.order` list | Show `Rp 0.00` |
| **Sales Revenue Trend** | Line Graph | `sale.report` | `company_id = 2`, FY 2026 | Monthly | IDR (Rp) | Monthly `sale.report` pivot | Render empty grid |
| **Top 10 Heavy Products** | Horizontal Bar Chart | `sale.report` | `company_id = 2`, FY 2026 | Product | IDR (Rp) | `product.product` form | Render "No Products Sold" |
| **Top Customers by Value** | Pivot Table | `sale.report` | `company_id = 2`, FY 2026 | Partner | IDR (Rp) | `res.partner` form | Render empty pivot |

---

## 3. Purchase & Suppliers Contract

| KPI / Visual | Target Metric / Visual Type | Target Odoo Model | Domain Filter | Grain | Unit | Drill-down Target | Empty-state Rule |
|---|---|---|---|---|---|---|---|
| **Confirmed Purchase Value** | Metric Card | `purchase.order` | `state = 'purchase'`, `company_id = 2` | Total | IDR (Rp) | `purchase.order` list | Show `Rp 0.00` |
| **Planned Lead Time** | Metric Card / Table | `purchase.order` | `date_planned - date_order` | Days | Days | `purchase.order` form | Show `0 Days` |
| **Actual Lead Time** | Metric Card / Table | `stock.move` + `purchase.order` | Receipt Date - Approval Date | Days | Days | `stock.move` form | Show `0 Days` |
| **Delivery Delay** | Metric Card | `stock.move` | Receipt Date - Planned Date | Days | Days | `stock.picking` form | Show `0 Days` |
| **Top Suppliers by Value** | Bar Chart / Pivot | `purchase.order` | `company_id = 2`, FY 2026 | Vendor | IDR (Rp) | `res.partner` form | Render "No PO Issued" |

---

## 4. Inventory Operations Contract

| KPI / Visual | Target Metric / Visual Type | Target Odoo Model | Domain Filter | Grain | Unit | Drill-down Target | Empty-state Rule |
|---|---|---|---|---|---|---|---|
| **On-Hand Inventory Value** | Metric Card | `stock.quant` | `location_id.usage = 'internal'` | Product | IDR (Rp) | `stock.quant` list | Show `Rp 0.00` |
| **Completed Movements** | Metric Card | `stock.move` | `state = 'done'`, `company_id = 2` | Moves | Moves | `stock.move` list | Show `0 Moves` |
| **Internal Transfers** | List / Metric | `stock.move` | `picking_type_id.code = 'internal'` | Pickings | Units | `stock.picking` form | Show `0 Transfers` |
| **Scrap Quantity** | List / Metric | `stock.scrap` | `company_id = 2` | Scraps | Units | `stock.scrap` form | Show `0 Scraps` |
