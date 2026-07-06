-- ============================================================
-- OBIDSS Analytics Mart — Performance Indexes
-- Optimized for Power BI Import Mode query patterns
-- ============================================================

-- ── Dimension Indexes (lookup by natural key) ───────────────
CREATE INDEX IF NOT EXISTS idx_dim_product_odoo_id   ON mart.dim_product(odoo_product_id);
CREATE INDEX IF NOT EXISTS idx_dim_customer_odoo_id  ON mart.dim_customer(odoo_partner_id);
CREATE INDEX IF NOT EXISTS idx_dim_vendor_odoo_id    ON mart.dim_vendor(odoo_partner_id);
CREATE INDEX IF NOT EXISTS idx_dim_company_odoo_id   ON mart.dim_company(odoo_company_id);
CREATE INDEX IF NOT EXISTS idx_dim_warehouse_odoo_id ON mart.dim_warehouse(odoo_warehouse_id);

-- ── Fact Indexes (filter by date + dimension FK) ────────────
-- fact_sales
CREATE INDEX IF NOT EXISTS idx_fact_sales_date       ON mart.fact_sales(date_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_product    ON mart.fact_sales(product_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_customer   ON mart.fact_sales(customer_id);

-- fact_purchase
CREATE INDEX IF NOT EXISTS idx_fact_purchase_date    ON mart.fact_purchase(date_id);
CREATE INDEX IF NOT EXISTS idx_fact_purchase_product ON mart.fact_purchase(product_id);
CREATE INDEX IF NOT EXISTS idx_fact_purchase_vendor  ON mart.fact_purchase(vendor_id);

-- fact_inventory
CREATE INDEX IF NOT EXISTS idx_fact_inventory_date      ON mart.fact_inventory(date_id);
CREATE INDEX IF NOT EXISTS idx_fact_inventory_product   ON mart.fact_inventory(product_id);
CREATE INDEX IF NOT EXISTS idx_fact_inventory_warehouse ON mart.fact_inventory(warehouse_id);
CREATE INDEX IF NOT EXISTS idx_fact_inventory_type      ON mart.fact_inventory(movement_type);

-- fact_accounting
CREATE INDEX IF NOT EXISTS idx_fact_accounting_date     ON mart.fact_accounting(date_id);
CREATE INDEX IF NOT EXISTS idx_fact_accounting_type     ON mart.fact_accounting(move_type);
