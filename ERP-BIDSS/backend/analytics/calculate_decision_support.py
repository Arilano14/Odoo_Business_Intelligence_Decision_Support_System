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
            SUM(CASE WHEN movement_type = 'incoming' THEN quantity ELSE -quantity END) as current_stock
        FROM {SCHEMA}.fact_inventory
        GROUP BY product_id
    """
    try:
        stock_df = pd.read_sql(stock_query, db.target_engine)
        df = df.merge(stock_df, on='product_id', how='left')
        df['current_stock'] = df['current_stock'].fillna(0)
    except Exception:
        df['current_stock'] = 0
        
    df['inventory_turnover'] = np.where(
        df['current_stock'] > 0, 
        df['annual_demand'] / df['current_stock'], 
        0
    )
        
    def get_status(row):
        if row['inventory_turnover'] < 2 and row['annual_demand'] > 0:
            return "Slow Moving - Tunda Pembelian"
        elif row['current_stock'] <= row['rop']:
            return "Reorder - Buat Draft PO"
        else:
            return "Normal - Pantau Penjualan"
            
    df['recommendation_status'] = df.apply(get_status, axis=1)

    # Save to Analytics Mart
    output_df = df[[
        'product_id', 'annual_demand', 'avg_daily_demand', 'avg_lead_time',
        'eoq', 'safety_stock', 'rop', 'current_stock', 'recommendation_status'
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

if __name__ == "__main__":
    calculate_decision_support()
