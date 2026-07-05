# Transformation Rules

## Business Rule Filtering (Odoo 18)

| Source Table | Filter | Keterangan |
| :--- | :--- | :--- |
| sale_order | state = 'sale' | Hanya SO confirmed |
| purchase_order | state = 'purchase' | Hanya PO confirmed |
| stock_move | state = 'done' | Hanya movement selesai |
| account_move | state = 'posted' | Hanya journal posted |
| product_product | active = True | Hanya produk aktif |

## Join Rules

| Target | Join Logic |
| :--- | :--- |
| fact_sales | sale_order_line LEFT JOIN sale_order ON order_id LEFT JOIN product_product ON product_id |
| fact_purchase | purchase_order_line LEFT JOIN purchase_order ON order_id LEFT JOIN product_product ON product_id |
| fact_inventory | stock_move (no join, self-contained) |
| fact_accounting | account_move_line LEFT JOIN account_move ON move_id |
| dim_product | product_product LEFT JOIN product_template ON product_tmpl_id LEFT JOIN product_category ON categ_id |
| dim_customer | res_partner WHERE customer_rank > 0 |
| dim_vendor | res_partner WHERE supplier_rank > 0 |

## Derived Columns

| Column | Formula | Target Table |
| :--- | :--- | :--- |
| revenue | price_unit × quantity × (1 - discount/100) | fact_sales |
| date_id | CAST(date AS INT, format YYYYMMDD) | All fact tables |
| movement_type | 'incoming' if location_dest is internal, else 'outgoing' | fact_inventory |
