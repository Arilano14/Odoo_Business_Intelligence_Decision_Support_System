# Duplicate Analysis

## Target
Duplikasi Primary Key = 0%.

## Analisis

| Table | PK | Expected Duplicate | Keterangan |
| :--- | :--- | :--- | :--- |
| sale_order | id | 0% | Auto-increment di PostgreSQL |
| sale_order_line | id | 0% | Auto-increment di PostgreSQL |
| purchase_order | id | 0% | Auto-increment di PostgreSQL |
| stock_move | id | 0% | Auto-increment di PostgreSQL |
| account_move | id | 0% | Auto-increment di PostgreSQL |
| product_product | id | 0% | Auto-increment di PostgreSQL |
| res_partner | id | 0% | Auto-increment di PostgreSQL |

## Composite Duplicate Check
| Table | Composite Key | Expected Duplicate |
| :--- | :--- | :--- |
| sale_order_line | (order_id, product_id) | Diperbolehkan (satu SO bisa memiliki produk sama dengan beda qty) |

## Kesimpulan
Duplikasi PK = 0%. Duplikasi composite diperbolehkan sesuai logika bisnis Odoo.
