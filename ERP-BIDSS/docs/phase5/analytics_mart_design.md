# Analytics Mart Design

## Overview
Analytics Mart merupakan lapisan data analitik (OLAP) yang dibangun di atas data operasional Odoo 18 (OLTP). Mart ini menggunakan Star Schema (Kimball) dan berada di PostgreSQL schema `mart` pada database yang sama dengan Odoo.

## Architecture
```
Odoo 18 PostgreSQL (public schema)
    │
    ├── sale_order, sale_order_line
    ├── purchase_order, purchase_order_line
    ├── stock_move, stock_quant
    ├── account_move, account_move_line
    ├── product_product, product_template, product_category
    ├── res_partner, res_company
    └── stock_warehouse
         │
         ▼  [Python ETL: Extract → Transform → Load]
         │
Analytics Mart (mart schema)
    │
    ├── dim_date          (365 rows — generated)
    ├── dim_product       (500 rows — from product_*)
    ├── dim_customer      (300 rows — from res_partner)
    ├── dim_vendor        (300 rows — from res_partner)
    ├── dim_company       (1 row   — from res_company)
    ├── dim_warehouse     (5 rows  — from stock_warehouse)
    ├── fact_sales        (~6.000 rows)
    ├── fact_purchase     (~2.000 rows)
    ├── fact_inventory    (~10.000 rows)
    └── fact_accounting   (~10.000 rows)
         │
         ▼  [Power BI Import Mode]
         │
    Dashboard (5 pages)
```

## Design Principles
1. **Star Schema Only** — tidak menggunakan Snowflake, Galaxy, atau Bridge Table.
2. **Surrogate Key** — semua dimension menggunakan surrogate key (sk_* atau date_id).
3. **Natural Key Preserved** — odoo_*_id dipertahankan untuk traceability.
4. **Fact = Immutable** — fact table hanya berisi event yang sudah terjadi.
5. **SCD Type 1** — overwrite untuk MVP (tidak ada history tracking).
6. **Full Refresh** — truncate & reload pada setiap ETL run.
7. **Derived Metrics** — revenue, cost, margin, lead_time_days, movement_type, source_module dihitung saat ETL.

## Power BI Compatibility
- Column names menggunakan snake_case (Power BI auto-format ke Title Case).
- NULL values diisi dengan default (0 untuk numerik, 'Unknown' untuk string).
- Data types menggunakan NUMERIC(15,2) untuk monetary values (presisi 2 desimal).
- Relationship auto-detect di Power BI melalui naming convention (date_id, product_id, dsb).
