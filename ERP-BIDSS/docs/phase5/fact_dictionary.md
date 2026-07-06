# Fact Dictionary

## fact_sales
**Grain:** 1 row = 1 confirmed sale_order_line
**Source:** sale_order JOIN sale_order_line WHERE state='sale'

| Column | Type | FK→ | Description | Derived? |
| :--- | :--- | :--- | :--- | :---: |
| sk_sales_id | SERIAL PK | — | Surrogate key | — |
| date_id | INTEGER | dim_date | Tanggal order (dari sale_order.date_order) | — |
| product_id | INTEGER | dim_product | Produk yang dijual | — |
| customer_id | INTEGER | dim_customer | Customer pembeli | — |
| company_id | INTEGER | dim_company | Perusahaan (PT Prima Alat Nusantara) | — |
| quantity | NUMERIC(15,4) | — | Jumlah unit yang dijual | — |
| price_unit | NUMERIC(15,2) | — | Harga per unit | — |
| discount | NUMERIC(5,2) | — | Persentase diskon (0–100) | — |
| subtotal | NUMERIC(15,2) | — | price_subtotal dari Odoo | — |
| revenue | NUMERIC(15,2) | — | qty × price_unit × (1 - discount/100) | ✅ |
| cost | NUMERIC(15,2) | — | qty × standard_price (dari dim_product) | ✅ |
| margin | NUMERIC(15,2) | — | revenue - cost | ✅ |

---

## fact_purchase
**Grain:** 1 row = 1 confirmed purchase_order_line
**Source:** purchase_order JOIN purchase_order_line WHERE state='purchase'

| Column | Type | FK→ | Description | Derived? |
| :--- | :--- | :--- | :--- | :---: |
| sk_purchase_id | SERIAL PK | — | Surrogate key | — |
| date_id | INTEGER | dim_date | Tanggal PO (dari purchase_order.date_order) | — |
| product_id | INTEGER | dim_product | Produk yang dibeli | — |
| vendor_id | INTEGER | dim_vendor | Vendor/Supplier | — |
| company_id | INTEGER | dim_company | Perusahaan | — |
| quantity | NUMERIC(15,4) | — | Jumlah unit yang dibeli | — |
| price_unit | NUMERIC(15,2) | — | Harga per unit dari vendor | — |
| subtotal | NUMERIC(15,2) | — | price_subtotal dari Odoo | — |
| lead_time_days | INTEGER | — | date_planned - date_order (hari) | ✅ |

---

## fact_inventory
**Grain:** 1 row = 1 completed stock_move
**Source:** stock_move WHERE state='done'

| Column | Type | FK→ | Description | Derived? |
| :--- | :--- | :--- | :--- | :---: |
| sk_inventory_id | SERIAL PK | — | Surrogate key | — |
| date_id | INTEGER | dim_date | Tanggal pergerakan stok | — |
| product_id | INTEGER | dim_product | Produk yang bergerak | — |
| warehouse_id | INTEGER | dim_warehouse | Gudang terkait | — |
| quantity | NUMERIC(15,4) | — | Jumlah unit yang bergerak | — |
| value | NUMERIC(15,2) | — | qty × standard_price (valuasi) | ✅ |
| movement_type | VARCHAR(20) | — | 'incoming' (receipt) atau 'outgoing' (delivery) | ✅ |
| reference | VARCHAR(100) | — | Referensi (SO/PO number) | — |

---

## fact_accounting
**Grain:** 1 row = 1 posted account_move_line
**Source:** account_move JOIN account_move_line WHERE state='posted'

| Column | Type | FK→ | Description | Derived? |
| :--- | :--- | :--- | :--- | :---: |
| sk_accounting_id | SERIAL PK | — | Surrogate key | — |
| date_id | INTEGER | dim_date | Tanggal posting jurnal | — |
| company_id | INTEGER | dim_company | Perusahaan | — |
| debit | NUMERIC(15,2) | — | Nilai debit | — |
| credit | NUMERIC(15,2) | — | Nilai kredit | — |
| account_name | VARCHAR(255) | — | Nama akun/label | — |
| move_type | VARCHAR(30) | — | Tipe jurnal Odoo (out_invoice, in_invoice, entry) | — |
| source_module | VARCHAR(30) | — | Modul asal: 'sales', 'purchase', 'manual' | ✅ |
