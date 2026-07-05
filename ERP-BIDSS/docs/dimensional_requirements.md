# Dimensional Requirements

## Star Schema Design (Kimball)

### Dimension Tables (Conformed)
| Dimension | Source Table (Odoo 18) | Grain |
| :--- | :--- | :--- |
| dim_date | Generated (calendar) | 1 row per day |
| dim_product | product_product + product_template + product_category | 1 row per product |
| dim_customer | res_partner (customer_rank > 0) | 1 row per customer |
| dim_vendor | res_partner (supplier_rank > 0) | 1 row per vendor |
| dim_company | res_company | 1 row per company |
| dim_warehouse | stock_warehouse | 1 row per warehouse |

### Fact Tables
| Fact | Source Table (Odoo 18) | Grain | Measures |
| :--- | :--- | :--- | :--- |
| fact_sales | sale_order + sale_order_line | 1 row per order line | qty, price_unit, subtotal, discount |
| fact_purchase | purchase_order + purchase_order_line | 1 row per order line | qty, price_unit, subtotal |
| fact_inventory | stock_move | 1 row per stock movement | qty, value |
| fact_accounting | account_move + account_move_line | 1 row per journal line | debit, credit |
