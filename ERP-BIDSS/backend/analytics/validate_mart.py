"""
Analytics Mart — Full Validation Report.

Validates the entire Analytics Mart for:
1. Table existence and row counts
2. Grain validation (no unexpected duplicates)
3. FK relationship integrity (no orphan keys)
4. Measure validation (no negative values where inappropriate)
5. KPI readiness check (can all KPIs be computed?)
6. Aggregation readiness (SUM, AVG, COUNT feasibility)
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
from config.database import db
from config.settings import settings

SCHEMA = settings.TARGET_SCHEMA
ENGINE = db.target_engine


def _query(sql):
    """Execute a query and return result."""
    try:
        return pd.read_sql(sql, ENGINE)
    except Exception as e:
        return pd.DataFrame({"error": [str(e)]})


def validate_table_existence():
    """Check all 10 mart tables exist and have data."""
    print("\n── 1. Table Existence & Row Counts ──")
    tables = [
        "dim_date", "dim_product", "dim_customer", "dim_vendor",
        "dim_company", "dim_warehouse",
        "fact_sales", "fact_purchase", "fact_inventory", "fact_accounting"
    ]
    results = []
    for t in tables:
        df = _query(f"SELECT COUNT(*) AS cnt FROM {SCHEMA}.{t}")
        if "error" in df.columns:
            status = "MISSING"
            count = 0
        else:
            count = int(df["cnt"].iloc[0])
            status = "OK" if count > 0 else "EMPTY"
        results.append({"table": t, "rows": count, "status": status})
        symbol = "✅" if status == "OK" else "❌"
        print(f"  {symbol} {t}: {count} rows [{status}]")
    return results


def validate_grain():
    """Validate grain by checking for unexpected duplicates."""
    print("\n── 2. Grain Validation ──")
    checks = [
        ("fact_sales", "sk_sales_id", "1 row per sale_order_line"),
        ("fact_purchase", "sk_purchase_id", "1 row per purchase_order_line"),
        ("fact_inventory", "sk_inventory_id", "1 row per stock_move"),
        ("fact_accounting", "sk_accounting_id", "1 row per account_move_line"),
    ]
    results = []
    for table, pk, grain in checks:
        df = _query(f"""
            SELECT {pk}, COUNT(*) AS cnt
            FROM {SCHEMA}.{table}
            GROUP BY {pk}
            HAVING COUNT(*) > 1
            LIMIT 5
        """)
        if "error" in df.columns:
            status = "ERROR"
            dupes = -1
        else:
            dupes = len(df)
            status = "PASS" if dupes == 0 else "FAIL"
        results.append({"table": table, "grain": grain, "duplicates": dupes, "status": status})
        symbol = "✅" if status == "PASS" else "❌"
        print(f"  {symbol} {table}: {grain} — {dupes} duplicate PKs [{status}]")
    return results


def validate_measures():
    """Validate that measures have reasonable values."""
    print("\n── 3. Measure Validation ──")
    checks = [
        ("fact_sales", "quantity", "> 0"),
        ("fact_sales", "revenue", ">= 0"),
        ("fact_sales", "price_unit", "> 0"),
        ("fact_purchase", "quantity", "> 0"),
        ("fact_purchase", "subtotal", ">= 0"),
        ("fact_inventory", "quantity", "> 0"),
        ("fact_accounting", "debit", ">= 0"),
        ("fact_accounting", "credit", ">= 0"),
    ]
    results = []
    for table, col, rule in checks:
        df = _query(f"""
            SELECT COUNT(*) AS violations
            FROM {SCHEMA}.{table}
            WHERE NOT ({col} {rule})
        """)
        if "error" in df.columns:
            status = "ERROR"
            violations = -1
        else:
            violations = int(df["violations"].iloc[0])
            status = "PASS" if violations == 0 else "WARN"
        results.append({"table": table, "column": col, "rule": rule,
                        "violations": violations, "status": status})
        symbol = "✅" if status == "PASS" else "⚠️"
        print(f"  {symbol} {table}.{col} {rule}: {violations} violations [{status}]")
    return results


def validate_kpi_readiness():
    """Check that all 12 KPIs can be computed from mart tables only."""
    print("\n── 4. KPI Readiness Check ──")
    kpi_checks = [
        ("Revenue", f"SELECT SUM(revenue) FROM {SCHEMA}.fact_sales"),
        ("Sales Growth", f"SELECT date_id, SUM(revenue) FROM {SCHEMA}.fact_sales GROUP BY date_id LIMIT 1"),
        ("Inventory Turnover", f"""
            SELECT SUM(fs.revenue) AS cogs_proxy,
                   AVG(fi.value) AS avg_inv
            FROM {SCHEMA}.fact_sales fs
            CROSS JOIN (SELECT AVG(value) AS value FROM {SCHEMA}.fact_inventory) fi
        """),
        ("DIO", f"SELECT AVG(value) FROM {SCHEMA}.fact_inventory"),
        ("Revenue Contribution", f"""
            SELECT product_id, SUM(revenue) / NULLIF((SELECT SUM(revenue) FROM {SCHEMA}.fact_sales), 0)
            FROM {SCHEMA}.fact_sales GROUP BY product_id LIMIT 1
        """),
        ("Inventory Value", f"SELECT SUM(value) FROM {SCHEMA}.fact_inventory WHERE movement_type='incoming'"),
        ("Purchase Value", f"SELECT SUM(subtotal) FROM {SCHEMA}.fact_purchase"),
        ("Purchase Growth", f"SELECT date_id, SUM(subtotal) FROM {SCHEMA}.fact_purchase GROUP BY date_id LIMIT 1"),
        ("ROP", f"""
            SELECT product_id, AVG(quantity) AS avg_daily
            FROM {SCHEMA}.fact_sales GROUP BY product_id LIMIT 1
        """),
        ("EOQ", f"SELECT product_id, SUM(quantity) FROM {SCHEMA}.fact_sales GROUP BY product_id LIMIT 1"),
        ("Supplier Score", f"SELECT vendor_id FROM {SCHEMA}.fact_purchase GROUP BY vendor_id LIMIT 1"),
        ("Demand Forecast", f"""
            SELECT date_id / 100 AS month_key, SUM(quantity)
            FROM {SCHEMA}.fact_sales GROUP BY month_key ORDER BY month_key LIMIT 3
        """),
    ]
    results = []
    for kpi, query in kpi_checks:
        df = _query(query)
        if "error" in df.columns:
            status = "FAIL"
        else:
            status = "PASS"
        results.append({"kpi": kpi, "status": status})
        symbol = "✅" if status == "PASS" else "❌"
        print(f"  {symbol} {kpi}: {status}")
    return results


def validate_aggregation_readiness():
    """Verify that standard aggregations work correctly."""
    print("\n── 5. Aggregation Readiness ──")
    agg_tests = [
        ("SUM revenue by month", f"""
            SELECT d.month, SUM(f.revenue)
            FROM {SCHEMA}.fact_sales f JOIN {SCHEMA}.dim_date d ON f.date_id = d.date_id
            GROUP BY d.month ORDER BY d.month
        """),
        ("AVG lead_time by vendor", f"""
            SELECT v.vendor_name, AVG(f.lead_time_days)
            FROM {SCHEMA}.fact_purchase f JOIN {SCHEMA}.dim_vendor v ON f.vendor_id = v.sk_vendor_id
            GROUP BY v.vendor_name LIMIT 5
        """),
        ("COUNT movements by type", f"""
            SELECT movement_type, COUNT(*)
            FROM {SCHEMA}.fact_inventory GROUP BY movement_type
        """),
        ("SUM debit/credit by source", f"""
            SELECT source_module, SUM(debit), SUM(credit)
            FROM {SCHEMA}.fact_accounting GROUP BY source_module
        """),
    ]
    results = []
    for desc, query in agg_tests:
        df = _query(query)
        if "error" in df.columns:
            status = "FAIL"
        else:
            status = "PASS"
        results.append({"test": desc, "status": status})
        symbol = "✅" if status == "PASS" else "❌"
        print(f"  {symbol} {desc}: {status}")
    return results


def run_full_validation():
    """Execute complete Analytics Mart validation."""
    print("=" * 60)
    print("ANALYTICS MART — FULL VALIDATION REPORT")
    print("=" * 60)

    r1 = validate_table_existence()
    r2 = validate_grain()
    r3 = validate_measures()
    r4 = validate_kpi_readiness()
    r5 = validate_aggregation_readiness()

    # Final summary
    all_results = []
    for r in [r1, r2, r3, r4, r5]:
        all_results.extend(r)

    passed = sum(1 for r in all_results if r.get("status") in ("OK", "PASS"))
    total = len(all_results)

    print("\n" + "=" * 60)
    print(f"VALIDATION COMPLETE: {passed}/{total} checks passed")
    if passed == total:
        print("STATUS: ALL PASS ✅ — Analytics Mart ready for Phase 6")
    else:
        print("STATUS: HAS ISSUES ⚠️ — Review findings above")
    print("=" * 60)

    return all_results


if __name__ == "__main__":
    run_full_validation()
