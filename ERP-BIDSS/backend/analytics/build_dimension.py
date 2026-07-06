"""
Analytics Mart — Dimension Table Builder.

Builds all 6 dimension tables from Odoo 18 source data
and loads them into PostgreSQL schema 'mart'.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np
from config.database import db
from config.settings import settings


def build_dim_date(start="2024-01-01", end="2024-12-31"):
    """Generate calendar dimension table (365 rows for 1 year)."""
    dates = pd.date_range(start=start, end=end, freq="D")
    dim = pd.DataFrame({
        "date_id": dates.strftime("%Y%m%d").astype(int),
        "full_date": dates.date,
        "year": dates.year.astype(int),
        "month": dates.month.astype(int),
        "day": dates.day.astype(int),
        "month_name": dates.strftime("%B"),
        "quarter": dates.quarter.astype(int),
        "day_of_week": dates.strftime("%A"),
        "is_weekend": dates.dayofweek.isin([5, 6]),
    })
    print(f"  [OK] dim_date: {len(dim)} rows generated")
    return dim


def build_dim_product(engine):
    """Build product dimension from Odoo product_product + template + category."""
    query = """
        SELECT
            pp.id           AS odoo_product_id,
            pt.name         AS product_name,
            pc.name         AS category,
            pp.default_code AS default_code,
            pt.list_price   AS list_price,
            pt.standard_price AS standard_price
        FROM product_product pp
        JOIN product_template pt ON pp.product_tmpl_id = pt.id
        LEFT JOIN product_category pc ON pt.categ_id = pc.id
        WHERE pp.active = True
        ORDER BY pp.id
    """
    try:
        dim = pd.read_sql(query, engine)
        dim.insert(0, "sk_product_id", range(1, len(dim) + 1))
        # Fill nulls for Power BI compatibility
        dim["category"] = dim["category"].fillna("Uncategorized")
        dim["default_code"] = dim["default_code"].fillna("")
        dim["list_price"] = dim["list_price"].fillna(0)
        dim["standard_price"] = dim["standard_price"].fillna(0)
        print(f"  [OK] dim_product: {len(dim)} rows")
        return dim
    except Exception as e:
        print(f"  [FAIL] dim_product: {e}")
        return pd.DataFrame()


def build_dim_customer(engine):
    """Build customer dimension from res_partner (customer_rank > 0)."""
    query = """
        SELECT
            rp.id   AS odoo_partner_id,
            rp.name AS customer_name,
            rp.city AS city
        FROM res_partner rp
        WHERE rp.customer_rank > 0 AND rp.active = True
        ORDER BY rp.id
    """
    try:
        dim = pd.read_sql(query, engine)
        dim.insert(0, "sk_customer_id", range(1, len(dim) + 1))
        dim["industry"] = "Distribution"  # Default for MVP simulation
        dim["city"] = dim["city"].fillna("Unknown")
        print(f"  [OK] dim_customer: {len(dim)} rows")
        return dim
    except Exception as e:
        print(f"  [FAIL] dim_customer: {e}")
        return pd.DataFrame()


def build_dim_vendor(engine):
    """Build vendor dimension from res_partner (supplier_rank > 0)."""
    query = """
        SELECT
            rp.id   AS odoo_partner_id,
            rp.name AS vendor_name,
            rp.city AS city
        FROM res_partner rp
        WHERE rp.supplier_rank > 0 AND rp.active = True
        ORDER BY rp.id
    """
    try:
        dim = pd.read_sql(query, engine)
        dim.insert(0, "sk_vendor_id", range(1, len(dim) + 1))
        dim["city"] = dim["city"].fillna("Unknown")
        print(f"  [OK] dim_vendor: {len(dim)} rows")
        return dim
    except Exception as e:
        print(f"  [FAIL] dim_vendor: {e}")
        return pd.DataFrame()


def build_dim_company(engine):
    """Build company dimension from res_company."""
    query = "SELECT id AS odoo_company_id, name AS company_name FROM res_company"
    try:
        dim = pd.read_sql(query, engine)
        dim.insert(0, "sk_company_id", range(1, len(dim) + 1))
        print(f"  [OK] dim_company: {len(dim)} rows")
        return dim
    except Exception as e:
        print(f"  [FAIL] dim_company: {e}")
        return pd.DataFrame()


def build_dim_warehouse(engine):
    """Build warehouse dimension from stock_warehouse."""
    query = """
        SELECT
            id   AS odoo_warehouse_id,
            name AS warehouse_name,
            code AS warehouse_code
        FROM stock_warehouse
    """
    try:
        dim = pd.read_sql(query, engine)
        dim.insert(0, "sk_warehouse_id", range(1, len(dim) + 1))
        print(f"  [OK] dim_warehouse: {len(dim)} rows")
        return dim
    except Exception as e:
        print(f"  [FAIL] dim_warehouse: {e}")
        return pd.DataFrame()


def load_dimension(df, table_name):
    """Load a single dimension table into mart schema (full refresh)."""
    if df.empty:
        print(f"  [SKIP] {table_name}: empty")
        return 0
    try:
        df.to_sql(
            table_name,
            db.target_engine,
            schema=settings.TARGET_SCHEMA,
            if_exists="replace",
            index=False,
            method="multi",
        )
        print(f"  [LOADED] {table_name}: {len(df)} rows → mart.{table_name}")
        return len(df)
    except Exception as e:
        print(f"  [FAIL] Loading {table_name}: {e}")
        return 0


def build_all_dimensions():
    """Build and load all 6 dimension tables."""
    print("\n" + "=" * 60)
    print("PHASE 5 — Building Dimension Tables")
    print("=" * 60)

    source = db.source_engine
    results = {}

    # 1. dim_date (generated, no source needed)
    dim_date = build_dim_date("2024-01-01", "2024-12-31")
    results["dim_date"] = load_dimension(dim_date, "dim_date")

    # 2-6. Dimensions from Odoo source
    dims = {
        "dim_product": build_dim_product(source),
        "dim_customer": build_dim_customer(source),
        "dim_vendor": build_dim_vendor(source),
        "dim_company": build_dim_company(source),
        "dim_warehouse": build_dim_warehouse(source),
    }

    for name, df in dims.items():
        results[name] = load_dimension(df, name)

    print("\n── Dimension Summary ──")
    total = 0
    for name, count in results.items():
        print(f"  {name}: {count} rows")
        total += count
    print(f"  TOTAL: {total} rows")

    return results, {
        "dim_date": dim_date,
        **dims,
    }


if __name__ == "__main__":
    build_all_dimensions()
