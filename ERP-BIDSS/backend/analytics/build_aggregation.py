import pandas as pd
import datetime
from config.database import db
from config.settings import settings

def build_monthly_summary(engine):
    """Build mart.monthly_summary for Sales, Purchase, and Forecast KPIs."""
    query = """
    WITH sales_agg AS (
        SELECT 
            LEFT(CAST(fs.date_id AS VARCHAR), 6) AS month_id,
            SUM(fs.revenue) AS revenue,
            SUM(fs.cost) AS cost,
            SUM(fs.margin) AS margin,
            COUNT(DISTINCT fs.sk_sales_id) AS total_sales_trx
        FROM mart.fact_sales fs
        GROUP BY 1
    ),
    purchase_agg AS (
        SELECT 
            LEFT(CAST(fp.date_id AS VARCHAR), 6) AS month_id,
            SUM(fp.subtotal) AS purchase_total,
            COUNT(*) AS purchase_lines,
            AVG(fp.lead_time_days) AS avg_lead_time,
            SUM(CASE WHEN fp.lead_time_days <= 5 THEN 1 ELSE 0 END) AS on_time_lines
        FROM mart.fact_purchase fp
        GROUP BY 1
    ),
    forecast_agg AS (
        SELECT 
            CAST(ff.month_id AS VARCHAR) AS month_id,
            AVG(ABS(ff.actual_qty - ff.ma3_forecast) / NULLIF(ff.actual_qty, 0)) AS error_rate
        FROM mart.fact_forecast_monthly ff
        GROUP BY 1
    ),
    inv_agg AS (
        SELECT 
            LEFT(CAST(fi.date_id AS VARCHAR), 6) AS month_id,
            SUM(CASE WHEN fi.movement_type = 'incoming' THEN fi.value ELSE -fi.value END) AS net_movement_value
        FROM mart.fact_inventory fi
        GROUP BY 1
    ),
    supplier_agg AS (
        SELECT AVG(final_score) AS supplier_avg_score
        FROM mart.fact_supplier_score
    ),
    dim_months AS (
        SELECT DISTINCT 
            LEFT(CAST(date_id AS VARCHAR), 6) AS month_id,
            month_name
        FROM mart.dim_date
    )
    SELECT 
        dm.month_id,
        dm.month_name,
        COALESCE(sa.revenue, 0) AS revenue,
        COALESCE(sa.cost, 0) AS cost,
        COALESCE(sa.margin, 0) AS margin,
        CASE WHEN COALESCE(sa.revenue, 0) = 0 THEN 0 ELSE (sa.margin / sa.revenue) * 100 END AS margin_pct,
        COALESCE(sa.total_sales_trx, 0) AS total_sales_trx,
        CASE WHEN COALESCE(sa.total_sales_trx, 0) = 0 THEN 0 ELSE (sa.revenue / sa.total_sales_trx) END AS avg_order_value,
        COALESCE(pa.purchase_total, 0) AS purchase_total,
        COALESCE(pa.purchase_lines, 0) AS purchase_lines,
        COALESCE(pa.avg_lead_time, 0) AS avg_lead_time,
        CASE WHEN COALESCE(pa.purchase_lines, 0) = 0 THEN 0 ELSE (CAST(pa.on_time_lines AS FLOAT) / pa.purchase_lines) END AS on_time_rate,
        CASE WHEN COALESCE(sa.revenue, 0) = 0 THEN 0 ELSE (pa.purchase_total / sa.revenue) END AS procurement_ratio,
        CASE WHEN fa.error_rate IS NULL THEN 1 ELSE GREATEST(0, 1 - fa.error_rate) END AS forecast_accuracy,
        COALESCE(ia.net_movement_value, 0) AS inventory_value,
        (SELECT supplier_avg_score FROM supplier_agg) AS supplier_avg_score
    FROM dim_months dm
    LEFT JOIN sales_agg sa ON dm.month_id = sa.month_id
    LEFT JOIN purchase_agg pa ON dm.month_id = pa.month_id
    LEFT JOIN forecast_agg fa ON dm.month_id = fa.month_id
    LEFT JOIN inv_agg ia ON dm.month_id = ia.month_id
    WHERE sa.revenue IS NOT NULL OR pa.purchase_total IS NOT NULL
    ORDER BY dm.month_id;
    """
    try:
        df = pd.read_sql(query, engine)
        print(f"  [OK] monthly_summary: {len(df)} rows")
        df['prev_revenue'] = df['revenue'].shift(1)
        df['revenue_growth_pct'] = ((df['revenue'] - df['prev_revenue']) / df['prev_revenue'] * 100).fillna(0)
        df.drop(columns=['prev_revenue'], inplace=True)
        return df
    except Exception as e:
        print(f"  [FAIL] monthly_summary: {e}")
        return pd.DataFrame()

def build_inventory_monthly_summary(engine):
    """Build mart.inventory_monthly_summary for Inventory KPIs."""
    query = """
    WITH inv_agg AS (
        SELECT 
            LEFT(CAST(fi.date_id AS VARCHAR), 6) AS month_id,
            SUM(CASE WHEN fi.movement_type = 'incoming' THEN fi.quantity ELSE 0 END) AS incoming_qty,
            SUM(CASE WHEN fi.movement_type = 'outgoing' THEN fi.quantity ELSE 0 END) AS outgoing_qty,
            SUM(CASE WHEN fi.movement_type = 'incoming' THEN fi.value ELSE 0 END) AS incoming_value,
            SUM(CASE WHEN fi.movement_type = 'outgoing' THEN fi.value ELSE 0 END) AS outgoing_value
        FROM mart.fact_inventory fi
        GROUP BY 1
    ),
    dim_months AS (
        SELECT DISTINCT 
            LEFT(CAST(date_id AS VARCHAR), 6) AS month_id
        FROM mart.dim_date
    )
    SELECT 
        dm.month_id,
        COALESCE(ia.incoming_qty, 0) AS incoming_qty,
        COALESCE(ia.outgoing_qty, 0) AS outgoing_qty,
        COALESCE(ia.incoming_value, 0) AS incoming_value,
        COALESCE(ia.outgoing_value, 0) AS outgoing_value,
        COALESCE(ia.incoming_value, 0) - COALESCE(ia.outgoing_value, 0) AS net_stock_movement_value
    FROM dim_months dm
    LEFT JOIN inv_agg ia ON dm.month_id = ia.month_id
    WHERE ia.incoming_qty > 0 OR ia.outgoing_qty > 0
    ORDER BY dm.month_id;
    """
    try:
        df = pd.read_sql(query, engine)
        print(f"  [OK] inventory_monthly_summary: {len(df)} rows")
        return df
    except Exception as e:
        print(f"  [FAIL] inventory_monthly_summary: {e}")
        return pd.DataFrame()

def build_supplier_summary(engine):
    query = """
    WITH purchase_stats AS (
        SELECT 
            vendor_id,
            SUM(subtotal) AS purchase_value,
            SUM(quantity) AS purchase_qty
        FROM mart.fact_purchase
        GROUP BY vendor_id
    ),
    total_purchase AS (
        SELECT SUM(subtotal) as global_purchase_value FROM mart.fact_purchase
    )
    SELECT 
        fss.sk_vendor_id AS vendor_id,
        fss.vendor_name,
        fss.total_pos,
        COALESCE(ps.purchase_value, 0) AS purchase_value,
        COALESCE(ps.purchase_qty, 0) AS purchase_qty,
        fss.delivery_pct,
        fss.fulfillment_pct,
        fss.avg_lead_time_days,
        fss.price_consistency_pct,
        fss.lead_time_stability_score,
        fss.delay_frequency,
        fss.final_score,
        fss.category,
        CASE WHEN (SELECT global_purchase_value FROM total_purchase) = 0 THEN 0 ELSE (COALESCE(ps.purchase_value, 0) / (SELECT global_purchase_value FROM total_purchase)) * 100 END AS purchase_contribution_pct,
        fss.recommendation_status
    FROM mart.fact_supplier_score fss
    LEFT JOIN purchase_stats ps ON fss.sk_vendor_id = ps.vendor_id
    """
    try:
        df = pd.read_sql(query, engine)
        print(f"  [OK] supplier_summary: {len(df)} rows")
        return df
    except Exception as e:
        print(f"  [FAIL] supplier_summary: {e}")
        return pd.DataFrame()

def build_sales_summary(engine):
    query = """
    WITH total_sales AS (
        SELECT SUM(revenue) as global_revenue FROM mart.fact_sales
    )
    SELECT 
        fs.product_id,
        dp.product_name,
        SUM(fs.revenue) AS total_revenue,
        SUM(fs.quantity) AS total_qty,
        SUM(fs.margin) AS total_margin,
        CASE WHEN SUM(fs.revenue) = 0 THEN 0 ELSE (SUM(fs.margin)/SUM(fs.revenue))*100 END AS margin_pct,
        COUNT(fs.sk_sales_id) AS trx_count,
        RANK() OVER(ORDER BY SUM(fs.revenue) DESC) AS rank_by_revenue,
        RANK() OVER(ORDER BY SUM(fs.margin) DESC) AS rank_by_margin,
        CASE WHEN (SELECT global_revenue FROM total_sales) = 0 THEN 0 ELSE (SUM(fs.revenue) / (SELECT global_revenue FROM total_sales)) * 100 END AS revenue_contribution_pct
    FROM mart.fact_sales fs
    JOIN mart.dim_product dp ON fs.product_id = dp.sk_product_id
    GROUP BY 1, 2
    """
    try:
        df = pd.read_sql(query, engine)
        print(f"  [OK] sales_summary: {len(df)} rows")
        return df
    except Exception as e:
        print(f"  [FAIL] sales_summary: {e}")
        return pd.DataFrame()

def build_inventory_summary(engine):
    query = """
    SELECT 
        dp.sk_product_id AS product_id,
        dp.product_name,
        dss.current_stock,
        dss.annual_demand,
        dss.current_stock * dp.list_price AS inventory_value,
        dss.inventory_turnover,
        dss.stock_coverage_days,
        dss.inventory_status,
        dss.inventory_age_days,
        dss.eoq,
        dss.safety_stock,
        dss.rop,
        dss.recommendation_status AS recommendation
    FROM mart.fact_decision_support dss
    JOIN mart.dim_product dp ON dss.product_id = dp.sk_product_id
    """
    try:
        df = pd.read_sql(query, engine)
        print(f"  [OK] inventory_summary: {len(df)} rows")
        return df
    except Exception as e:
        print(f"  [FAIL] inventory_summary: {e}")
        return pd.DataFrame()

def build_executive_summary(monthly_summary_df, engine):
    if monthly_summary_df.empty:
        return pd.DataFrame()
    
    # Calculate purchase_growth_pct
    df = monthly_summary_df.copy()
    df['prev_purchase'] = df['purchase_total'].shift(1)
    df['purchase_growth_pct'] = ((df['purchase_total'] - df['prev_purchase']) / df['prev_purchase'] * 100).fillna(0)
    df.drop(columns=['prev_purchase'], inplace=True)
    
    executive_df = df[[
        'month_id', 'month_name', 'revenue', 'revenue_growth_pct',
        'purchase_total', 'purchase_growth_pct', 'margin', 
        'margin_pct', 'inventory_value', 'avg_lead_time',
        'supplier_avg_score', 'forecast_accuracy', 'on_time_rate', 
        'total_sales_trx'
    ]].copy()
    
    print(f"  [OK] executive_summary: {len(executive_df)} rows")
    return executive_df

def load_aggregation(df, table_name):
    """Load a single aggregation table into mart schema (full refresh)."""
    if df.empty:
        print(f"  [SKIP] {table_name}: empty")
        return 0
    try:
        # Task 6: Add Metadata
        df['generated_at'] = datetime.datetime.now()
        df['data_period_start'] = '2024-01-01'
        df['data_period_end'] = '2026-12-31'

        df.to_sql(
            table_name,
            db.target_engine,
            schema=settings.TARGET_SCHEMA,
            if_exists="replace",
            index=False,
            method="multi",
        )
        print(f"  [LOADED] {table_name}: {len(df)} rows → mart.{table_name}")
        return len(df)
    except Exception as e:
        print(f"  [FAIL] Loading {table_name}: {e}")
        return 0

def build_all_aggregations():
    print("\n" + "=" * 60)
    print("PHASE 7 — Building Aggregation Tables (BI Presentation Layer)")
    print("=" * 60)
    
    target = db.target_engine
    results = {}
    
    ms_df = build_monthly_summary(target)
    
    agg = {
        "monthly_summary": ms_df,
        "inventory_monthly_summary": build_inventory_monthly_summary(target),
        "supplier_summary": build_supplier_summary(target),
        "sales_summary": build_sales_summary(target),
        "inventory_summary": build_inventory_summary(target),
        "executive_summary": build_executive_summary(ms_df, target)
    }
    
    for name, df in agg.items():
        results[name] = load_aggregation(df, name)
        
    print("\n── Aggregation Summary ──")
    total = 0
    for name, count in results.items():
        print(f"  {name}: {count} rows")
        total += count
    print(f"  TOTAL: {total} rows")
    
    return results

if __name__ == "__main__":
    build_all_aggregations()
