# Data Loading Strategy

## Strategy: Full Refresh (Truncate & Load)

Untuk MVP (laporan magang S1), strategi loading yang digunakan adalah **Full Refresh**:
1. Truncate seluruh tabel di schema 'mart'.
2. Load ulang seluruh data dari hasil transformasi.

### Alasan
- Sederhana dan mudah diimplementasikan.
- Volume data ≈ 30.000 rows masih sangat kecil untuk full refresh.
- Menghindari kompleksitas SCD Type 2 dan incremental load.

## Loading Order
Dimension tables harus dimuat terlebih dahulu sebelum Fact tables (karena FK dependency).

```
1. dim_date
2. dim_product
3. dim_customer
4. dim_vendor
5. dim_company
6. dim_warehouse
7. fact_sales
8. fact_purchase
9. fact_inventory
10. fact_accounting
```

## Target Schema
- **Schema name:** mart
- **Database:** PostgreSQL (sama dengan Odoo, schema terpisah)
- **Method:** pandas.DataFrame.to_sql(schema='mart', if_exists='replace')
