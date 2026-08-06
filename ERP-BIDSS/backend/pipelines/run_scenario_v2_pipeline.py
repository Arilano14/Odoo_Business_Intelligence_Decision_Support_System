"""
Phase 11.4 — Full ETL & Data Mart Benchmark Pipeline (Scenario V2)
===================================================================
1. Extracts confirmed Scenario V2 sales from Odoo clone database into mart.fact_sales.
2. Runs 6 candidate forecasting models across 36 months (2024-2026).
3. Selects Champion models based ONLY on 2025 data.
4. Evaluates final holdout performance based ONLY on 2026 data (FY 2026).
5. Writes exact row counts to Data Mart PostgreSQL:
   - mart.fact_forecast_model_comparison (17,280 rows)
   - mart.fact_forecast_monthly (2,880 rows)
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


def classify_demand_pattern(history: np.ndarray) -> str:
    nonzero = history[history > 0]
    if len(nonzero) == 0:
        return "Intermittent"
    adi = len(history) / len(nonzero)
    mean_d = np.mean(nonzero)
    std_d = np.std(nonzero, ddof=1) if len(nonzero) > 1 else 0.0
    cv2 = (std_d / mean_d) ** 2 if mean_d > 0 else 0.0
    
    if adi < 1.32 and cv2 < 0.49:
        return "Smooth"
    elif adi < 1.32 and cv2 >= 0.49:
        return "Erratic"
    elif adi >= 1.32 and cv2 < 0.49:
        return "Intermittent"
    else:
        return "Lumpy"


def run_pipeline():
    print("=" * 75)
    print("PHASE 11.4 — ETL REFRESH & DATA MART BENCHMARK (SCENARIO V2)")
    print("=" * 75)

    # 1. Fetch 240 Verified Portfolio SKUs
    with db.target_engine.connect() as conn:
        prod_df = pd.read_sql(text(f"""
            SELECT sk_product_id AS product_id, product_name, category, default_code, standard_price, list_price
            FROM {SCHEMA}.dim_product
            WHERE default_code LIKE 'PORTFOLIO_2026_%'
            ORDER BY product_id
        """), conn)

    print(f"Verified Portfolio Scope: {len(prod_df)} SKUs")
    if len(prod_df) != 240:
        print(f"SCOPE FAILURE: Expected exactly 240 portfolio SKUs, got {len(prod_df)}")
        sys.exit(1)

    # 2. Rebuild mart.fact_sales from Odoo ORM confirmed orders
    print("\nRebuilding mart.fact_sales from Odoo Scenario V2 Sales Orders...")
    fact_sales_query = f"""
        SELECT 
            dp.sk_product_id AS product_id,
            COALESCE(dc.sk_customer_id, 1) AS customer_id,
            2 AS company_id,
            TO_CHAR(so.date_order, 'YYYYMMDD')::INT AS date_id,
            sol.product_uom_qty::NUMERIC AS quantity,
            sol.price_unit::NUMERIC AS price_unit,
            0.0::NUMERIC AS discount,
            (sol.product_uom_qty * sol.price_unit)::NUMERIC AS subtotal,
            (sol.product_uom_qty * sol.price_unit)::NUMERIC AS revenue,
            (sol.product_uom_qty * dp.standard_price)::NUMERIC AS cost,
            (sol.product_uom_qty * (sol.price_unit - dp.standard_price))::NUMERIC AS margin
        FROM sale_order_line sol
        JOIN sale_order so ON sol.order_id = so.id
        JOIN product_product pp ON sol.product_id = pp.id
        JOIN {SCHEMA}.dim_product dp ON pp.default_code = dp.default_code
        LEFT JOIN res_partner rp ON so.partner_id = rp.id
        LEFT JOIN {SCHEMA}.dim_customer dc ON rp.id = dc.odoo_partner_id
        WHERE so.company_id = 2
          AND so.state = 'sale'
          AND so.client_order_ref LIKE 'SYNTH_V2_%'
    """
    
    with db.source_engine.connect() as source_conn:
        fact_sales_df = pd.read_sql(text(fact_sales_query), source_conn)

    print(f"Extracted {len(fact_sales_df)} sales line records for Data Mart.")
    
    # Save to mart.fact_sales using TRUNCATE & append
    with db.target_engine.connect() as target_conn:
        target_conn.execute(text(f"TRUNCATE TABLE {SCHEMA}.fact_sales"))
        target_conn.commit()
        fact_sales_df.to_sql('fact_sales', target_conn, schema=SCHEMA, if_exists='append', index=False)
        target_conn.commit()
    print("  [OK] Successfully refreshed mart.fact_sales!")

    # 3. Aggregate Monthly Demand (2024–2026) per Product
    sales_agg_query = f"""
        SELECT 
            product_id,
            SUBSTRING(date_id::TEXT, 1, 6)::INT AS month_id,
            SUM(quantity) AS actual_qty
        FROM {SCHEMA}.fact_sales
        GROUP BY product_id, month_id
        ORDER BY product_id, month_id
    """
    with db.target_engine.connect() as target_conn:
        sales_agg_df = pd.read_sql(text(sales_agg_query), target_conn)

    # Build 36-month matrix (202401 to 202612) for all 240 products
    all_products = prod_df['product_id'].values
    all_months = []
    for yr in [2024, 2025, 2026]:
        for mo in range(1, 13):
            all_months.append(yr * 100 + mo)

    full_idx = pd.MultiIndex.from_product([all_products, all_months], names=['product_id', 'month_id'])
    sales_grid = sales_agg_df.set_index(['product_id', 'month_id']).reindex(full_idx, fill_value=0.0).reset_index()
    sales_grid = sales_grid.sort_values(['product_id', 'month_id']).reset_index(drop=True)

    # 4. Classify Demand Patterns using 2024–2025 History (Months 1..24)
    patterns = {}
    for p_id in all_products:
        p_hist_2024_2025 = sales_grid[(sales_grid['product_id'] == p_id) & (sales_grid['month_id'] < 202601)]['actual_qty'].values
        patterns[p_id] = classify_demand_pattern(p_hist_2024_2025)

    prod_df['demand_pattern'] = prod_df['product_id'].map(patterns)

    # 5. Run Rolling-Origin Benchmark
    fy2026_months = [202601 + i for i in range(12)]
    
    model_evals_2025 = []
    model_evals_2026 = []

    for p_id in all_products:
        full_series = sales_grid[sales_grid['product_id'] == p_id].sort_values('month_id')['actual_qty'].values
        pattern = patterns[p_id]
        
        for model_name, model_fn in MODEL_FUNCS.items():
            # 2025 Evaluation (Months 13..24, indices 12..23)
            for step_idx in range(12, 24):
                actual = full_series[step_idx]
                history = full_series[:step_idx]
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
                m_id = fy2026_months[step_idx - 24]
                actual = full_series[step_idx]
                history = full_series[:step_idx]
                fct_raw = max(0.0, float(model_fn(history)))
                fct_round = max(0.0, float(np.round(fct_raw)))
                abs_err = abs(actual - fct_raw)
                bias = fct_raw - actual
                
                model_evals_2026.append({
                    'product_id': int(p_id), 'model_name': model_name, 'demand_pattern': pattern,
                    'month_id': int(m_id), 'actual_qty': float(actual), 'forecast_raw': round(fct_raw, 4),
                    'forecast_rounded': float(fct_round), 'absolute_error': round(abs_err, 4), 'bias': round(bias, 4)
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
    stats_2025 = stats_2025.sort_values(['product_id', 'wape', 'mae', 'abs_bias']).reset_index(drop=True)
    
    champions_2025 = stats_2025.groupby('product_id').first().reset_index()
    champion_map = set(zip(champions_2025['product_id'], champions_2025['model_name']))

    print("\nChampion Model Distribution (Selected on 2025 Data):")
    print(champions_2025['model_name'].value_counts().to_string())

    # 7. Apply Champion Selection to 2026 Holdout Data
    df_2026['is_champion'] = df_2026.apply(
        lambda r: (r['product_id'], r['model_name']) in champion_map, axis=1
    )
    
    # Compute 2026 Model Summary Metrics
    for p_id in all_products:
        for m_name in MODEL_FUNCS.keys():
            sub = df_2026[(df_2026['product_id'] == p_id) & (df_2026['model_name'] == m_name)]
            t_act = sub['actual_qty'].sum()
            t_err = sub['absolute_error'].sum()
            w_val = t_err / t_act if t_act > 0 else 0.0
            acc_val = max(0.0, 1.0 - w_val)
            mae_val = sub['absolute_error'].mean()
            
            mask = (df_2026['product_id'] == p_id) & (df_2026['model_name'] == m_name)
            df_2026.loc[mask, 'wape'] = round(w_val, 4)
            df_2026.loc[mask, 'accuracy'] = round(acc_val, 4)
            df_2026.loc[mask, 'mae'] = round(mae_val, 4)

    df_2026['scenario_version'] = SCENARIO_VERSION
    df_2026['synthetic_batch_id'] = BATCH_ID

    # 8. Write Results to Data Mart Tables
    print("\nWriting final benchmark results to Data Mart PostgreSQL...")

    # Table 1: mart.fact_forecast_model_comparison (17,280 rows)
    db_comp_df = df_2026[[
        'product_id', 'model_name', 'demand_pattern', 'month_id',
        'actual_qty', 'forecast_raw', 'forecast_rounded',
        'absolute_error', 'bias', 'wape', 'accuracy', 'mae', 'is_champion',
        'scenario_version', 'synthetic_batch_id'
    ]]
    with db.target_engine.connect() as conn:
        db_comp_df.to_sql('fact_forecast_model_comparison', conn, schema=SCHEMA, if_exists='replace', index=False)
        conn.commit()
    print(f"  [OK] Successfully wrote {len(db_comp_df)} rows to {SCHEMA}.fact_forecast_model_comparison (Target: 17,280)")

    # Table 2: mart.fact_forecast_monthly (2,880 rows for Champion Models)
    champ_2026 = df_2026[df_2026['is_champion']].copy()
    
    def classify_champion_interpretation(row):
        act, fct = row['actual_qty'], row['forecast_raw']
        if act == 0 and fct < 0.05:
            return "Correct Zero Forecast"
        elif act == 0 and fct >= 0.05:
            return "Zero-Demand Over-Forecast"
        elif act > 0 and fct < 0.05:
            return "Missed Demand"
        err_pct = (row['absolute_error'] / act * 100) if act > 0 else 0
        if err_pct <= 10:
            return "Accurate"
        elif fct > act:
            return "Over-Forecast"
        else:
            return "Under-Forecast"

    champ_2026['interpretation'] = champ_2026.apply(classify_champion_interpretation, axis=1)
    champ_2026['ma3_forecast'] = champ_2026['forecast_rounded']
    champ_2026['forecast_error_pct'] = np.where(
        champ_2026['actual_qty'] > 0,
        np.round(champ_2026['absolute_error'] / champ_2026['actual_qty'] * 100, 2),
        np.nan
    )
    champ_2026['forecast_available'] = True

    db_champ_df = champ_2026[[
        'product_id', 'month_id', 'model_name', 'demand_pattern',
        'forecast_raw', 'forecast_rounded', 'is_champion',
        'actual_qty', 'absolute_error', 'forecast_error_pct',
        'forecast_available', 'interpretation',
        'scenario_version', 'synthetic_batch_id'
    ]].rename(columns={'model_name': 'champion_model'})

    with db.target_engine.connect() as conn:
        db_champ_df.to_sql('fact_forecast_monthly', conn, schema=SCHEMA, if_exists='replace', index=False)
        conn.commit()
    print(f"  [OK] Successfully wrote {len(db_champ_df)} rows to {SCHEMA}.fact_forecast_monthly (Target: 2,880)")

    # 9. Final Reconciliation & Acceptance Report
    tot_act_2026 = champ_2026['actual_qty'].sum()
    tot_err_2026 = champ_2026['absolute_error'].sum()
    holdout_wape_2026 = tot_err_2026 / tot_act_2026
    holdout_acc_2026 = max(0.0, 1.0 - holdout_wape_2026) * 100

    pos_2026 = champ_2026[champ_2026['actual_qty'] > 0]
    pos_act_2026 = pos_2026['actual_qty'].sum()
    pos_err_2026 = pos_2026['absolute_error'].sum()
    pos_wape_2026 = pos_err_2026 / pos_act_2026
    pos_acc_2026 = max(0.0, 1.0 - pos_wape_2026) * 100

    print("\n" + "=" * 75)
    print("PHASE 11.4 FINAL HOLDOUT ACCURACY RECONCILIATION (FY 2026):")
    print("=" * 75)
    print(f"Total Holdout Actual Quantity:           {tot_act_2026:,.2f}")
    print(f"Total Holdout Absolute Error:          {tot_err_2026:,.2f}")
    print(f"VERIFIED PORTFOLIO CHAMPION HOLDOUT WAPE: {holdout_wape_2026 * 100:.2f}%")
    print(f"VERIFIED PORTFOLIO CHAMPION ACCURACY (KPI): {holdout_acc_2026:.2f}%")
    print(f"Positive-Demand Holdout WAPE:           {pos_wape_2026 * 100:.2f}%")
    print(f"Positive-Demand Holdout Accuracy:       {pos_acc_2026:.2f}%")

    assert len(db_comp_df) == 17280, f"Expected 17,280 comparison rows, got {len(db_comp_df)}"
    assert len(db_champ_df) == 2880, f"Expected 2,880 champion rows, got {len(db_champ_df)}"

    print("\n" + "=" * 75)
    print("FINAL ACCEPTANCE EVALUATION STATUS:")
    if holdout_wape_2026 <= 0.20 and holdout_acc_2026 >= 80.0:
        print("STATUS: PASS (Verified Portfolio Champion Holdout Accuracy >= 80%)")
    else:
        print("STATUS: FAILED (Portfolio Champion Holdout WAPE > 20%)")
    print("=" * 75)

if __name__ == "__main__":
    run_pipeline()
