# Dimension Dictionary

## dim_date
| Column | Type | PK | Description | Power BI Role |
| :--- | :--- | :---: | :--- | :--- |
| date_id | INTEGER | ✅ | Surrogate key (format YYYYMMDD, e.g. 20240115) | Date slicer key |
| full_date | DATE | | Tanggal lengkap | Date display |
| year | SMALLINT | | Tahun (e.g. 2024) | Year filter |
| month | SMALLINT | | Bulan (1–12) | Month sort |
| day | SMALLINT | | Hari (1–31) | Day drill-down |
| month_name | VARCHAR(20) | | Nama bulan ('January', 'February', ...) | Month display |
| quarter | SMALLINT | | Quarter (1–4) | Quarter filter |
| day_of_week | VARCHAR(20) | | Nama hari ('Monday', 'Tuesday', ...) | Weekday analysis |
| is_weekend | BOOLEAN | | True jika Sabtu/Minggu | Weekend filter |

---

## dim_product
| Column | Type | PK | Description | Power BI Role |
| :--- | :--- | :---: | :--- | :--- |
| sk_product_id | SERIAL | ✅ | Surrogate key | Relationship key |
| odoo_product_id | INTEGER | | Natural key (product_product.id) | Traceability |
| product_name | VARCHAR(255) | | Nama produk (dari product_template.name) | Product display |
| category | VARCHAR(255) | | Kategori produk (dari product_category.name) | Category filter |
| default_code | VARCHAR(100) | | SKU code (product_product.default_code) | SKU lookup |
| list_price | NUMERIC(15,2) | | Harga jual (selling price) | Price analysis |
| standard_price | NUMERIC(15,2) | | Harga pokok (cost price) | COGS & Inventory Valuation |

---

## dim_customer
| Column | Type | PK | Description | Power BI Role |
| :--- | :--- | :---: | :--- | :--- |
| sk_customer_id | SERIAL | ✅ | Surrogate key | Relationship key |
| odoo_partner_id | INTEGER | | Natural key (res_partner.id) | Traceability |
| customer_name | VARCHAR(255) | | Nama customer | Customer display |
| city | VARCHAR(100) | | Kota customer | Geographic filter |
| industry | VARCHAR(100) | | Industri (Konstruksi, Pertambangan, dsb) | Segment filter |

---

## dim_vendor
| Column | Type | PK | Description | Power BI Role |
| :--- | :--- | :---: | :--- | :--- |
| sk_vendor_id | SERIAL | ✅ | Surrogate key | Relationship key |
| odoo_partner_id | INTEGER | | Natural key (res_partner.id) | Traceability |
| vendor_name | VARCHAR(255) | | Nama vendor/supplier | Vendor display |
| city | VARCHAR(100) | | Kota vendor | Geographic filter |

---

## dim_company
| Column | Type | PK | Description | Power BI Role |
| :--- | :--- | :---: | :--- | :--- |
| sk_company_id | SERIAL | ✅ | Surrogate key | Relationship key |
| odoo_company_id | INTEGER | | Natural key (res_company.id) | Traceability |
| company_name | VARCHAR(255) | | Nama perusahaan | Company filter |

---

## dim_warehouse
| Column | Type | PK | Description | Power BI Role |
| :--- | :--- | :---: | :--- | :--- |
| sk_warehouse_id | SERIAL | ✅ | Surrogate key | Relationship key |
| odoo_warehouse_id | INTEGER | | Natural key (stock_warehouse.id) | Traceability |
| warehouse_name | VARCHAR(255) | | Nama gudang | Warehouse filter |
| warehouse_code | VARCHAR(10) | | Kode gudang | Short label |
