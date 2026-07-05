# Surrogate Key Plan

## Prinsip
- Seluruh Dimension Table menggunakan Surrogate Key (sk_*_id) sebagai Primary Key.
- Natural Key dari Odoo (odoo_*_id) dipertahankan sebagai kolom biasa untuk traceability.
- Surrogate Key bertipe INTEGER AUTO-INCREMENT.
- Fact Table menggunakan Surrogate Key sendiri (sk_*_id) dan Foreign Key ke Dimension.

## Mapping

| Dimension | Surrogate Key | Natural Key (Odoo) |
| :--- | :--- | :--- |
| dim_date | date_id (INT, format YYYYMMDD) | — |
| dim_product | sk_product_id | odoo_product_id (product_product.id) |
| dim_customer | sk_customer_id | odoo_partner_id (res_partner.id) |
| dim_vendor | sk_vendor_id | odoo_partner_id (res_partner.id) |
| dim_company | sk_company_id | odoo_company_id (res_company.id) |
| dim_warehouse | sk_warehouse_id | odoo_warehouse_id (stock_warehouse.id) |

## SCD Strategy
- **SCD Type 1** (overwrite) digunakan untuk MVP.
- Jika atribut berubah (misal harga produk), nilai lama ditimpa dengan nilai baru.
