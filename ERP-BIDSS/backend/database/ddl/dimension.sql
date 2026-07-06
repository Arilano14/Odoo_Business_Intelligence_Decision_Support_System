-- ============================================================
-- OBIDSS Analytics Mart — Dimension Tables DDL
-- Database: PostgreSQL (same instance as Odoo 18)
-- Schema: mart
-- Compatible with: Odoo 18, Power BI Import Mode
-- ============================================================

CREATE SCHEMA IF NOT EXISTS mart;

-- ────────────────────────────────────────────────────────────
-- dim_date — Calendar Dimension (Generated)
-- Grain: 1 row per calendar day
-- ────────────────────────────────────────────────────────────
DROP TABLE IF EXISTS mart.dim_date CASCADE;
CREATE TABLE mart.dim_date (
    date_id         INTEGER     PRIMARY KEY,   -- Surrogate Key (format: YYYYMMDD)
    full_date       DATE        NOT NULL,
    year            SMALLINT    NOT NULL,
    month           SMALLINT    NOT NULL,
    day             SMALLINT    NOT NULL,
    month_name      VARCHAR(20) NOT NULL,      -- 'January', 'February', ...
    quarter         SMALLINT    NOT NULL,       -- 1, 2, 3, 4
    day_of_week     VARCHAR(20) NOT NULL,       -- 'Monday', 'Tuesday', ...
    is_weekend      BOOLEAN     NOT NULL DEFAULT FALSE
);

COMMENT ON TABLE  mart.dim_date IS 'Calendar dimension — 1 row per day. Generated programmatically.';
COMMENT ON COLUMN mart.dim_date.date_id IS 'Surrogate key in YYYYMMDD format (e.g. 20240115)';

-- ────────────────────────────────────────────────────────────
-- dim_product — Product Dimension
-- Source: product_product + product_template + product_category
-- Grain: 1 row per product variant
-- ────────────────────────────────────────────────────────────
DROP TABLE IF EXISTS mart.dim_product CASCADE;
CREATE TABLE mart.dim_product (
    sk_product_id   SERIAL      PRIMARY KEY,   -- Surrogate Key
    odoo_product_id INTEGER     NOT NULL,       -- Natural Key (product_product.id)
    product_name    VARCHAR(255) NOT NULL,      -- product_template.name
    category        VARCHAR(255),               -- product_category.name
    default_code    VARCHAR(100),               -- product_product.default_code (SKU)
    list_price      NUMERIC(15,2) DEFAULT 0,    -- Selling price
    standard_price  NUMERIC(15,2) DEFAULT 0,    -- Cost price (for COGS & Inventory Valuation)
    CONSTRAINT uq_dim_product_odoo_id UNIQUE (odoo_product_id)
);

COMMENT ON TABLE  mart.dim_product IS 'Product dimension — joined from product_product, product_template, product_category.';
COMMENT ON COLUMN mart.dim_product.standard_price IS 'Cost price used for COGS calculation and Inventory Valuation.';

-- ────────────────────────────────────────────────────────────
-- dim_customer — Customer Dimension
-- Source: res_partner WHERE customer_rank > 0
-- Grain: 1 row per customer partner
-- ────────────────────────────────────────────────────────────
DROP TABLE IF EXISTS mart.dim_customer CASCADE;
CREATE TABLE mart.dim_customer (
    sk_customer_id  SERIAL      PRIMARY KEY,   -- Surrogate Key
    odoo_partner_id INTEGER     NOT NULL,       -- Natural Key (res_partner.id)
    customer_name   VARCHAR(255) NOT NULL,
    city            VARCHAR(100),
    industry        VARCHAR(100),               -- Derived from partner category/tag
    CONSTRAINT uq_dim_customer_odoo_id UNIQUE (odoo_partner_id)
);

COMMENT ON TABLE mart.dim_customer IS 'Customer dimension — res_partner where customer_rank > 0.';

-- ────────────────────────────────────────────────────────────
-- dim_vendor — Vendor/Supplier Dimension
-- Source: res_partner WHERE supplier_rank > 0
-- Grain: 1 row per vendor partner
-- ────────────────────────────────────────────────────────────
DROP TABLE IF EXISTS mart.dim_vendor CASCADE;
CREATE TABLE mart.dim_vendor (
    sk_vendor_id    SERIAL      PRIMARY KEY,   -- Surrogate Key
    odoo_partner_id INTEGER     NOT NULL,       -- Natural Key (res_partner.id)
    vendor_name     VARCHAR(255) NOT NULL,
    city            VARCHAR(100),
    CONSTRAINT uq_dim_vendor_odoo_id UNIQUE (odoo_partner_id)
);

COMMENT ON TABLE mart.dim_vendor IS 'Vendor/Supplier dimension — res_partner where supplier_rank > 0.';

-- ────────────────────────────────────────────────────────────
-- dim_company — Company Dimension
-- Source: res_company
-- Grain: 1 row per company
-- ────────────────────────────────────────────────────────────
DROP TABLE IF EXISTS mart.dim_company CASCADE;
CREATE TABLE mart.dim_company (
    sk_company_id   SERIAL      PRIMARY KEY,   -- Surrogate Key
    odoo_company_id INTEGER     NOT NULL,       -- Natural Key (res_company.id)
    company_name    VARCHAR(255) NOT NULL,
    CONSTRAINT uq_dim_company_odoo_id UNIQUE (odoo_company_id)
);

COMMENT ON TABLE mart.dim_company IS 'Company dimension — res_company. Single company for MVP.';

-- ────────────────────────────────────────────────────────────
-- dim_warehouse — Warehouse Dimension
-- Source: stock_warehouse
-- Grain: 1 row per warehouse
-- ────────────────────────────────────────────────────────────
DROP TABLE IF EXISTS mart.dim_warehouse CASCADE;
CREATE TABLE mart.dim_warehouse (
    sk_warehouse_id   SERIAL      PRIMARY KEY,   -- Surrogate Key
    odoo_warehouse_id INTEGER     NOT NULL,       -- Natural Key (stock_warehouse.id)
    warehouse_name    VARCHAR(255) NOT NULL,
    warehouse_code    VARCHAR(10),
    CONSTRAINT uq_dim_warehouse_odoo_id UNIQUE (odoo_warehouse_id)
);

COMMENT ON TABLE mart.dim_warehouse IS 'Warehouse dimension — stock_warehouse.';
