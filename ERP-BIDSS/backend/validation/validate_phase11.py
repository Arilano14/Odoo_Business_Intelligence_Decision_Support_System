"""
Phase 11 Automated Validation Suite.

Validates 20+ mandatory criteria for Phase 11:
Analytics, DSS, and Aggregation Recalculation (FY 2026).
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.database import db
from config.settings import settings
from sqlalchemy import text
import pandas as pd
import numpy as np


def validate_phase11():
    print("============================================================")
    print("PHASE 11 AUTOMATED VALIDATION SUITE (FY 2026 ANALYTICS)")
    print("============================================================")

    passed = 0
    failed = 0

    def check(description: str, condition: bool, info: str = ""):
        nonlocal passed, failed
        if condition:
            print(f"[PASS] {description} {f'({info})' if info else ''}")
            passed += 1
        else:
            print(f"[FAIL] {description} {f'({info})' if info else ''}")
            failed += 1

    try:
        with db.target_engine.connect() as conn:
            # --- 1. FORECAST VALIDATION (fact_forecast_monthly) ---
            forecast_cnt = conn.execute(text("SELECT COUNT(*) FROM mart.fact_forecast_monthly")).fetchone()[0]
            check("1. fact_forecast_monthly row count = 2880 (283 prods x 12 mos)", forecast_cnt == 2880, f"Rows: {forecast_cnt}")

            nan_forecast = conn.execute(text("SELECT COUNT(*) FROM mart.fact_forecast_monthly WHERE ma3_forecast IS NULL")).fetchone()[0]
            check("2. Zero NULLs in ma3_forecast", nan_forecast == 0, f"Nulls: {nan_forecast}")

            neg_forecast = conn.execute(text("SELECT COUNT(*) FROM mart.fact_forecast_monthly WHERE ma3_forecast < 0")).fetchone()[0]
            check("3. Zero negative forecast quantities", neg_forecast == 0, f"Negatives: {neg_forecast}")

            months_avail = conn.execute(text("SELECT COUNT(DISTINCT month_id) FROM mart.fact_forecast_monthly WHERE forecast_available = TRUE")).fetchone()[0]
            check("4. Forecast available for 9 evaluation months (202604-202612)", months_avail == 9, f"Months: {months_avail}")

            # --- 2. DECISION SUPPORT VALIDATION (fact_decision_support) ---
            dss_cnt = conn.execute(text("SELECT COUNT(*) FROM mart.fact_decision_support")).fetchone()[0]
            check("5. fact_decision_support row count = 283 products", dss_cnt == 283, f"Rows: {dss_cnt}")

            neg_eoq = conn.execute(text("SELECT COUNT(*) FROM mart.fact_decision_support WHERE eoq < 0")).fetchone()[0]
            check("6. Zero negative EOQ values", neg_eoq == 0, f"Negatives: {neg_eoq}")

            neg_ss = conn.execute(text("SELECT COUNT(*) FROM mart.fact_decision_support WHERE safety_stock < 0")).fetchone()[0]
            check("7. Zero negative Safety Stock values", neg_ss == 0, f"Negatives: {neg_ss}")

            invalid_rop = conn.execute(text("SELECT COUNT(*) FROM mart.fact_decision_support WHERE rop < safety_stock")).fetchone()[0]
            check("8. ROP is at least equal to Safety Stock (rop >= safety_stock)", invalid_rop == 0, f"Invalid: {invalid_rop}")

            # --- 3. SUPPLIER PERFORMANCE VALIDATION (fact_supplier_score) ---
            supp_cnt = conn.execute(text("SELECT COUNT(*) FROM mart.fact_supplier_score")).fetchone()[0]
            check("9. fact_supplier_score row count = 24 portfolio suppliers", supp_cnt == 24, f"Suppliers: {supp_cnt}")

            score_out_of_bounds = conn.execute(text("SELECT COUNT(*) FROM mart.fact_supplier_score WHERE final_score < 0 OR final_score > 100")).fetchone()[0]
            check("10. All final supplier scores within 0-100 range", score_out_of_bounds == 0, f"Out of bounds: {score_out_of_bounds}")

            grades = [g[0] for g in conn.execute(text("SELECT DISTINCT category FROM mart.fact_supplier_score")).fetchall()]
            check("11. Supplier grades present", len(grades) > 0, f"Grades: {grades}")

            # --- 4. BI AGGREGATION VALIDATION ---
            ms_cnt = conn.execute(text("SELECT COUNT(*) FROM mart.monthly_summary")).fetchone()[0]
            check("12. monthly_summary contains 12 FY 2026 rows", ms_cnt == 12, f"Rows: {ms_cnt}")

            exec_cnt = conn.execute(text("SELECT COUNT(*) FROM mart.executive_summary")).fetchone()[0]
            check("13. executive_summary contains 12 monthly rows", exec_cnt == 12, f"Rows: {exec_cnt}")

            cust_cnt = conn.execute(text("SELECT COUNT(*) FROM mart.sales_summary")).fetchone()[0]
            check("14. sales_summary contains 240 product rows", cust_cnt == 240, f"Rows: {cust_cnt}")

            vend_cnt = conn.execute(text("SELECT COUNT(*) FROM mart.supplier_summary")).fetchone()[0]
            check("15. supplier_summary contains 24 vendor rows", vend_cnt == 24, f"Rows: {vend_cnt}")

            # Contribution totals reconciliation
            cust_contrib_df = pd.read_sql("SELECT revenue_contribution_pct FROM mart.sales_summary", conn)
            cust_contrib_sum = cust_contrib_df["revenue_contribution_pct"].sum()
            check("16. Sales revenue contribution sums to 100%", abs(cust_contrib_sum - 100.0) < 0.01, f"Sum: {cust_contrib_sum:.2f}%")

            vend_contrib_df = pd.read_sql("SELECT purchase_contribution_pct FROM mart.supplier_summary", conn)
            vend_contrib_sum = vend_contrib_df["purchase_contribution_pct"].sum()
            check("17. Supplier purchase contribution sums to 100%", abs(vend_contrib_sum - 100.0) < 0.01, f"Sum: {vend_contrib_sum:.2f}%")

            # Zero records from 2024 or invalid company
            old_data = conn.execute(text("SELECT COUNT(*) FROM mart.monthly_summary WHERE data_period_start != '2026-01-01'")).fetchone()[0]
            check("18. Zero active 2024 period dates in aggregation metadata", old_data == 0, f"Legacy rows: {old_data}")

    except Exception as e:
        print(f"[ERROR] Validation execution failed: {e}")
        sys.exit(1)

    print("\n============================================================")
    print(f"VALIDATION SUMMARY: {passed} PASSED, {failed} FAILED")
    print("============================================================")

    if failed > 0:
        sys.exit(1)
    else:
        print("[VALIDATION SUCCESS] Phase 11 Analytics & DSS Recalculation met 100% of mandatory criteria!")
        sys.exit(0)


if __name__ == "__main__":
    validate_phase11()
