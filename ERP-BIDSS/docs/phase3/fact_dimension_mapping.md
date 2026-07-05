# Fact & Dimension Mapping

## KPI to Star Schema Traceability

| KPI | Fact Table | Required Dimensions | Measures Used | Validated |
| :--- | :--- | :--- | :--- | :--- |
| Revenue | fact_sales | dim_date, dim_product, dim_customer | subtotal | ✅ |
| Sales Growth | fact_sales | dim_date | subtotal (month-over-month) | ✅ |
| Purchase Value | fact_purchase | dim_date, dim_product, dim_vendor | subtotal | ✅ |
| Purchase Growth | fact_purchase | dim_date | subtotal (month-over-month) | ✅ |
| Inventory Value | fact_inventory | dim_date, dim_product, dim_warehouse | quantity × standard_price | ✅ |
| Inventory Turnover | fact_sales + fact_inventory | dim_date, dim_product | COGS / Avg Inventory | ✅ |
| DIO | fact_sales + fact_inventory | dim_date, dim_product | (Avg Inventory / COGS) × 365 | ✅ |
| Revenue Contribution | fact_sales | dim_product | subtotal per product / total | ✅ |
| ROP | fact_sales + dim_product | dim_product | avg_daily_demand × lead_time | ✅ |
| EOQ | fact_sales + dim_product | dim_product | √(2DS/H) | ✅ |
| Supplier Performance | fact_purchase | dim_vendor | weighted_score | ✅ |
| Demand Forecast | fact_sales | dim_date, dim_product | MA3 on monthly qty | ✅ |

## Kesimpulan
Seluruh 12 KPI dapat diturunkan dari Star Schema yang dirancang. Tidak ada KPI yang membutuhkan tabel tambahan.
