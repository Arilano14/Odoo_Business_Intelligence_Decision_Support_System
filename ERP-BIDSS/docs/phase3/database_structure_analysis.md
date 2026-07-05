# Database Structure Analysis

## Odoo Core Tables (Simulated)
| Table Name | Columns | Types | Primary Key | Foreign Keys | Nullable? |
| --- | --- | --- | --- | --- | --- |
| sale_order | 5 | int, varchar, date | id | partner_id | Yes (date_order) |
| sale_order_line | 7 | int, float | id | order_id, product_id | No |
| purchase_order | 5 | int, varchar, date | id | partner_id | Yes |
| stock_move | 6 | int, float, date | id | product_id, picking_id | No |
| ccount_move | 6 | int, varchar, date | id | partner_id | No |
| product_product | 4 | int, varchar | id | product_tmpl_id | No |
| es_partner | 5 | int, varchar | id | parent_id | Yes (email) |
