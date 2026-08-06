"""
Phase 11.4 — Gate 0 Dry-Run Scenario V2 Generator & Forecast Validator
========================================================================
Generates 36-month synthetic demand scenario (2024-2026) for 240 Verified Portfolio SKUs.
Runs 6 candidate models, selects Champion per product on 2025 data, and evaluates 2026 holdout.
"""

import sys
import os
import math
import hashlib
import json
import numpy as np
import pandas as pd
from sqlalchemy import text

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.database import db
from config.settings import settings

SCHEMA = settings.TARGET_SCHEMA
SEED = 20260806
SCENARIO_VERSION = "SYNTHETIC_FORECAST_V2"
BATCH_ID = "SYNTH_V2_SEED_20260806"

# Candidate forecasting models
def forecast_naive(history: np.ndarray) -> float:
    return float(history[-1]) if len(history) > 0 else 0.0

def forecast_ma3(history: np.ndarray) -> float:
    if len(history) < 3:
        return 0.0
    recent = history[-3:]
    return 0.0 if np.sum(recent) == 0 else float(np.mean(recent))

def forecast_ses(history: np.ndarray, alpha: float = 0.2) -> float:
    if len(history) == 0:
        return 0.0
    s = float(history[0])
    for y in history[1:]:
        s = alpha * float(y) + (1.0 - alpha) * s
    return float(s)

def forecast_croston(history: np.ndarray, alpha: float = 0.2) -> float:
    if len(history) == 0:
        return 0.0
    nonzero = history[history > 0]
    if len(nonzero) == 0:
        return 0.0
    z = float(nonzero[0])
    p = float(len(history) / len(nonzero))
    q = 1.0
    for y in history:
        if y > 0:
            z = alpha * float(y) + (1.0 - alpha) * z
            p = alpha * q + (1.0 - alpha) * p
            q = 1.0
        else:
            q += 1.0
    return float(z / p) if p > 0 else 0.0

def forecast_sba(history: np.ndarray, alpha: float = 0.2) -> float:
    return float((1.0 - (alpha / 2.0)) * forecast_croston(history, alpha=alpha))

def forecast_tsb(history: np.ndarray, alpha: float = 0.2, beta: float = 0.2) -> float:
    if len(history) == 0:
        return 0.0
    nonzero = history[history > 0]
    if len(nonzero) == 0:
        return 0.0
    z = float(nonzero[0])
    p = float(len(nonzero) / len(history))
    for y in history:
        if y > 0:
            z = alpha * float(y) + (1.0 - alpha) * z
            p = beta * 1.0 + (1.0 - beta) * p
        else:
            p = beta * 0.0 + (1.0 - beta) * p
    return float(p * z)

MODEL_FUNCS = {
    'Naive': forecast_naive,
    'MA3': forecast_ma3,
    'SES': forecast_ses,
    'Croston': forecast_croston,
    'SBA': forecast_sba,
    'TSB': forecast_tsb,
}


def run_dryrun():
    print("=" * 75)
    print("GATE 0 DRY-RUN — SYNTHETIC DEMAND SCENARIO V2 BENCHMARK")
    print("=" * 75)
    
    # 1. Fetch exactly 240 Verified Portfolio Products
    query = f"""
        SELECT sk_product_id AS product_id, product_name, category, default_code, standard_price, list_price
        FROM {SCHEMA}.dim_product
        WHERE default_code LIKE 'PORTFOLIO_2026_%'
        ORDER BY product_id
    """
    with db.target_engine.connect() as conn:
        prod_df = pd.read_sql(text(query), conn)
    
    print(f"Verified Portfolio Scope: {len(prod_df)} SKUs")
    if len(prod_df) != 240:
        print(f"SCOPE FAILURE: Expected exactly 240 portfolio SKUs, got {len(prod_df)}")
        sys.exit(1)

    # 2. Generator Config & Hash Computation
    rng = np.random.default_rng(SEED)
    config_dict = {
        "seed": SEED,
        "scenario_version": SCENARIO_VERSION,
        "batch_id": BATCH_ID,
        "portfolio_skus": 240,
        "patterns": {"Smooth": 84, "Erratic": 48, "Intermittent": 84, "Lumpy": 24}
    }
    config_str = json.dumps(config_dict, sort_keys=True)
    config_hash = hashlib.sha256(config_str.encode('utf-8')).hexdigest()
    print(f"Generator Config Hash: {config_hash}")

    # 3. Assign Stable Pattern Profiles to 240 SKUs
    # Sort products and assign: 84 Smooth, 48 Erratic, 84 Intermittent, 24 Lumpy
    pattern_assignments = (
        ['Smooth'] * 84 +
        ['Erratic'] * 48 +
        ['Intermittent'] * 84 +
        ['Lumpy'] * 24
    )
    prod_df['demand_pattern'] = pattern_assignments

    print("\nDemand Pattern Allocation (240 Portfolio SKUs):")
    print(prod_df['demand_pattern'].value_counts().to_string())

    # 4. Generate 36-Month Demand Matrix (2024-01 to 2026-12)
    # Months 1..12 (2024), 13..24 (2025), 25..36 (2026)
    demand_records = []
    
    for idx, row in prod_df.iterrows():
        p_id = int(row['product_id'])
        pattern = row['demand_pattern']
        p_seed = int(SEED + p_id)
        p_rng = np.random.default_rng(p_seed)
        
        # Base demand and parameters per pattern
        if pattern == 'Smooth':
            base_d = p_rng.uniform(18.0, 30.0)
            trend_r = 0.005
            season_s = 0.10
            noise_sd = 0.05
            zero_p = 0.00
        elif pattern == 'Erratic':
            base_d = p_rng.uniform(12.0, 22.0)
            trend_r = 0.003
            season_s = 0.08
            noise_sd = 0.10
            zero_p = 0.05
        elif pattern == 'Intermittent':
            base_d = p_rng.uniform(8.0, 16.0)
            trend_r = 0.002
            season_s = 0.05
            noise_sd = 0.08
            zero_p = 0.20
        else: # Lumpy
            base_d = p_rng.uniform(5.0, 12.0)
            trend_r = 0.001
            season_s = 0.00
            noise_sd = 0.12
            zero_p = 0.35

        for m_idx in range(1, 37): # Months 1..36
            # Compute signal
            trend_factor = 1.0 + (trend_r * m_idx)
            season_factor = 1.0 + (season_s * math.sin(2.0 * math.pi * m_idx / 12.0))
            noise_factor = max(0.70, p_rng.normal(1.0, noise_sd))
            
            expected_demand = base_d * trend_factor * season_factor * noise_factor
            
            if p_rng.random() < zero_p:
                actual_qty = 0
            else:
                actual_qty = max(0, int(round(expected_demand)))
                
            # Date construction (2024-01 to 2026-12)
            yr = 2024 + ((m_idx - 1) // 12)
            mo = ((m_idx - 1) % 12) + 1
            month_id = yr * 100 + mo
            
            demand_records.append({
                'product_id': p_id,
                'demand_pattern': pattern,
                'month_index': m_idx,
                'month_id': month_id,
                'year': yr,
                'actual_qty': actual_qty
            })

    demand_df = pd.DataFrame(demand_records)
    
    # Save Staging CSV
    staging_file = "staging_scenario_v2.csv"
    demand_df.to_csv(staging_file, index=False)
    print(f"\n[OK] Stored 36-month demand scenario in '{staging_file}' ({len(demand_df)} rows)")

    # 5. Run Rolling-Origin Benchmark & Champion Selection
    # Champion Selection Period: 2025 ONLY (Months 13..24)
    # Holdout Evaluation Period: 2026 ONLY (Months 25..36)
    
    model_evals_2025 = []
    model_evals_2026 = []
    
    products = prod_df['product_id'].values
    
    for p_id in products:
        p_demand = demand_df[demand_df['product_id'] == p_id].sort_values('month_index')['actual_qty'].values
        pattern = prod_df[prod_df['product_id'] == p_id]['demand_pattern'].values[0]
        
        for model_name, model_fn in MODEL_FUNCS.items():
            # 2025 Evaluation (Months 13..24, indices 12..23)
            for step_idx in range(12, 24):
                actual = p_demand[step_idx]
                history = p_demand[:step_idx]
                fct_raw = max(0.0, float(model_fn(history)))
                abs_err = abs(actual - fct_raw)
                bias = fct_raw - actual
                
                model_evals_2025.append({
                    'product_id': p_id, 'model_name': model_name,
                    'actual_qty': actual, 'forecast_raw': fct_raw,
                    'absolute_error': abs_err, 'bias': bias
                })
                
            # 2026 Holdout Evaluation (Months 25..36, indices 24..35)
            for step_idx in range(24, 36):
                m_id = 202601 + (step_idx - 24)
                actual = p_demand[step_idx]
                history = p_demand[:step_idx]
                fct_raw = max(0.0, float(model_fn(history)))
                fct_round = max(0.0, float(np.round(fct_raw)))
                abs_err = abs(actual - fct_raw)
                bias = fct_raw - actual
                
                model_evals_2026.append({
                    'product_id': p_id, 'model_name': model_name, 'demand_pattern': pattern,
                    'month_id': m_id, 'actual_qty': actual, 'forecast_raw': fct_raw,
                    'forecast_rounded': fct_round, 'absolute_error': abs_err, 'bias': bias
                })

    df_2025 = pd.DataFrame(model_evals_2025)
    df_2026 = pd.DataFrame(model_evals_2026)

    # 6. Select Champion per Product based ONLY on 2025 Data
    stats_2025 = df_2025.groupby(['product_id', 'model_name']).agg(
        tot_act=('actual_qty', 'sum'),
        tot_err=('absolute_error', 'sum'),
        mae=('absolute_error', 'mean'),
        mean_bias=('bias', 'mean')
    ).reset_index()
    
    stats_2025['wape'] = stats_2025['tot_err'] / stats_2025['tot_act']
    stats_2025['abs_bias'] = stats_2025['mean_bias'].abs()
    
    # Sort hierarchy: 1. Lowest WAPE, 2. Lowest MAE, 3. Lowest |Bias|
    stats_2025 = stats_2025.sort_values(['product_id', 'wape', 'mae', 'abs_bias']).reset_index(drop=True)
    champions_2025 = stats_2025.groupby('product_id').first().reset_index()
    champion_map = set(zip(champions_2025['product_id'], champions_2025['model_name']))

    print("\nChampion Model Distribution (Selected on 2025 Data):")
    print(champions_2025['model_name'].value_counts().to_string())

    # 7. Evaluate 2026 Holdout Performance for Champion Models
    df_2026['is_champion'] = df_2026.apply(
        lambda r: (r['product_id'], r['model_name']) in champion_map, axis=1
    )

    champ_2026 = df_2026[df_2026['is_champion']].copy()
    
    tot_act_2026 = champ_2026['actual_qty'].sum()
    tot_err_2026 = champ_2026['absolute_error'].sum()
    holdout_wape_2026 = tot_err_2026 / tot_act_2026
    holdout_acc_2026 = max(0.0, 1.0 - holdout_wape_2026) * 100

    # Positive Demand Metrics
    pos_2026 = champ_2026[champ_2026['actual_qty'] > 0]
    pos_act_2026 = pos_2026['actual_qty'].sum()
    pos_err_2026 = pos_2026['absolute_error'].sum()
    pos_wape_2026 = pos_err_2026 / pos_act_2026
    pos_acc_2026 = max(0.0, 1.0 - pos_wape_2026) * 100

    print("\n" + "=" * 75)
    print("GATE 0 DRY-RUN HOLDOUT ACCURACY RESULTS (FY 2026):")
    print("=" * 75)
    print(f"Total Holdout Actual Quantity:           {tot_act_2026:,.2f}")
    print(f"Total Holdout Absolute Error:          {tot_err_2026:,.2f}")
    print(f"Portfolio Champion Holdout WAPE:        {holdout_wape_2026 * 100:.2f}%")
    print(f"Portfolio Champion Holdout Accuracy:    {holdout_acc_2026:.2f}%")
    print(f"Positive-Demand Holdout WAPE:           {pos_wape_2026 * 100:.2f}%")
    print(f"Positive-Demand Holdout Accuracy:       {pos_acc_2026:.2f}%")

    print("\nExpected Row Counts Check:")
    print(f"  Model Comparison Rows (240 prods x 6 models x 12 mos): {len(df_2026)} / 17,280")
    print(f"  Champion Monthly Rows (240 prods x 12 mos):             {len(champ_2026)} / 2,880")

    assert len(df_2026) == 17280, f"Expected 17,280 comparison rows, got {len(df_2026)}"
    assert len(champ_2026) == 2880, f"Expected 2,880 champion rows, got {len(champ_2026)}"

    print("\n" + "=" * 75)
    print("GATE 0 ACCEPTANCE STATUS:")
    if holdout_wape_2026 <= 0.20 and holdout_acc_2026 >= 80.0:
        print("GATE 0 RESULT: PASS (Holdout WAPE <= 20% / Accuracy >= 80%)")
        print(f"CONFIG HASH FROZEN: {config_hash}")
        print("READY FOR ODOO ORM TRANSACTION CREATION!")
    else:
        print(f"GATE 0 RESULT: FAILED (Holdout WAPE = {holdout_wape_2026 * 100:.2f}%)")
        print("DO NOT CREATE ODOO RECORDS UNTIL DRY-RUN PASSES!")
        sys.exit(1)

if __name__ == "__main__":
    run_dryrun()
