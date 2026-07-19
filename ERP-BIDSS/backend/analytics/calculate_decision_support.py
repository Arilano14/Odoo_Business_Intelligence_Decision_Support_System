"""
Decision Support System (DSS) Layer.

Calculates prescriptive and predictive metrics based on Business Assumptions.
Saves the results into Analytics Mart schema (e.g. mart.fact_decision_support).
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np
from config.database import db
from config.settings import settings

# ── Business Assumptions ─────────────────────────────────────
ORDERING_COST = 500000  # S = Rp 500.000 per PO
HOLDING_COST_RATE = 0.20  # H = 20% of standard_price per year
WORKING_DAYS = 300
SAFETY_FACTOR = 1.65  # 95% service level


def calculate_decision_support():
    print("=" * 60)
    print("PHASE 6 — Calculating Decision Support System (DSS)")
    print("=" * 60)

    SCHEMA = settings.TARGET_SCHEMA
    
    # Extract data from Analytics Mart
    # We need product, daily demand stats, and lead time stats
    
    query = f"""
        WITH daily_sales AS (
            SELECT 
                product_id,
                date_id,
                SUM(quantity) AS daily_qty
            FROM {SCHEMA}.fact_sales
            GROUP BY product_id, date_id
        ),
        product_stats AS (
            SELECT 
                product_id,
                SUM(daily_qty) AS annual_demand,
                AVG(daily_qty) AS avg_daily_demand,
                MAX(daily_qty) AS max_daily_demand,
                STDDEV(daily_qty) AS stddev_demand
            FROM daily_sales
            GROUP BY product_id
        ),
        lead_time_stats AS (
            SELECT 
                product_id,
                AVG(lead_time_days) AS avg_lead_time,
                MAX(lead_time_days) AS max_lead_time,
                STDDEV(lead_time_days) AS stddev_lead_time
            FROM {SCHEMA}.fact_purchase
            GROUP BY product_id
        )
        SELECT 
            p.sk_product_id AS product_id,
            p.product_name,
            p.list_price AS standard_price,
            COALESCE(s.annual_demand, 0) AS annual_demand,
            COALESCE(s.avg_daily_demand, 0) AS avg_daily_demand,
            COALESCE(s.max_daily_demand, 0) AS max_daily_demand,
            COALESCE(s.stddev_demand, 0) AS stddev_demand,
            COALESCE(l.avg_lead_time, 5) AS avg_lead_time,
            COALESCE(l.max_lead_time, 5) AS max_lead_time,
            COALESCE(l.stddev_lead_time, 0) AS stddev_lead_time
        FROM {SCHEMA}.dim_product p
        LEFT JOIN product_stats s ON p.sk_product_id = s.product_id
        LEFT JOIN lead_time_stats l ON p.sk_product_id = l.product_id
        WHERE p.list_price > 0
    """
    
    try:
        df = pd.read_sql(query, db.target_engine)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    if df.empty:
        print("No product data to calculate DSS.")
        return
        
    print(f"Processing DSS for {len(df)} products...")
    
    # 1. Calculate Holding Cost (H)
    df['holding_cost'] = df['standard_price'] * HOLDING_COST_RATE
    
    # 2. Calculate EOQ: sqrt((2 * D * S) / H)
    # Prevent division by zero
    df['eoq'] = np.where(
        df['holding_cost'] > 0,
        np.sqrt((2 * df['annual_demand'] * ORDERING_COST) / df['holding_cost']),
        0
    ).round(0).astype(int)
    
    # 3. Calculate Safety Stock
    # Formula: (Max Demand x Max Lead Time) - (Avg Demand x Avg Lead Time)
    # Or Statistical: Z * sqrt( (Avg LT * StdDev Dem^2) + (Avg Dem^2 * StdDev LT^2) )
    # We use the standard logical one as requested in prompt.
    df['safety_stock'] = (
        (df['max_daily_demand'] * df['max_lead_time']) - 
        (df['avg_daily_demand'] * df['avg_lead_time'])
    ).round(0).astype(int)
    
    # Prevent negative safety stock
    df['safety_stock'] = np.where(df['safety_stock'] < 0, 0, df['safety_stock'])
    
    # 4. Calculate ROP: (Avg Daily Demand * Avg Lead Time) + Safety Stock
    df['rop'] = (
        (df['avg_daily_demand'] * df['avg_lead_time']) + df['safety_stock']
    ).round(0).astype(int)
    
    # 5. Recommendation Status
    # In a real pipeline, we'd compare ROP to Current Stock On Hand.
    # We will fetch current stock from fact_inventory.
    stock_query = f"""
        SELECT 
            product_id,
            SUM(CASE WHEN movement_type = 'incoming' THEN quantity ELSE -quantity END) as current_stock,
            MAX(date_id) as last_movement_date
        FROM {SCHEMA}.fact_inventory
        GROUP BY product_id
    """
    try:
        stock_df = pd.read_sql(stock_query, db.target_engine)
        df = df.merge(stock_df, on='product_id', how='left')
        df['current_stock'] = df['current_stock'].fillna(0)
        
        # Calculate Inventory Age Days based on last_movement_date
        # Convert integer YYYYMMDD to datetime
        # Use 2026-12-31 as current date for age calculation since dataset goes up to end of 2026
        df['last_movement_date'] = pd.to_datetime(df['last_movement_date'], format='%Y%m%d', errors='coerce')
        current_date_for_aging = pd.to_datetime('2026-12-31')
        df['inventory_age_days'] = (current_date_for_aging - df['last_movement_date']).dt.days.fillna(999).astype(int)
    except Exception:
        df['current_stock'] = 0
        df['inventory_age_days'] = 999
        
    df['inventory_turnover'] = np.where(
        df['current_stock'] > 0, 
        df['annual_demand'] / df['current_stock'], 
        0
    )
    
    # Calculate Stock Coverage Days
    df['stock_coverage_days'] = np.where(
        df['avg_daily_demand'] > 0,
        df['current_stock'] / df['avg_daily_demand'],
        999
    ).round(0).astype(int)
        
    def get_status(row):
        if row['inventory_turnover'] < 2 and row['annual_demand'] > 0:
            return "Slow Moving - Tunda Pembelian"
        elif row['current_stock'] <= row['rop']:
            return "Reorder - Buat Draft PO"
        else:
            return "Normal - Pantau Penjualan"
            
    df['recommendation_status'] = df.apply(get_status, axis=1)

    # 6. Inventory Status (Fast / Slow / Dead)
    # Threshold dihitung berdasarkan distribusi aktual data (data-driven):
    # Median turnover = 0.07, P75 = 0.12, P90 = 0.21
    # Disesuaikan untuk konteks distributor alat berat (volume rendah, harga tinggi)
    products_with_demand = df[df['annual_demand'] > 0]['inventory_turnover']
    if len(products_with_demand) > 0:
        p25 = products_with_demand.quantile(0.25)
        p75 = products_with_demand.quantile(0.75)
    else:
        p25, p75 = 0.03, 0.12
    
    def get_inventory_status(row):
        if row['annual_demand'] == 0:
            return "Dead Stock"
        elif row['inventory_turnover'] >= p75:
            return "Fast Moving"
        elif row['inventory_turnover'] >= p25:
            return "Normal"
        else:
            return "Slow Moving"
            
    df['inventory_status'] = df.apply(get_inventory_status, axis=1)

    # 7. Risk Level & Priority
    # Urutan evaluasi: Stock Out → Near Reorder → Dead Stock → Slow Moving Overstock → Normal
    # Menggunakan stock_coverage_days sebagai secondary trigger karena
    # gap SS-ROP sangat sempit pada data distributor alat berat
    def get_risk_and_priority(row):
        risk = "Low"
        priority = 5
        impact = 0
        action = "Pantau pergerakan rutin"
        
        # Priority 1: Stock Out — stok di bawah safety stock, ada demand aktif
        if row['current_stock'] <= row['safety_stock'] and row['annual_demand'] > 0:
            risk = "High"
            priority = 1
            impact = (row['avg_daily_demand'] * row['avg_lead_time'] * row['standard_price'])
            action = "Segera buat PO Express"
            
        # Priority 2: Near Reorder — stok mendekati habis (coverage < 30 hari), ada demand
        elif row['stock_coverage_days'] < 30 and row['annual_demand'] > 0 and row['current_stock'] > 0:
            risk = "Medium"
            priority = 2
            impact = (row['eoq'] * row['standard_price']) * 0.1
            action = "Buat Draft PO sejumlah EOQ"
            
        # Priority 3: Dead Stock — tidak ada demand, stok menumpuk
        elif row['inventory_status'] == 'Dead Stock' and row['current_stock'] > 0:
            risk = "High"
            priority = 3
            impact = row['current_stock'] * row['standard_price']
            action = "Beri diskon cuci gudang / Retur supplier"
            
        # Priority 4: Slow Moving Overstock — demand rendah, stok berlebih
        elif row['inventory_status'] == 'Slow Moving' and row['stock_coverage_days'] > 180:
            risk = "Medium"
            priority = 4
            impact = (row['current_stock'] * row['standard_price']) * HOLDING_COST_RATE
            action = "Hentikan pembelian, buat promo bundling"
            
        return pd.Series([risk, priority, impact, action])

    df[['risk_level', 'priority', 'business_impact', 'suggested_action']] = df.apply(get_risk_and_priority, axis=1)

    # Fetch latest forecast from fact_forecast_monthly
    try:
        latest_forecast_query = f"""
            SELECT product_id, ma3_forecast AS forecast_qty
            FROM {SCHEMA}.fact_forecast_monthly
            WHERE month_id = (SELECT MAX(month_id) FROM {SCHEMA}.fact_forecast_monthly)
        """
        forecast_df = pd.read_sql(latest_forecast_query, db.target_engine)
        df = df.merge(forecast_df, on='product_id', how='left')
        df['forecast_qty'] = df['forecast_qty'].fillna(0).astype(int)
    except Exception:
        df['forecast_qty'] = 0

    # Save to Analytics Mart
    output_df = df[[
        'product_id', 'product_name', 'annual_demand', 'avg_daily_demand', 'avg_lead_time',
        'forecast_qty', 'eoq', 'safety_stock', 'rop', 'current_stock', 'recommendation_status',
        'inventory_status', 'inventory_age_days', 'stock_coverage_days',
        'inventory_turnover', 'priority', 'risk_level', 'business_impact', 'suggested_action'
    ]]
    
    try:
        output_df.to_sql(
            'fact_decision_support',
            db.target_engine,
            schema=SCHEMA,
            if_exists='replace',
            index=False
        )
        print(f"✅ Successfully wrote {len(output_df)} rows to {SCHEMA}.fact_decision_support")
    except Exception as e:
        print(f"❌ Failed to write DSS data: {e}")

def calculate_forecast():
    print("\n" + "=" * 60)
    print("PHASE 6 — Calculating 3-Month Moving Average Forecast")
    print("=" * 60)
    
    SCHEMA = settings.TARGET_SCHEMA
    
    # 1. Get Monthly Demand per Product
    query = f"""
        SELECT 
            product_id,
            SUBSTRING(date_id::TEXT, 1, 6) AS month_id,
            SUM(quantity) AS actual_qty
        FROM {SCHEMA}.fact_sales
        GROUP BY product_id, month_id
        ORDER BY product_id, month_id
    """
    
    try:
        df = pd.read_sql(query, db.target_engine)
    except Exception as e:
        print(f"Error fetching data for forecast: {e}")
        return

    if df.empty:
        print("No sales data available for forecasting.")
        return

    # Pivot to ensure missing months are 0
    df['month_id'] = pd.to_datetime(df['month_id'], format='%Y%m')
    
    # Generate full combinations of product & month
    all_products = df['product_id'].unique()
    all_months = pd.date_range(start=df['month_id'].min(), end=df['month_id'].max(), freq='MS')
    full_idx = pd.MultiIndex.from_product([all_products, all_months], names=['product_id', 'month_id'])
    
    df = df.set_index(['product_id', 'month_id']).reindex(full_idx, fill_value=0).reset_index()
    
    # Calculate 3-Month Moving Average (shift by 1 so we predict based on past 3 months)
    df['ma3_forecast'] = df.groupby('product_id')['actual_qty'].transform(
        lambda x: x.rolling(window=3, min_periods=1).mean().shift(1)
    ).fillna(0).round(0).astype(int)
    
    # Calculate Forecast Error (%)
    df['forecast_error_pct'] = np.where(
        df['actual_qty'] > 0,
        abs(df['actual_qty'] - df['ma3_forecast']) / df['actual_qty'] * 100,
        np.where(df['ma3_forecast'] > 0, 100, 0)
    ).round(2)
    
    # Generate Interpretation
    def get_interpretation(row):
        if row['ma3_forecast'] == 0:
            return "Baseline (Tidak cukup data historis)"
            
        error = row['forecast_error_pct']
        if error <= 10:
            return "Akurat. Prediksi sesuai dengan permintaan aktual."
        elif row['actual_qty'] > row['ma3_forecast']:
            return f"Under-forecast (Error {error}%). Permintaan aktual lebih tinggi dari prediksi. Kemungkinan imbas Panic Buying atau lonjakan proyek."
        else:
            return f"Over-forecast (Error {error}%). Permintaan aktual lebih rendah dari prediksi. Waspada risiko overstock jika PO tidak ditahan."

    df['interpretation'] = df.apply(get_interpretation, axis=1)
    
    # Convert month_id back to integer format YYYYMM
    df['month_id'] = df['month_id'].dt.strftime('%Y%m').astype(int)
    
    # Save to Analytics Mart
    try:
        df.to_sql(
            'fact_forecast_monthly',
            db.target_engine,
            schema=SCHEMA,
            if_exists='replace',
            index=False
        )
        print(f"✅ Successfully wrote {len(df)} rows to {SCHEMA}.fact_forecast_monthly")
    except Exception as e:
        print(f"❌ Failed to write Forecast data: {e}")

if __name__ == "__main__":
    calculate_forecast()
    calculate_decision_support()

