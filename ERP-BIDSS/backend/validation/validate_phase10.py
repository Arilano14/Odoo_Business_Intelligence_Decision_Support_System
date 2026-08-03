"""
Phase 10 Automated Validation Suite.

Validates 12 mandatory criteria for Phase 10:
ETL Pipeline Re-alignment & Data Warehouse Refresh (FY 2026).
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.database import db
from config.settings import settings
from sqlalchemy import text


def validate_phase10():
    print("============================================================")
    print("PHASE 10 AUTOMATED VALIDATION SUITE (FY 2026)")
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
            # 1. Target schema exists
            schemas = [s[0] for s in conn.execute(text("SELECT schema_name FROM information_schema.schemata")).fetchall()]
            check("1. Target schema 'mart' exists", settings.TARGET_SCHEMA in schemas)

            # 2. Required tables exist
            tables = [t[0] for t in conn.execute(text(f"SELECT table_name FROM information_schema.tables WHERE table_schema='{settings.TARGET_SCHEMA}'")).fetchall()]
            required_tables = ["dim_date", "dim_product", "dim_customer", "dim_vendor", "dim_company", "dim_warehouse", "fact_sales", "fact_purchase", "fact_inventory"]
            missing = [t for t in required_tables if t not in tables]
            check("2. Required Star Schema tables exist", len(missing) == 0, f"Missing: {missing}")

            # 3. Dimension row counts
            dim_date_cnt = conn.execute(text("SELECT COUNT(*) FROM mart.dim_date")).fetchone()[0]
            check("3. dim_date row count = 365 (FY 2026)", dim_date_cnt == 365, f"Count: {dim_date_cnt}")

            dim_prod_cnt = conn.execute(text("SELECT COUNT(*) FROM mart.dim_product")).fetchone()[0]
            check("4. dim_product contains portfolio products", dim_prod_cnt >= 240, f"Count: {dim_prod_cnt}")

            dim_cust_cnt = conn.execute(text("SELECT COUNT(*) FROM mart.dim_customer")).fetchone()[0]
            check("5. dim_customer contains 48 portfolio customers", dim_cust_cnt == 48, f"Count: {dim_cust_cnt}")

            dim_vend_cnt = conn.execute(text("SELECT COUNT(*) FROM mart.dim_vendor")).fetchone()[0]
            check("6. dim_vendor contains 24 portfolio suppliers", dim_vend_cnt == 24, f"Count: {dim_vend_cnt}")

            dim_comp_cnt = conn.execute(text("SELECT COUNT(*) FROM mart.dim_company")).fetchone()[0]
            check("7. dim_company contains 1 main company", dim_comp_cnt == 1, f"Count: {dim_comp_cnt}")

            # 4. Fact tables non-empty
            fact_sales_cnt = conn.execute(text("SELECT COUNT(*) FROM mart.fact_sales")).fetchone()[0]
            check("8. fact_sales is non-empty", fact_sales_cnt > 0, f"Rows: {fact_sales_cnt}")

            fact_pur_cnt = conn.execute(text("SELECT COUNT(*) FROM mart.fact_purchase")).fetchone()[0]
            check("9. fact_purchase is non-empty", fact_pur_cnt > 0, f"Rows: {fact_pur_cnt}")

            fact_inv_cnt = conn.execute(text("SELECT COUNT(*) FROM mart.fact_inventory")).fetchone()[0]
            check("10. fact_inventory is non-empty", fact_inv_cnt > 0, f"Rows: {fact_inv_cnt}")

            # 5. Date range equals FY 2026
            min_date = conn.execute(text("SELECT MIN(date_id) FROM mart.dim_date")).fetchone()[0]
            max_date = conn.execute(text("SELECT MAX(date_id) FROM mart.dim_date")).fetchone()[0]
            check("11. Calendar date range is FY 2026 (20260101-20261231)", min_date == 20260101 and max_date == 20261231, f"Range: {min_date}..{max_date}")

            sales_min_date = conn.execute(text("SELECT MIN(date_id) FROM mart.fact_sales")).fetchone()[0]
            sales_max_date = conn.execute(text("SELECT MAX(date_id) FROM mart.fact_sales")).fetchone()[0]
            check("12. Sales transaction dates within FY 2026", str(sales_min_date).startswith("2026") and str(sales_max_date).startswith("2026"), f"Sales range: {sales_min_date}..{sales_max_date}")

            # 6. Orphan FK checks
            orphan_prod = conn.execute(text("SELECT COUNT(*) FROM mart.fact_sales WHERE product_id NOT IN (SELECT sk_product_id FROM mart.dim_product)")).fetchone()[0]
            check("13. Zero orphan product keys in fact_sales", orphan_prod == 0, f"Orphans: {orphan_prod}")

            orphan_cust = conn.execute(text("SELECT COUNT(*) FROM mart.fact_sales WHERE customer_id NOT IN (SELECT sk_customer_id FROM mart.dim_customer)")).fetchone()[0]
            check("14. Zero orphan customer keys in fact_sales", orphan_cust == 0, f"Orphans: {orphan_cust}")

            # 7. No 2024 dates in mart
            old_sales_dates = conn.execute(text("SELECT COUNT(*) FROM mart.fact_sales WHERE date_id < 20260101 OR date_id > 20261231")).fetchone()[0]
            check("15. Zero records outside FY 2026 in fact_sales", old_sales_dates == 0, f"Out of range: {old_sales_dates}")

    except Exception as e:
        print(f"[ERROR] Validation execution failed: {e}")
        sys.exit(1)

    print("\n============================================================")
    print(f"VALIDATION SUMMARY: {passed} PASSED, {failed} FAILED")
    print("============================================================")

    if failed > 0:
        sys.exit(1)
    else:
        print("[VALIDATION SUCCESS] Phase 10 Data Warehouse Refresh met 100% of mandatory criteria!")
        sys.exit(0)


if __name__ == "__main__":
    validate_phase10()
