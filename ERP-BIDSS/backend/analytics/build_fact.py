"""
Analytics Mart — Fact Table Builder.

Builds all 4 fact tables from Odoo 18 source data,
applying business rules, derived metrics, and surrogate key mapping.
Loads results into PostgreSQL schema 'mart'.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np
from config.database import db
from config.settings import settings


def _load_sk_map(table, sk_col, nk_col):
    """Load surrogate key mapping from a dimension table."""
    try:
        df = pd.read_sql(
            f"SELECT {sk_col}, {nk_col} FROM {settings.TARGET_SCHEMA}.{table}",
            db.target_engine
        )
        return df.set_index(nk_col)[sk_col].to_dict()
    except Exception:
        return {}


def build_fact_sales(source_engine, dim_data):
    """Build fact_sales from sale_order + sale_order_line.

    Derived metrics:
    - revenue = qty × price_unit × (1 - discount/100)
    - cost = qty × standard_price (from dim_product)
    - margin = revenue - cost
    """
    query = """
        SELECT
            sol.id              AS line_id,
            so.date_order       AS date_order,
            sol.product_id      AS odoo_product_id,
            so.partner_id       AS odoo_partner_id,
            so.company_id       AS odoo_company_id,
            sol.product_uom_qty AS quantity,
            sol.price_unit      AS price_unit,
            COALESCE(sol.discount, 0) AS discount,
            sol.price_subtotal  AS subtotal
        FROM sale_order_line sol
        JOIN sale_order so ON sol.order_id = so.id
        WHERE so.state = 'sale'
        ORDER BY so.date_order
    """
    try:
        fact = pd.read_sql(query, source_engine)
    except Exception as e:
        print(f"  [FAIL] fact_sales extract: {e}")
        return pd.DataFrame()

    if fact.empty:
        return pd.DataFrame()

    # Surrogate key mappings
    product_map = _load_sk_map("dim_product", "sk_product_id", "odoo_product_id")
    customer_map = _load_sk_map("dim_customer", "sk_customer_id", "odoo_partner_id")
    company_map = _load_sk_map("dim_company", "sk_company_id", "odoo_company_id")

    # Build standard_price lookup for cost calculation
    price_lookup = {}
    if "dim_product" in dim_data and not dim_data["dim_product"].empty:
        dp = dim_data["dim_product"]
        price_lookup = dp.set_index("odoo_product_id")["standard_price"].to_dict()

    # Transform
    fact["date_id"] = pd.to_datetime(fact["date_order"]).dt.strftime("%Y%m%d").astype(int)
    fact["product_id"] = fact["odoo_product_id"].map(product_map).fillna(0).astype(int)
    fact["customer_id"] = fact["odoo_partner_id"].map(customer_map).fillna(0).astype(int)
    fact["company_id"] = fact["odoo_company_id"].map(company_map).fillna(1).astype(int)

    # Derived measures
    fact["revenue"] = (
        fact["quantity"] * fact["price_unit"] * (1 - fact["discount"] / 100)
    ).round(2)
    fact["cost"] = (
        fact["quantity"] * fact["odoo_product_id"].map(price_lookup).fillna(0)
    ).round(2)
    fact["margin"] = (fact["revenue"] - fact["cost"]).round(2)

    result = fact[[
        "date_id", "product_id", "customer_id", "company_id",
        "quantity", "price_unit", "discount", "subtotal", "revenue", "cost", "margin"
    ]].copy()
    result.insert(0, "sk_sales_id", range(1, len(result) + 1))

    print(f"  [OK] fact_sales: {len(result)} rows (revenue, cost, margin calculated)")
    return result


def build_fact_purchase(source_engine, dim_data):
    """Build fact_purchase from purchase_order + purchase_order_line.

    Derived metrics:
    - lead_time_days = date_planned - date_order (in days)
    """
    query = """
        SELECT
            pol.id              AS line_id,
            po.date_order       AS date_order,
            po.date_planned     AS date_planned,
            pol.product_id      AS odoo_product_id,
            po.partner_id       AS odoo_partner_id,
            po.company_id       AS odoo_company_id,
            pol.product_qty     AS quantity,
            pol.price_unit      AS price_unit,
            pol.price_subtotal  AS subtotal
        FROM purchase_order_line pol
        JOIN purchase_order po ON pol.order_id = po.id
        WHERE po.state = 'purchase'
        ORDER BY po.date_order
    """
    try:
        fact = pd.read_sql(query, source_engine)
    except Exception as e:
        print(f"  [FAIL] fact_purchase extract: {e}")
        return pd.DataFrame()

    if fact.empty:
        return pd.DataFrame()

    product_map = _load_sk_map("dim_product", "sk_product_id", "odoo_product_id")
    vendor_map = _load_sk_map("dim_vendor", "sk_vendor_id", "odoo_partner_id")
    company_map = _load_sk_map("dim_company", "sk_company_id", "odoo_company_id")

    fact["date_id"] = pd.to_datetime(fact["date_order"]).dt.strftime("%Y%m%d").astype(int)
    fact["product_id"] = fact["odoo_product_id"].map(product_map).fillna(0).astype(int)
    fact["vendor_id"] = fact["odoo_partner_id"].map(vendor_map).fillna(0).astype(int)
    fact["company_id"] = fact["odoo_company_id"].map(company_map).fillna(1).astype(int)

    # Derived: lead_time_days
    fact["lead_time_days"] = (
        pd.to_datetime(fact["date_planned"]) - pd.to_datetime(fact["date_order"])
    ).dt.days.fillna(0).astype(int)

    result = fact[[
        "date_id", "product_id", "vendor_id", "company_id",
        "quantity", "price_unit", "subtotal", "lead_time_days"
    ]].copy()
    result.insert(0, "sk_purchase_id", range(1, len(result) + 1))

    print(f"  [OK] fact_purchase: {len(result)} rows (lead_time_days calculated)")
    return result


def build_fact_inventory(source_engine, dim_data):
    """Build fact_inventory from stock_move (state='done').

    Derived metrics:
    - movement_type = 'incoming' or 'outgoing' based on location logic
    - value = quantity × standard_price
    """
    query = """
        SELECT
            sm.id                AS move_id,
            sm.date              AS move_date,
            sm.product_id        AS odoo_product_id,
            sm.product_uom_qty   AS quantity,
            sm.location_id       AS location_id,
            sm.location_dest_id  AS location_dest_id,
            sm.reference         AS reference
        FROM stock_move sm
        WHERE sm.state IN ('done', 'assigned')
        ORDER BY sm.date
    """
    try:
        fact = pd.read_sql(query, source_engine)
    except Exception as e:
        print(f"  [FAIL] fact_inventory extract: {e}")
        return pd.DataFrame()

    if fact.empty:
        return pd.DataFrame()

    product_map = _load_sk_map("dim_product", "sk_product_id", "odoo_product_id")

    # Get internal locations (Odoo: locations with usage='internal' are warehouse locations)
    try:
        internal_locs = pd.read_sql(
            "SELECT id FROM stock_location WHERE usage = 'internal'",
            source_engine
        )["id"].tolist()
    except Exception:
        internal_locs = []

    fact["date_id"] = pd.to_datetime(fact["move_date"]).dt.strftime("%Y%m%d").astype(int)
    fact["product_id"] = fact["odoo_product_id"].map(product_map).fillna(0).astype(int)

    # Derive movement_type based on Odoo location logic
    if internal_locs:
        is_dest_internal = fact["location_dest_id"].isin(internal_locs)
        is_src_internal = fact["location_id"].isin(internal_locs)
        
        # If destination is internal and source is not -> incoming
        # If source is internal and destination is not -> outgoing
        # If both are internal -> internal
        conditions = [
            (~is_src_internal) & is_dest_internal,
            is_src_internal & (~is_dest_internal),
            is_src_internal & is_dest_internal
        ]
        choices = ["incoming", "outgoing", "internal"]
        fact["movement_type"] = np.select(conditions, choices, default="other")
    else:
        # Fallback: use location_id < location_dest_id heuristic
        fact["movement_type"] = np.where(
            fact["location_dest_id"] > fact["location_id"],
            "incoming",
            "outgoing"
        )

    # Derive value (quantity × standard_price)
    price_lookup = {}
    if "dim_product" in dim_data and not dim_data["dim_product"].empty:
        dp = dim_data["dim_product"]
        price_lookup = dp.set_index("odoo_product_id")["standard_price"].to_dict()
    fact["value"] = (
        fact["quantity"] * fact["odoo_product_id"].map(price_lookup).fillna(0)
    ).round(2)

    # Warehouse mapping: derive from location (simplified for MVP)
    fact["warehouse_id"] = 1  # Default warehouse for MVP (single warehouse)

    result = fact[[
        "date_id", "product_id", "warehouse_id",
        "quantity", "value", "movement_type", "reference"
    ]].copy()
    result.insert(0, "sk_inventory_id", range(1, len(result) + 1))

    print(f"  [OK] fact_inventory: {len(result)} rows (movement_type, value calculated)")
    return result


def build_fact_accounting(source_engine, dim_data):
    """Build fact_accounting from account_move + account_move_line.

    Derived metrics:
    - source_module = derived from move_type (out_invoice→sales, in_invoice→purchase)
    """
    query = """
        SELECT
            aml.id          AS line_id,
            aml.date        AS line_date,
            am.company_id   AS odoo_company_id,
            aml.debit       AS debit,
            aml.credit      AS credit,
            aml.name        AS account_name,
            am.move_type    AS move_type
        FROM account_move_line aml
        JOIN account_move am ON aml.move_id = am.id
        WHERE am.state = 'posted'
        ORDER BY aml.date
    """
    try:
        fact = pd.read_sql(query, source_engine)
    except Exception as e:
        print(f"  [FAIL] fact_accounting extract: {e}")
        return pd.DataFrame()

    if fact.empty:
        return pd.DataFrame()

    company_map = _load_sk_map("dim_company", "sk_company_id", "odoo_company_id")

    fact["date_id"] = pd.to_datetime(fact["line_date"]).dt.strftime("%Y%m%d").astype(int)
    fact["company_id"] = fact["odoo_company_id"].map(company_map).fillna(1).astype(int)

    # Derive source_module from Odoo move_type
    module_map = {
        "out_invoice": "sales",
        "out_refund": "sales",
        "in_invoice": "purchase",
        "in_refund": "purchase",
        "entry": "manual",
    }
    fact["source_module"] = fact["move_type"].map(module_map).fillna("other")

    result = fact[[
        "date_id", "company_id",
        "debit", "credit", "account_name", "move_type", "source_module"
    ]].copy()
    result.insert(0, "sk_accounting_id", range(1, len(result) + 1))

    print(f"  [OK] fact_accounting: {len(result)} rows (source_module derived)")
    return result


def load_fact(df, table_name):
    """Load a single fact table into mart schema (full refresh)."""
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


def build_all_facts(dim_data):
    """Build and load all 4 fact tables."""
    print("\n" + "=" * 60)
    print("PHASE 5 — Building Fact Tables")
    print("=" * 60)

    source = db.source_engine
    results = {}

    facts = {
        "fact_sales": build_fact_sales(source, dim_data),
        "fact_purchase": build_fact_purchase(source, dim_data),
        "fact_inventory": build_fact_inventory(source, dim_data),
        "fact_accounting": build_fact_accounting(source, dim_data),
    }

    for name, df in facts.items():
        results[name] = load_fact(df, name)

    print("\n── Fact Summary ──")
    total = 0
    for name, count in results.items():
        print(f"  {name}: {count} rows")
        total += count
    print(f"  TOTAL: {total} rows")

    return results


if __name__ == "__main__":
    # Requires dimensions to be built first
    from build_dimension import build_all_dimensions
    _, dim_data = build_all_dimensions()
    build_all_facts(dim_data)
