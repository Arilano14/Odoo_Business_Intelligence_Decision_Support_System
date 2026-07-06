"""
Analytics Mart — Relationship & Integrity Validator.

Verifies that all foreign keys in fact tables
reference valid surrogate keys in dimension tables.
No orphan keys allowed.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
from config.database import db
from config.settings import settings


SCHEMA = settings.TARGET_SCHEMA

# Relationship matrix: (fact_table, fk_column) → (dim_table, pk_column)
RELATIONSHIPS = [
    ("fact_sales", "date_id", "dim_date", "date_id"),
    ("fact_sales", "product_id", "dim_product", "sk_product_id"),
    ("fact_sales", "customer_id", "dim_customer", "sk_customer_id"),
    ("fact_sales", "company_id", "dim_company", "sk_company_id"),

    ("fact_purchase", "date_id", "dim_date", "date_id"),
    ("fact_purchase", "product_id", "dim_product", "sk_product_id"),
    ("fact_purchase", "vendor_id", "dim_vendor", "sk_vendor_id"),
    ("fact_purchase", "company_id", "dim_company", "sk_company_id"),

    ("fact_inventory", "date_id", "dim_date", "date_id"),
    ("fact_inventory", "product_id", "dim_product", "sk_product_id"),
    ("fact_inventory", "warehouse_id", "dim_warehouse", "sk_warehouse_id"),

    ("fact_accounting", "date_id", "dim_date", "date_id"),
    ("fact_accounting", "company_id", "dim_company", "sk_company_id"),
]


def check_relationship(fact_table, fk_col, dim_table, pk_col):
    """Check a single FK relationship for orphan keys."""
    query = f"""
        SELECT COUNT(*) AS orphan_count
        FROM {SCHEMA}.{fact_table} f
        LEFT JOIN {SCHEMA}.{dim_table} d ON f.{fk_col} = d.{pk_col}
        WHERE d.{pk_col} IS NULL
          AND f.{fk_col} IS NOT NULL
          AND f.{fk_col} != 0
    """
    try:
        result = pd.read_sql(query, db.target_engine)
        orphans = int(result["orphan_count"].iloc[0])
        status = "PASS" if orphans == 0 else "FAIL"
        return {
            "fact": fact_table,
            "fk": fk_col,
            "dim": dim_table,
            "pk": pk_col,
            "orphans": orphans,
            "status": status,
        }
    except Exception as e:
        return {
            "fact": fact_table,
            "fk": fk_col,
            "dim": dim_table,
            "pk": pk_col,
            "orphans": -1,
            "status": f"ERROR: {e}",
        }


def validate_all_relationships():
    """Validate all FK relationships in Analytics Mart."""
    print("\n" + "=" * 60)
    print("PHASE 5 — Relationship Validation")
    print("=" * 60)

    results = []
    for fact, fk, dim, pk in RELATIONSHIPS:
        result = check_relationship(fact, fk, dim, pk)
        results.append(result)
        symbol = "✅" if result["status"] == "PASS" else "❌"
        print(f"  {symbol} {fact}.{fk} → {dim}.{pk}: {result['status']} ({result['orphans']} orphans)")

    # Summary
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] != "PASS")
    print(f"\n── Summary ──")
    print(f"  PASS: {passed}/{len(results)}")
    print(f"  FAIL: {failed}/{len(results)}")
    print(f"  Overall: {'ALL PASS ✅' if failed == 0 else 'HAS FAILURES ❌'}")

    return results


if __name__ == "__main__":
    validate_all_relationships()
