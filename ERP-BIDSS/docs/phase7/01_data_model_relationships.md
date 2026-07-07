# 01. Data Model Relationships (Power BI Semantic Model)

Dokumen ini mendefinisikan hubungan antar tabel (Star Schema) setelah di-import dari skema mart PostgreSQL ke dalam Power BI Desktop.

## Star Schema Overview
Analytics Mart menggunakan model Star Schema klasik dengan 4 Fact Table yang berada di tengah, dan 5 Dimension Table yang mengelilinginya.

### Dimension Tables (Lookup Tables)
- dim_date (1)
- dim_product (1)
- dim_customer (1)
- dim_vendor (1)
- dim_warehouse (1)

### Fact Tables (Data Tables)
- act_sales (*)
- act_purchase (*)
- act_inventory (*)
- act_accounting (*)

---

## Relationship Mapping

Semua relasi bersifat **1-to-Many (1:*)** dengan arah filter **Single (Cross filter direction: Single)** dari Dimension ke Fact.

| From Table (1) | From Column | To Table (*) | To Column | Active |
| :--- | :--- | :--- | :--- | :--- |
| **dim_date** | date_id | **fact_sales** | date_id | Yes |
| **dim_date** | date_id | **fact_purchase** | date_id | Yes |
| **dim_date** | date_id | **fact_inventory**| date_id | Yes |
| **dim_date** | date_id | **fact_accounting**| date_id | Yes |
| **dim_product** | sk_product_id| **fact_sales** | product_id | Yes |
| **dim_product** | sk_product_id| **fact_purchase** | product_id | Yes |
| **dim_product** | sk_product_id| **fact_inventory**| product_id | Yes |
| **dim_customer**| sk_customer_id| **fact_sales** | customer_id | Yes |
| **dim_vendor** | sk_vendor_id| **fact_purchase** | endor_id | Yes |
| **dim_warehouse**| sk_warehouse_id| **fact_inventory**| warehouse_id | Yes |

---

## Power BI Specific Configurations

### 1. Mark as Date Table
- Pilih tabel dim_date.
- Buka tab *Table tools* > **Mark as date table**.
- Pilih kolom ull_date (tipe data Date).
- *Alasan*: Untuk memastikan fungsi Time Intelligence DAX (seperti YTD, MTD, MoM) berjalan sempurna tanpa membuat kalender otomatis (Auto date/time) yang membebani model.

### 2. Hide Surrogate Keys & Foreign Keys
- Sembunyikan (*Hide in report view*) semua kolom Surrogate Key (contoh: sk_product_id, date_id, product_id di Fact Table) agar user tidak bingung saat drag-and-drop visual. User hanya perlu melihat atribut deskriptif seperti product_name.

### 3. Disable Auto Date/Time
- File > Options and settings > Options > Current File > Data Load.
- Uncheck **Auto date/time**.
- *Alasan*: Karena kita sudah mempunyai dim_date kustom yang lebih komprehensif.
