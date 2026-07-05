# Fact & Dimension Validation (KPI Mapping)

| KPI | Formula Source | Required Dimensions | Validated? |
| --- | --- | --- | --- |
| Revenue | act_sales.amount_total | Date, Product, Customer | Yes |
| Inventory Value | act_inventory.qty_on_hand * cost | Date, Product, Warehouse | Yes |
| Purchase Value | act_purchase.amount_total | Date, Product, Vendor | Yes |
| Forecast Demand | Prophet on act_sales | Date, Product | Yes |
