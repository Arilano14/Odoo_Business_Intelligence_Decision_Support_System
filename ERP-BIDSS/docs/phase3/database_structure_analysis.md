# Database Structure Analysis

## Odoo 18 PostgreSQL Tables

### Sales Module
| Table | Key Columns | PK | FK | State Filter |
| :--- | :--- | :--- | :--- | :--- |
| sale_order | id, name, partner_id, date_order, amount_total, state | id | partner_id → res_partner.id | state='sale' |
| sale_order_line | id, order_id, product_id, product_uom_qty, price_unit, price_subtotal, discount | id | order_id → sale_order.id, product_id → product_product.id | — |

### Purchase Module
| Table | Key Columns | PK | FK | State Filter |
| :--- | :--- | :--- | :--- | :--- |
| purchase_order | id, name, partner_id, date_order, date_planned, amount_total, state | id | partner_id → res_partner.id | state='purchase' |
| purchase_order_line | id, order_id, product_id, product_qty, price_unit, price_subtotal | id | order_id → purchase_order.id, product_id → product_product.id | — |

### Inventory Module
| Table | Key Columns | PK | FK | State Filter |
| :--- | :--- | :--- | :--- | :--- |
| stock_move | id, product_id, product_uom_qty, location_id, location_dest_id, state, date, reference | id | product_id → product_product.id | state='done' |
| stock_quant | id, product_id, location_id, quantity | id | product_id → product_product.id | — |
| stock_picking | id, name, partner_id, scheduled_date, date_done, state | id | partner_id → res_partner.id | — |
| stock_warehouse | id, name, code, company_id | id | company_id → res_company.id | — |

### Accounting Module
| Table | Key Columns | PK | FK | State Filter |
| :--- | :--- | :--- | :--- | :--- |
| account_move | id, name, move_type, partner_id, date, amount_total, state | id | partner_id → res_partner.id | state='posted' |
| account_move_line | id, move_id, account_id, debit, credit, name, date | id | move_id → account_move.id | — |

### Master Data
| Table | Key Columns | PK | FK |
| :--- | :--- | :--- | :--- |
| product_product | id, product_tmpl_id, default_code, active | id | product_tmpl_id → product_template.id |
| product_template | id, name, list_price, standard_price, categ_id, type | id | categ_id → product_category.id |
| product_category | id, name, parent_id | id | parent_id → product_category.id |
| res_partner | id, name, email, phone, city, supplier_rank, customer_rank | id | — |
| res_company | id, name | id | — |
