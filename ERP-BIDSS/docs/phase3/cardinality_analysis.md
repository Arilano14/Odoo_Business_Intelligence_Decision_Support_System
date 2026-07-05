# Cardinality Analysis

## Relationship Cardinality (Odoo 18)

| Parent | Child | Cardinality | FK Column |
| :--- | :--- | :--- | :--- |
| res_partner (Customer) | sale_order | 1:N | sale_order.partner_id |
| sale_order | sale_order_line | 1:N | sale_order_line.order_id |
| res_partner (Vendor) | purchase_order | 1:N | purchase_order.partner_id |
| purchase_order | purchase_order_line | 1:N | purchase_order_line.order_id |
| product_product | sale_order_line | 1:N | sale_order_line.product_id |
| product_product | purchase_order_line | 1:N | purchase_order_line.product_id |
| product_product | stock_move | 1:N | stock_move.product_id |
| product_product | stock_quant | 1:N | stock_quant.product_id |
| product_template | product_product | 1:N | product_product.product_tmpl_id |
| product_category | product_template | 1:N | product_template.categ_id |
| res_company | stock_warehouse | 1:N | stock_warehouse.company_id |
| account_move | account_move_line | 1:N | account_move_line.move_id |
| stock_picking | stock_move | 1:N | stock_move.picking_id |
