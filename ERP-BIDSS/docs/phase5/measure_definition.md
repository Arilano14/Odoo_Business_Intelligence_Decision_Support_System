# Measure Definition

## Measures in Fact Tables

### Direct Measures (dari Odoo)
| Measure | Fact Table | Column | Aggregation | Description |
| :--- | :--- | :--- | :--- | :--- |
| Quantity Sold | fact_sales | quantity | SUM | Jumlah unit terjual |
| Selling Price | fact_sales | price_unit | AVG | Harga jual rata-rata |
| Discount | fact_sales | discount | AVG | Rata-rata diskon (%) |
| Subtotal Sales | fact_sales | subtotal | SUM | Subtotal dari Odoo |
| Quantity Purchased | fact_purchase | quantity | SUM | Jumlah unit dibeli |
| Subtotal Purchase | fact_purchase | subtotal | SUM | Subtotal dari Odoo |
| Stock Quantity | fact_inventory | quantity | SUM | Volume pergerakan stok |
| Journal Debit | fact_accounting | debit | SUM | Total debit |
| Journal Credit | fact_accounting | credit | SUM | Total kredit |

### Derived Measures (dihitung saat ETL)
| Measure | Fact Table | Column | Formula | Description |
| :--- | :--- | :--- | :--- | :--- |
| Revenue | fact_sales | revenue | qty × price × (1 - disc/100) | Pendapatan bersih per line |
| Cost | fact_sales | cost | qty × standard_price | Harga pokok penjualan per line |
| Margin | fact_sales | margin | revenue - cost | Laba kotor per line |
| Lead Time | fact_purchase | lead_time_days | date_planned - date_order | Waktu tunggu pengiriman (hari) |
| Inventory Value | fact_inventory | value | qty × standard_price | Valuasi pergerakan stok |
| Source Module | fact_accounting | source_module | map(move_type) | Asal jurnal (sales/purchase/manual) |

### KPI Measures (dihitung di Phase 6 / Power BI DAX)
| KPI | Base Measures | Formula |
| :--- | :--- | :--- |
| Total Revenue | SUM(revenue) | Direct from mart |
| Sales Growth | SUM(revenue) by month | MoM comparison |
| Inventory Turnover | SUM(cost) / AVG(inventory value) | Cross-fact calculation |
| DIO | (AVG inventory / SUM cost) × 365 | Cross-fact calculation |
| Revenue Contribution | product_revenue / total_revenue × 100 | Ratio calculation |
| ROP | AVG(daily qty) × lead_time | fact_sales + dim_product |
| EOQ | √(2DS/H) | fact_sales aggregation |
| Supplier Score | Weighted average of delivery/fulfillment/quality | fact_purchase aggregation |
| Demand Forecast | MA3(monthly qty) | fact_sales time series |
