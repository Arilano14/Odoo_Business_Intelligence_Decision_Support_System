"""
Load module — Load transformed data into Analytics Mart.

Loads Dimension and Fact tables into PostgreSQL schema 'mart'
using pandas to_sql with full refresh (truncate & load) strategy.
"""
import pandas as pd
from config.database import db
from config.settings import settings


# Loading order: Dimensions first, then Facts (FK dependency)
LOAD_ORDER = [
    "dim_date",
    "dim_product",
    "dim_customer",
    "dim_vendor",
    "dim_company",
    "dim_warehouse",
    "fact_sales",
    "fact_purchase",
    "fact_inventory",
    "fact_accounting",
]


def load_table(df: pd.DataFrame, table_name: str) -> int:
    """Load a single DataFrame into Analytics Mart.

    Uses full refresh strategy (if_exists='replace') for MVP.

    Args:
        df: DataFrame to load
        table_name: Target table name in schema 'mart'

    Returns:
        Number of rows loaded. 0 on failure.
    """
    if df.empty:
        print(f"[SKIP] {table_name}: empty DataFrame")
        return 0

    try:
        df.to_sql(
            table_name,
            db.target_engine,
            schema=settings.TARGET_SCHEMA,
            if_exists="replace",
            index=False,
        )
        print(f"[OK] Loaded {table_name}: {len(df)} rows → schema '{settings.TARGET_SCHEMA}'")
        return len(df)
    except Exception as e:
        print(f"[FAIL] Error loading {table_name}: {e}")
        return 0


def load_all(tables: dict) -> dict:
    """Load all tables in correct order.

    Args:
        tables: Dictionary mapping table_name -> DataFrame

    Returns:
        Dictionary mapping table_name -> rows_loaded
    """
    results = {}
    for name in LOAD_ORDER:
        if name in tables:
            results[name] = load_table(tables[name], name)
        else:
            print(f"[SKIP] {name}: not in tables dict")
            results[name] = 0
    return results
