"""
Supplier Score Calculator

Evaluates suppliers based on 4 criteria:
- Delivery Speed (40%): Comparing actual receipt date vs order date vs standard lead time (5 days).
- Order Fulfillment (30%): Quantity Received / Quantity Ordered
- Price Consistency (20%): Standard Price / PO Price
- Delay Frequency (10%): Percentage of POs where receipt date > planned date
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
    
    # Calculate dimensions per line
    # 1. Delivery Score (Target 5 days, if 5 days = 100%, each day late -10%)
    df['delivery_score_line'] = np.where(
        df['lead_time_days'] <= 5, 
        100, 
        np.maximum(0, 100 - ((df['lead_time_days'] - 5) * 10))
    )
    
    # 2. Fulfillment (For simulation simplicity, assume 100% since ORM does full receipt)
    # If partial receipt was simulated, it would be qty_received / qty_ordered
    df['fulfillment_score_line'] = 100
    
    # 3. Price Consistency (Standard Price / PO Price)
    # Cap at 100%
    df['price_consistency_line'] = np.where(
        df['price_unit'] > 0,
        np.minimum(100, (df['standard_price'] / df['price_unit']) * 100),
        100
    )
    
    # Aggregate by Vendor
    vendor_stats = df.groupby(['vendor_id', 'vendor_name']).agg(
        total_pos=('sk_purchase_id', 'nunique'),
        total_delayed_lines=('is_delayed', 'sum'),
        total_lines=('is_delayed', 'count'),
        avg_delivery_score=('delivery_score_line', 'mean'),
        avg_fulfillment_score=('fulfillment_score_line', 'mean'),
        avg_price_consistency=('price_consistency_line', 'mean')
    ).reset_index()
    
    # 4. Delay Frequency Score
    # 0 delays = 100%. 100% delay = 0%.
    vendor_stats['delay_frequency'] = vendor_stats['total_delayed_lines'] / vendor_stats['total_lines']
    vendor_stats['delay_frequency_score'] = (1 - vendor_stats['delay_frequency']) * 100
    
    # Calculate Final Weighted Score
    # 40% Delivery, 30% Fulfillment, 20% Price, 10% Delay Freq
    vendor_stats['final_score'] = (
        (vendor_stats['avg_delivery_score'] * 0.40) +
        (vendor_stats['avg_fulfillment_score'] * 0.30) +
        (vendor_stats['avg_price_consistency'] * 0.20) +
        (vendor_stats['delay_frequency_score'] * 0.10)
    ).round(2)
    
    def get_alert(row):
        if row['delay_frequency'] > 0.10 or row['final_score'] < 70:
            return "Review Supplier - Evaluasi Kontrak"
        return "Baik - Pertahankan"
        
    vendor_stats['recommendation_status'] = vendor_stats.apply(get_alert, axis=1)

    # Save to Analytics Mart
    output_df = vendor_stats[[
        'vendor_id', 'vendor_name', 'total_pos', 'avg_delivery_score', 
        'avg_fulfillment_score', 'avg_price_consistency', 'delay_frequency_score',
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
