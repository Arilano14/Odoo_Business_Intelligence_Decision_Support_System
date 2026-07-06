-- ============================================================
-- OBIDSS Analytics Mart — Sample Queries
-- These queries validate that mart tables support all KPIs.
-- Compatible with Power BI DirectQuery / Import Mode.
-- ============================================================

-- ── KPI 1: Total Revenue ────────────────────────────────────
SELECT
    SUM(fs.revenue) AS total_revenue
FROM mart.fact_sales fs;

-- ── KPI 2: Sales Growth (Month-over-Month) ──────────────────
SELECT
    d.year,
    d.month,
    d.month_name,
    SUM(fs.revenue) AS monthly_revenue,
    LAG(SUM(fs.revenue)) OVER (ORDER BY d.year, d.month) AS prev_month_revenue,
    ROUND(
        (SUM(fs.revenue) - LAG(SUM(fs.revenue)) OVER (ORDER BY d.year, d.month))
        / NULLIF(LAG(SUM(fs.revenue)) OVER (ORDER BY d.year, d.month), 0) * 100,
        2
    ) AS sales_growth_pct
FROM mart.fact_sales fs
JOIN mart.dim_date d ON fs.date_id = d.date_id
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;

-- ── KPI 3: Inventory Turnover ───────────────────────────────
-- Simplified: COGS proxy (total cost from sales) / Average Inventory Value
SELECT
    ROUND(
        SUM(fs.cost) / NULLIF(AVG(inv.inventory_value), 0),
        2
    ) AS inventory_turnover
FROM mart.fact_sales fs
CROSS JOIN (
    SELECT SUM(fi.value) AS inventory_value
    FROM mart.fact_inventory fi
    WHERE fi.movement_type = 'incoming'
) inv;

-- ── KPI 5: Revenue Contribution per Product ─────────────────
SELECT
    dp.product_name,
    dp.category,
    SUM(fs.revenue) AS product_revenue,
    ROUND(
        SUM(fs.revenue) / NULLIF((SELECT SUM(revenue) FROM mart.fact_sales), 0) * 100,
        2
    ) AS contribution_pct
FROM mart.fact_sales fs
JOIN mart.dim_product dp ON fs.product_id = dp.sk_product_id
GROUP BY dp.product_name, dp.category
ORDER BY product_revenue DESC
LIMIT 20;

-- ── KPI 7: Purchase Value per Month ─────────────────────────
SELECT
    d.month_name,
    SUM(fp.subtotal) AS purchase_value,
    AVG(fp.lead_time_days) AS avg_lead_time
FROM mart.fact_purchase fp
JOIN mart.dim_date d ON fp.date_id = d.date_id
GROUP BY d.month, d.month_name
ORDER BY d.month;

-- ── KPI 11: Supplier Performance Data ───────────────────────
-- (Weighted scoring will be calculated in Phase 7 Decision Support)
SELECT
    dv.vendor_name,
    COUNT(fp.sk_purchase_id) AS total_orders,
    AVG(fp.lead_time_days) AS avg_lead_time,
    SUM(fp.subtotal) AS total_purchase_value
FROM mart.fact_purchase fp
JOIN mart.dim_vendor dv ON fp.vendor_id = dv.sk_vendor_id
GROUP BY dv.vendor_name
ORDER BY total_purchase_value DESC;

-- ── KPI 12: Demand Forecast Input (Monthly Qty) ─────────────
SELECT
    d.year,
    d.month,
    d.month_name,
    dp.product_name,
    SUM(fs.quantity) AS monthly_qty
FROM mart.fact_sales fs
JOIN mart.dim_date d ON fs.date_id = d.date_id
JOIN mart.dim_product dp ON fs.product_id = dp.sk_product_id
GROUP BY d.year, d.month, d.month_name, dp.product_name
ORDER BY dp.product_name, d.year, d.month;

-- ── Accounting: Revenue vs Purchase by Module ───────────────
SELECT
    fa.source_module,
    SUM(fa.debit) AS total_debit,
    SUM(fa.credit) AS total_credit,
    SUM(fa.debit) - SUM(fa.credit) AS net_balance
FROM mart.fact_accounting fa
GROUP BY fa.source_module
ORDER BY fa.source_module;

-- ── Inventory Movement Summary ──────────────────────────────
SELECT
    d.month_name,
    fi.movement_type,
    SUM(fi.quantity) AS total_qty,
    SUM(fi.value) AS total_value
FROM mart.fact_inventory fi
JOIN mart.dim_date d ON fi.date_id = d.date_id
GROUP BY d.month, d.month_name, fi.movement_type
ORDER BY d.month, fi.movement_type;

-- ── Top Customers by Revenue ────────────────────────────────
SELECT
    dc.customer_name,
    dc.city,
    SUM(fs.revenue) AS total_revenue,
    SUM(fs.margin) AS total_margin,
    COUNT(fs.sk_sales_id) AS total_transactions
FROM mart.fact_sales fs
JOIN mart.dim_customer dc ON fs.customer_id = dc.sk_customer_id
GROUP BY dc.customer_name, dc.city
ORDER BY total_revenue DESC
LIMIT 10;
