# Star Schema Final

## Final Star Schema — Analytics Mart (schema: mart)

```mermaid
erDiagram
    dim_date ||--o{ fact_sales : "date_id"
    dim_product ||--o{ fact_sales : "product_id"
    dim_customer ||--o{ fact_sales : "customer_id"
    dim_company ||--o{ fact_sales : "company_id"

    dim_date ||--o{ fact_purchase : "date_id"
    dim_product ||--o{ fact_purchase : "product_id"
    dim_vendor ||--o{ fact_purchase : "vendor_id"
    dim_company ||--o{ fact_purchase : "company_id"

    dim_date ||--o{ fact_inventory : "date_id"
    dim_product ||--o{ fact_inventory : "product_id"
    dim_warehouse ||--o{ fact_inventory : "warehouse_id"

    dim_date ||--o{ fact_accounting : "date_id"
    dim_company ||--o{ fact_accounting : "company_id"

    fact_sales {
        SERIAL sk_sales_id PK
        INTEGER date_id FK
        INTEGER product_id FK
        INTEGER customer_id FK
        INTEGER company_id FK
        NUMERIC quantity
        NUMERIC price_unit
        NUMERIC discount
        NUMERIC subtotal
        NUMERIC revenue "DERIVED"
        NUMERIC cost "DERIVED"
        NUMERIC margin "DERIVED"
    }

    fact_purchase {
        SERIAL sk_purchase_id PK
        INTEGER date_id FK
        INTEGER product_id FK
        INTEGER vendor_id FK
        INTEGER company_id FK
        NUMERIC quantity
        NUMERIC price_unit
        NUMERIC subtotal
        INTEGER lead_time_days "DERIVED"
    }

    fact_inventory {
        SERIAL sk_inventory_id PK
        INTEGER date_id FK
        INTEGER product_id FK
        INTEGER warehouse_id FK
        NUMERIC quantity
        NUMERIC value "DERIVED"
        VARCHAR movement_type "DERIVED"
        VARCHAR reference
    }

    fact_accounting {
        SERIAL sk_accounting_id PK
        INTEGER date_id FK
        INTEGER company_id FK
        NUMERIC debit
        NUMERIC credit
        VARCHAR account_name
        VARCHAR move_type
        VARCHAR source_module "DERIVED"
    }

    dim_date {
        INTEGER date_id PK
        DATE full_date
        SMALLINT year
        SMALLINT month
        SMALLINT day
        VARCHAR month_name
        SMALLINT quarter
        VARCHAR day_of_week
        BOOLEAN is_weekend
    }

    dim_product {
        SERIAL sk_product_id PK
        INTEGER odoo_product_id
        VARCHAR product_name
        VARCHAR category
        VARCHAR default_code
        NUMERIC list_price
        NUMERIC standard_price
    }

    dim_customer {
        SERIAL sk_customer_id PK
        INTEGER odoo_partner_id
        VARCHAR customer_name
        VARCHAR city
        VARCHAR industry
    }

    dim_vendor {
        SERIAL sk_vendor_id PK
        INTEGER odoo_partner_id
        VARCHAR vendor_name
        VARCHAR city
    }

    dim_company {
        SERIAL sk_company_id PK
        INTEGER odoo_company_id
        VARCHAR company_name
    }

    dim_warehouse {
        SERIAL sk_warehouse_id PK
        INTEGER odoo_warehouse_id
        VARCHAR warehouse_name
        VARCHAR warehouse_code
    }
```

## Relationship Summary (13 FK)

| # | Fact | FK Column | Dim | PK Column | Cardinality |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | fact_sales | date_id | dim_date | date_id | N:1 |
| 2 | fact_sales | product_id | dim_product | sk_product_id | N:1 |
| 3 | fact_sales | customer_id | dim_customer | sk_customer_id | N:1 |
| 4 | fact_sales | company_id | dim_company | sk_company_id | N:1 |
| 5 | fact_purchase | date_id | dim_date | date_id | N:1 |
| 6 | fact_purchase | product_id | dim_product | sk_product_id | N:1 |
| 7 | fact_purchase | vendor_id | dim_vendor | sk_vendor_id | N:1 |
| 8 | fact_purchase | company_id | dim_company | sk_company_id | N:1 |
| 9 | fact_inventory | date_id | dim_date | date_id | N:1 |
| 10 | fact_inventory | product_id | dim_product | sk_product_id | N:1 |
| 11 | fact_inventory | warehouse_id | dim_warehouse | sk_warehouse_id | N:1 |
| 12 | fact_accounting | date_id | dim_date | date_id | N:1 |
| 13 | fact_accounting | company_id | dim_company | sk_company_id | N:1 |

## Catatan untuk Power BI
- Power BI akan auto-detect relationship berdasarkan nama kolom yang sama (date_id, product_id, dsb).
- Semua relationship bertipe **Many-to-One** (Fact → Dimension).
- Tidak ada relationship Fact-to-Fact (sesuai Kimball).
- Cross-filter direction: **Single** (dari Dimension ke Fact).
