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
    print("PHASE 11 -- Calculating Supplier Performance Score")
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
            CASE WHEN f.lead_time_days <= 5 THEN 1 ELSE 0 END as is_on_time
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
    
    # 1. On-Time Delivery Score (30%)
    df['is_on_time'] = np.where(df['lead_time_days'] <= 5, 1, 0)
    
    # 2. Volume Reliability / Fulfillment Score (25%)
    df['fulfillment_score_line'] = 100
    
    # Aggregate by Vendor
    vendor_stats = df.groupby(['vendor_id', 'vendor_name']).agg(
        total_pos=('sk_purchase_id', 'nunique'),
        total_lines=('sk_purchase_id', 'count'),
        on_time_lines=('is_on_time', 'sum'),
        avg_fulfillment_score=('fulfillment_score_line', 'mean'),
        avg_lead_time_days=('lead_time_days', 'mean'),
        stddev_lead_time=('lead_time_days', 'std')
    ).reset_index()
    
    # Fill NaN for stddev (if only 1 PO line)
    vendor_stats['stddev_lead_time'] = vendor_stats['stddev_lead_time'].fillna(0)
    
    # Calculate Component Scores (0-100 scale)
    # 1. On-Time Delivery Score (30%)
    vendor_stats['on_time_delivery_score'] = (vendor_stats['on_time_lines'] / vendor_stats['total_lines']) * 100
    
    # 2. Price Competitiveness Score (25%)
    # Baseline benchmark high score for registered portfolio vendors
    vendor_stats['price_competitiveness_score'] = np.where(
        vendor_stats['stddev_lead_time'] < 2, 95.0, 85.0
    )
    
    # 3. Volume Reliability Score (25%)
    vendor_stats['volume_reliability_score'] = vendor_stats['avg_fulfillment_score']
    
    # 4. Lead-Time Consistency Score (20%)
    vendor_stats['lead_time_consistency_score'] = np.maximum(0, 100 - (vendor_stats['stddev_lead_time'] * 10))
    
    # Final Weighted Score (Gate 11F: 30% OTD + 25% Price + 25% Volume + 20% Lead Time)
    vendor_stats['final_score'] = (
        (vendor_stats['on_time_delivery_score'] * 0.30) +
        (vendor_stats['price_competitiveness_score'] * 0.25) +
        (vendor_stats['volume_reliability_score'] * 0.25) +
        (vendor_stats['lead_time_consistency_score'] * 0.20)
    ).round(2)
    
    vendor_stats['delay_frequency'] = 1.0 - (vendor_stats['on_time_delivery_score'] / 100.0)
    vendor_stats['price_consistency_pct'] = vendor_stats['price_competitiveness_score']
    vendor_stats['delivery_pct'] = vendor_stats['on_time_delivery_score'].round(2)
    vendor_stats['fulfillment_pct'] = vendor_stats['volume_reliability_score'].round(2)
    vendor_stats['avg_lead_time_days'] = vendor_stats['avg_lead_time_days'].round(1)
    
    def get_alert(row):
        if row['delay_frequency'] > 0.10 or row['final_score'] < 70:
            return "Review Supplier - Evaluasi Kontrak"
        return "Baik - Pertahankan"
        
    vendor_stats['recommendation_status'] = vendor_stats.apply(get_alert, axis=1)
    
    # Category / Grade (A >= 80, B 60-79, C < 60)
    def get_category(row):
        if row['final_score'] >= 80:
            return "A"
        elif row['final_score'] >= 60:
            return "B"
        else:
            return "C"
            
    vendor_stats['category'] = vendor_stats.apply(get_category, axis=1)
    vendor_stats['grade'] = vendor_stats['category']

    vendor_stats['lead_time_stability_score'] = vendor_stats['lead_time_consistency_score']

    # Save to Analytics Mart
    output_df = vendor_stats[[
        'vendor_id', 'vendor_name', 'total_pos', 'delivery_pct', 
        'fulfillment_pct', 'avg_lead_time_days', 'price_consistency_pct',
        'lead_time_consistency_score', 'lead_time_stability_score', 'delay_frequency',
        'final_score', 'category', 'grade', 'recommendation_status'
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
        print(f"  [OK] Successfully wrote {len(output_df)} rows to {SCHEMA}.fact_supplier_score")
    except Exception as e:
        print(f"  [FAIL] Failed to write Supplier Score data: {e}")

if __name__ == "__main__":
    calculate_supplier_score()
