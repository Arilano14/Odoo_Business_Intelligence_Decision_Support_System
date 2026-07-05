# Data Requirements

## Source Tables (Odoo 18 PostgreSQL)

### Sales Module
| Table | Required Columns | Tipe |
| :--- | :--- | :--- |
| sale_order | id, name, partner_id, date_order, amount_total, amount_untaxed, state, company_id | Transactional |
| sale_order_line | id, order_id, product_id, product_uom_qty, price_unit, price_subtotal, discount | Detail |

### Purchase Module
| Table | Required Columns | Tipe |
| :--- | :--- | :--- |
| purchase_order | id, name, partner_id, date_order, date_planned, amount_total, state | Transactional |
| purchase_order_line | id, order_id, product_id, product_qty, price_unit, price_subtotal, date_planned | Detail |

### Inventory Module
| Table | Required Columns | Tipe |
| :--- | :--- | :--- |
| stock_move | id, name, product_id, product_uom_qty, location_id, location_dest_id, state, date, reference | Transactional |
| stock_quant | id, product_id, location_id, quantity | Snapshot |
| stock_picking | id, name, partner_id, scheduled_date, date_done, state, picking_type_id | Transactional |
| stock_warehouse | id, name, code, company_id | Master |

### Accounting Module
| Table | Required Columns | Tipe |
| :--- | :--- | :--- |
| account_move | id, name, move_type, partner_id, date, amount_total, state, journal_id | Transactional |
| account_move_line | id, move_id, account_id, debit, credit, name, date | Detail |

### Master Data
| Table | Required Columns | Tipe |
| :--- | :--- | :--- |
| product_product | id, product_tmpl_id, default_code, active | Master |
| product_template | id, name, list_price, standard_price, categ_id, type, sale_ok, purchase_ok | Master |
| product_category | id, name, parent_id | Master |
| res_partner | id, name, email, phone, city, country_id, supplier_rank, customer_rank, company_type | Master |
| res_company | id, name | Master |
