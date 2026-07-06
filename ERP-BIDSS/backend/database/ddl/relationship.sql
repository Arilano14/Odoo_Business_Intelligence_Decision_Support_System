-- ============================================================
-- OBIDSS Analytics Mart — Foreign Key Relationships
-- Ensures referential integrity between Fact ↔ Dimension
-- ============================================================

-- ── fact_sales relationships ────────────────────────────────
ALTER TABLE mart.fact_sales
    ADD CONSTRAINT fk_fact_sales_date
        FOREIGN KEY (date_id) REFERENCES mart.dim_date(date_id),
    ADD CONSTRAINT fk_fact_sales_product
        FOREIGN KEY (product_id) REFERENCES mart.dim_product(sk_product_id),
    ADD CONSTRAINT fk_fact_sales_customer
        FOREIGN KEY (customer_id) REFERENCES mart.dim_customer(sk_customer_id),
    ADD CONSTRAINT fk_fact_sales_company
        FOREIGN KEY (company_id) REFERENCES mart.dim_company(sk_company_id);

-- ── fact_purchase relationships ─────────────────────────────
ALTER TABLE mart.fact_purchase
    ADD CONSTRAINT fk_fact_purchase_date
        FOREIGN KEY (date_id) REFERENCES mart.dim_date(date_id),
    ADD CONSTRAINT fk_fact_purchase_product
        FOREIGN KEY (product_id) REFERENCES mart.dim_product(sk_product_id),
    ADD CONSTRAINT fk_fact_purchase_vendor
        FOREIGN KEY (vendor_id) REFERENCES mart.dim_vendor(sk_vendor_id),
    ADD CONSTRAINT fk_fact_purchase_company
        FOREIGN KEY (company_id) REFERENCES mart.dim_company(sk_company_id);

-- ── fact_inventory relationships ────────────────────────────
ALTER TABLE mart.fact_inventory
    ADD CONSTRAINT fk_fact_inventory_date
        FOREIGN KEY (date_id) REFERENCES mart.dim_date(date_id),
    ADD CONSTRAINT fk_fact_inventory_product
        FOREIGN KEY (product_id) REFERENCES mart.dim_product(sk_product_id),
    ADD CONSTRAINT fk_fact_inventory_warehouse
        FOREIGN KEY (warehouse_id) REFERENCES mart.dim_warehouse(sk_warehouse_id);

-- ── fact_accounting relationships ───────────────────────────
ALTER TABLE mart.fact_accounting
    ADD CONSTRAINT fk_fact_accounting_date
        FOREIGN KEY (date_id) REFERENCES mart.dim_date(date_id),
    ADD CONSTRAINT fk_fact_accounting_company
        FOREIGN KEY (company_id) REFERENCES mart.dim_company(sk_company_id);
