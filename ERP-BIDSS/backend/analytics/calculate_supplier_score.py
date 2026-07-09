"""
Supplier Score Calculator

Evaluates suppliers based on 3 criteria:
- On Time Delivery (40%): Percentage of lines delivered on or before standard lead time (5 days).
- Order Fulfillment (35%): Quantity Received / Quantity Ordered (Simulated as 100%).
- Lead Time Stability (25%): Based on Standard Deviation of Lead Time (Consistent = 100%).
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np
from config.database import db
from config.settings import settings

def calculate_supplier_score():
    print("=" * 60)
    print("PHASE 6 — Calculating Supplier Performance Score")
    print("=" * 60)

    SCHEMA = settings.TARGET_SCHEMA
    
    # Extract data from Analytics Mart (Purchase Fact and Dimension Vendor)
    query = f"""
        SELECT 
            f.vendor_id,
            v.vendor_name,
            f.sk_purchase_id,
            f.lead_time_days,
            f.quantity,
            f.price_unit,
            f.subtotal,
            p.list_price AS standard_price,
            f.date_id,
            -- For simulation, we assume delay if lead_time_days > 5
            CASE WHEN f.lead_time_days > 5 THEN 1 ELSE 0 END as is_delayed
        FROM {SCHEMA}.fact_purchase f
        JOIN {SCHEMA}.dim_vendor v ON f.vendor_id = v.sk_vendor_id
        JOIN {SCHEMA}.dim_product p ON f.product_id = p.sk_product_id
    """
    
    try:
        df = pd.read_sql(query, db.target_engine)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    if df.empty:
        print("No purchase data to calculate Supplier Score.")
        return
        
    print(f"Evaluating {df['vendor_id'].nunique()} Suppliers across {len(df)} lines...")
    
    # 1. Delivery Score (On Time Delivery % per line)
    df['is_on_time'] = np.where(df['lead_time_days'] <= 5, 1, 0)
    
    # 2. Fulfillment (For simulation simplicity, assume 100%)
    df['fulfillment_score_line'] = 100
    
    # Aggregate by Vendor
    vendor_stats = df.groupby(['vendor_id', 'vendor_name']).agg(
        total_pos=('sk_purchase_id', 'nunique'),
        total_lines=('sk_purchase_id', 'count'),
        on_time_lines=('is_on_time', 'sum'),
        avg_fulfillment_score=('fulfillment_score_line', 'mean'),
        stddev_lead_time=('lead_time_days', 'std')
    ).reset_index()
    
    # Fill NaN for stddev (if only 1 PO line)
    vendor_stats['stddev_lead_time'] = vendor_stats['stddev_lead_time'].fillna(0)
    
    # Calculate Component Scores
    # 1. On Time Delivery Score (40%)
    vendor_stats['on_time_delivery_score'] = (vendor_stats['on_time_lines'] / vendor_stats['total_lines']) * 100
    
    # 2. Fulfillment Score (35%)
    vendor_stats['fulfillment_score'] = vendor_stats['avg_fulfillment_score']
    
    # 3. Lead Time Stability Score (25%)
    # If stddev is 0, score is 100. Every 1 day of stddev reduces score by 10.
    vendor_stats['lead_time_stability_score'] = np.maximum(0, 100 - (vendor_stats['stddev_lead_time'] * 10))
    
    # Final Weighted Score
    vendor_stats['final_score'] = (
        (vendor_stats['on_time_delivery_score'] * 0.40) +
        (vendor_stats['fulfillment_score'] * 0.35) +
        (vendor_stats['lead_time_stability_score'] * 0.25)
    ).round(2)
    
    vendor_stats['delay_frequency'] = 1.0 - (vendor_stats['on_time_delivery_score'] / 100.0)
    
    def get_alert(row):
        if row['delay_frequency'] > 0.10 or row['final_score'] < 70:
            return "Review Supplier - Evaluasi Kontrak"
        return "Baik - Pertahankan"
        
    vendor_stats['recommendation_status'] = vendor_stats.apply(get_alert, axis=1)

    # Save to Analytics Mart
    output_df = vendor_stats[[
        'vendor_id', 'vendor_name', 'total_pos', 'on_time_delivery_score', 
        'fulfillment_score', 'lead_time_stability_score', 'delay_frequency',
        'final_score', 'recommendation_status'
    ]]
    
    try:
        output_df = output_df.rename(columns={'vendor_id': 'sk_vendor_id'})
        output_df.to_sql(
            'fact_supplier_score',
            db.target_engine,
            schema=SCHEMA,
            if_exists='replace',
            index=False
        )
        print(f"✅ Successfully wrote {len(output_df)} rows to {SCHEMA}.fact_supplier_score")
    except Exception as e:
        print(f"❌ Failed to write Supplier Score data: {e}")

if __name__ == "__main__":
    calculate_supplier_score()
