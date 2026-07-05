# Star Schema Design

## Design Principles
- Mengikuti Kimball Dimensional Modeling.
- Surrogate key (sk_*) digunakan pada semua dimension table.
- Natural key Odoo (odoo_*_id) dipertahankan untuk traceability.
- Fact table berisi measures numerik dan foreign key ke dimensions.

## Fact Tables

### fact_sales
- **Grain:** 1 row per sale_order_line (confirmed)
- **Source:** sale_order JOIN sale_order_line WHERE state='sale'
- **Measures:** quantity, price_unit, discount, subtotal, revenue

### fact_purchase
- **Grain:** 1 row per purchase_order_line (confirmed)
- **Source:** purchase_order JOIN purchase_order_line WHERE state='purchase'
- **Measures:** quantity, price_unit, subtotal

### fact_inventory
- **Grain:** 1 row per stock_move (done)
- **Source:** stock_move WHERE state='done'
- **Measures:** quantity, value, movement_type (in/out)

### fact_accounting
- **Grain:** 1 row per account_move_line (posted)
- **Source:** account_move JOIN account_move_line WHERE state='posted'
- **Measures:** debit, credit

## Dimension Tables

### dim_date
- Generated calendar table (365 days × jumlah tahun simulasi).
- Kolom: date_id, full_date, year, month, day, month_name, quarter, day_of_week.

### dim_product
- Source: product_product JOIN product_template JOIN product_category.
- Kolom: sk_product_id, odoo_product_id, product_name, category, default_code, list_price, standard_price.

### dim_customer
- Source: res_partner WHERE customer_rank > 0.
- Kolom: sk_customer_id, odoo_partner_id, customer_name, city, industry.

### dim_vendor
- Source: res_partner WHERE supplier_rank > 0.
- Kolom: sk_vendor_id, odoo_partner_id, vendor_name, city.

### dim_company
- Source: res_company.
- Kolom: sk_company_id, odoo_company_id, company_name.

### dim_warehouse
- Source: stock_warehouse.
- Kolom: sk_warehouse_id, odoo_warehouse_id, warehouse_name, warehouse_code.
