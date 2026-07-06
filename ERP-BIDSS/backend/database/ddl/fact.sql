-- ============================================================
-- OBIDSS Analytics Mart — Fact Tables DDL
-- Database: PostgreSQL (same instance as Odoo 18)
-- Schema: mart
-- Compatible with: Odoo 18, Power BI Import Mode
-- ============================================================

-- ────────────────────────────────────────────────────────────
-- fact_sales — Sales Fact
-- Source: sale_order JOIN sale_order_line WHERE state='sale'
-- Grain: 1 row per confirmed sale_order_line
-- ────────────────────────────────────────────────────────────
DROP TABLE IF EXISTS mart.fact_sales CASCADE;
CREATE TABLE mart.fact_sales (
    sk_sales_id     SERIAL          PRIMARY KEY,
    date_id         INTEGER         NOT NULL,       -- FK → dim_date
    product_id      INTEGER         NOT NULL,       -- FK → dim_product
    customer_id     INTEGER         NOT NULL,       -- FK → dim_customer
    company_id      INTEGER         NOT NULL,       -- FK → dim_company

    -- Measures
    quantity        NUMERIC(15,4)   NOT NULL DEFAULT 0,
    price_unit      NUMERIC(15,2)   NOT NULL DEFAULT 0,
    discount        NUMERIC(5,2)    DEFAULT 0,       -- Percentage (0-100)
    subtotal        NUMERIC(15,2)   NOT NULL DEFAULT 0,  -- price_subtotal from Odoo
    revenue         NUMERIC(15,2)   NOT NULL DEFAULT 0,  -- qty × price × (1 - discount/100)
    cost            NUMERIC(15,2)   DEFAULT 0,       -- qty × standard_price (for margin)
    margin          NUMERIC(15,2)   DEFAULT 0        -- revenue - cost
);

COMMENT ON TABLE  mart.fact_sales IS 'Sales fact — 1 row per sale_order_line. Only confirmed orders (state=sale).';
COMMENT ON COLUMN mart.fact_sales.revenue IS 'Calculated: quantity × price_unit × (1 - discount/100)';
COMMENT ON COLUMN mart.fact_sales.cost IS 'Calculated: quantity × dim_product.standard_price';
COMMENT ON COLUMN mart.fact_sales.margin IS 'Calculated: revenue - cost';

-- ────────────────────────────────────────────────────────────
-- fact_purchase — Purchase Fact
-- Source: purchase_order JOIN purchase_order_line WHERE state='purchase'
-- Grain: 1 row per confirmed purchase_order_line
-- ────────────────────────────────────────────────────────────
DROP TABLE IF EXISTS mart.fact_purchase CASCADE;
CREATE TABLE mart.fact_purchase (
    sk_purchase_id  SERIAL          PRIMARY KEY,
    date_id         INTEGER         NOT NULL,       -- FK → dim_date
    product_id      INTEGER         NOT NULL,       -- FK → dim_product
    vendor_id       INTEGER         NOT NULL,       -- FK → dim_vendor
    company_id      INTEGER         NOT NULL,       -- FK → dim_company

    -- Measures
    quantity        NUMERIC(15,4)   NOT NULL DEFAULT 0,
    price_unit      NUMERIC(15,2)   NOT NULL DEFAULT 0,
    subtotal        NUMERIC(15,2)   NOT NULL DEFAULT 0,
    lead_time_days  INTEGER         DEFAULT 0        -- date_planned - date_order (days)
);

COMMENT ON TABLE  mart.fact_purchase IS 'Purchase fact — 1 row per purchase_order_line. Only confirmed orders (state=purchase).';
COMMENT ON COLUMN mart.fact_purchase.lead_time_days IS 'Calculated: date_planned - date_order in days.';

-- ────────────────────────────────────────────────────────────
-- fact_inventory — Inventory Movement Fact
-- Source: stock_move WHERE state='done'
-- Grain: 1 row per completed stock movement
-- ────────────────────────────────────────────────────────────
DROP TABLE IF EXISTS mart.fact_inventory CASCADE;
CREATE TABLE mart.fact_inventory (
    sk_inventory_id SERIAL          PRIMARY KEY,
    date_id         INTEGER         NOT NULL,       -- FK → dim_date
    product_id      INTEGER         NOT NULL,       -- FK → dim_product
    warehouse_id    INTEGER         NOT NULL,       -- FK → dim_warehouse

    -- Measures
    quantity        NUMERIC(15,4)   NOT NULL DEFAULT 0,
    value           NUMERIC(15,2)   DEFAULT 0,       -- quantity × standard_price
    movement_type   VARCHAR(20)     NOT NULL,         -- 'incoming' or 'outgoing'
    reference       VARCHAR(100)                      -- stock_move.reference (SO/PO link)
);

COMMENT ON TABLE  mart.fact_inventory IS 'Inventory movement fact — 1 row per stock_move (state=done).';
COMMENT ON COLUMN mart.fact_inventory.movement_type IS 'incoming = goods receipt, outgoing = delivery';
COMMENT ON COLUMN mart.fact_inventory.value IS 'Calculated: quantity × dim_product.standard_price';

-- ────────────────────────────────────────────────────────────
-- fact_accounting — Accounting Journal Fact
-- Source: account_move JOIN account_move_line WHERE state='posted'
-- Grain: 1 row per posted account_move_line
-- ────────────────────────────────────────────────────────────
DROP TABLE IF EXISTS mart.fact_accounting CASCADE;
CREATE TABLE mart.fact_accounting (
    sk_accounting_id SERIAL         PRIMARY KEY,
    date_id          INTEGER        NOT NULL,       -- FK → dim_date
    company_id       INTEGER        NOT NULL,       -- FK → dim_company

    -- Measures
    debit            NUMERIC(15,2)  NOT NULL DEFAULT 0,
    credit           NUMERIC(15,2)  NOT NULL DEFAULT 0,
    account_name     VARCHAR(255),                   -- account name/label
    move_type        VARCHAR(30),                    -- out_invoice, in_invoice, entry, etc.
    source_module    VARCHAR(30)                     -- derived: 'sales', 'purchase', 'manual'
);

COMMENT ON TABLE  mart.fact_accounting IS 'Accounting journal fact — 1 row per account_move_line (posted only).';
COMMENT ON COLUMN mart.fact_accounting.source_module IS 'Derived from move_type: out_invoice→sales, in_invoice→purchase, entry→manual.';
