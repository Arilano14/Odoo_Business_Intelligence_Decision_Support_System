import sys
sys.path.append('backend')
import pandas as pd
import numpy as np
from config.database import db
from config.settings import settings

SCHEMA = settings.TARGET_SCHEMA

query = f"SELECT * FROM {SCHEMA}.fact_forecast_monthly ORDER BY product_id, month_id"
df = pd.read_sql(query, db.target_engine)

print("=" * 70)
print("APPROVED FORECAST LOGIC REPAIR — AUDIT & VERIFICATION REPORT")
print("=" * 70)

total_rows = len(df)
prod_count = df['product_id'].nunique()
month_count = df['month_id'].nunique()
print(f"1. Grid Completeness: {total_rows} rows ({prod_count} products x {month_count} months)")
assert total_rows == 283 * 12 or total_rows == prod_count * 12, f"Unexpected row count: {total_rows}"

# Check duplicates
dups = df.duplicated(subset=['product_id', 'month_id']).sum()
print(f"2. Duplicate Check (product_id, month_id): {dups} duplicates found")
assert dups == 0, "Duplicates found!"

# Check unavailable periods (first 3 months per product)
unavail_df = df[~df['forecast_available']]
print(f"3. Unavailable Period Count: {len(unavail_df)} rows (Expected 283 x 3 = 849)")
assert len(unavail_df) == prod_count * 3, f"Expected {prod_count * 3} unavailable rows, got {len(unavail_df)}"

# Check nullability of unavailable periods
unavail_nulls = unavail_df['ma3_forecast'].isna().sum()
print(f"4. Unavailable Forecast Null Check: {unavail_nulls} / {len(unavail_df)} are NULL")

# Check zero-history rule (0,0,0 -> forecast 0)
correct_zeros = df[df['interpretation'] == 'Correct Zero Forecast']
print(f"5. Correct Zero Forecast Count (actual=0, forecast=0): {len(correct_zeros)} rows")

# Breakdown of 7-class interpretation system
print("\n6. Interpretation Distribution (7-Class System):")
print(df['interpretation'].value_counts().to_string())

# Calculate Python WAPE (Overall)
valid_df = df[df['forecast_available']].copy()
total_actual = valid_df['actual_qty'].sum()
total_abs_error = valid_df['absolute_error'].sum()
wape_overall_error = total_abs_error / total_actual if total_actual > 0 else 0
accuracy_overall = (1 - wape_overall_error) * 100

print("\n" + "=" * 70)
print("STATISTICAL ACCURACY METRICS (PYTHON ETL RECONCILIATION)")
print("=" * 70)
print(f"Total Actual Quantity (Valid Periods):   {total_actual:,.2f}")
print(f"Total Absolute Error (Valid Periods):  {total_abs_error:,.2f}")
print(f"WAPE Overall Error Rate:                 {wape_overall_error * 100:.2f}%")
print(f"Forecast Accuracy Overall (WAPE):        {accuracy_overall:.2f}%")

# Calculate Positive Demand Accuracy (actual > 0)
pos_df = valid_df[valid_df['actual_qty'] > 0].copy()
pos_actual = pos_df['actual_qty'].sum()
pos_abs_error = pos_df['absolute_error'].sum()
pos_wape_error = pos_abs_error / pos_actual if pos_actual > 0 else 0
accuracy_positive_demand = (1 - pos_wape_error) * 100

print(f"\nPositive Demand Total Actual:            {pos_actual:,.2f}")
print(f"Positive Demand Absolute Error:          {pos_abs_error:,.2f}")
print(f"Positive Demand WAPE Error Rate:         {pos_wape_error * 100:.2f}%")
print(f"Accuracy on Positive Demand:             {accuracy_positive_demand:.2f}%")

print("\n" + "=" * 70)
print("FINAL EVALUATION STATUS:")
if accuracy_overall >= 80:
    print("STATUS: PASS (Accuracy >= 80%)")
else:
    print(f"STATUS: MA3 MODEL LIMITATION — REQUIRE MODEL COMPARISON (Accuracy = {accuracy_overall:.2f}%)")
print("=" * 70)
