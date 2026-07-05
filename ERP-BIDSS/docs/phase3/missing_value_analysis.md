# Missing Value Analysis

## Target
Missing value pada kolom kritikal harus < 5%.

## Analisis per Kolom Kritikal

| Table | Column | Expected Missing | Action |
| :--- | :--- | :--- | :--- |
| sale_order | date_order | 0% | Mandatory field di Odoo |
| sale_order | partner_id | 0% | Mandatory field di Odoo |
| sale_order_line | product_id | 0% | Mandatory field di Odoo |
| sale_order_line | price_unit | 0% | Default dari product_template.list_price |
| purchase_order | partner_id | 0% | Mandatory field di Odoo |
| stock_move | product_id | 0% | Mandatory field di Odoo |
| stock_move | date | 0% | Mandatory field di Odoo |
| res_partner | email | ~10% | Non-critical, tetap dipertahankan (NULL) |
| res_partner | phone | ~5% | Non-critical, tetap dipertahankan (NULL) |
| product_product | default_code | ~2% | Generate SKU otomatis jika NULL |

## Kesimpulan
Seluruh kolom kritikal (yang digunakan untuk KPI dan Star Schema) memiliki missing value rate 0% karena merupakan mandatory field di Odoo 18. Kolom non-kritikal (email, phone) memiliki missing value yang ditoleransi.
