"""
ETL Pipeline — End-to-end orchestrator for OBIDSS.

Runs the complete Extract → Transform → Load pipeline
from Odoo 18 PostgreSQL to Analytics Mart (Star Schema).

This pipeline builds 6 Dimension + 4 Fact tables.
"""
import pandas as pd
from etl.extract import extract_all
from etl.transform import (
    build_dim_date, build_dim_product, build_dim_customer,
    build_dim_vendor, build_dim_company, build_dim_warehouse,
    build_fact_sales, build_fact_purchase,
    build_fact_inventory, build_fact_accounting,
)
from etl.load import load_all
from etl.logger import ETLLogger


def run_pipeline():
    """Execute the full ETL pipeline."""
    logger = ETLLogger("OBIDSS_ETL_PIPELINE")
    logger.start()

    print("=" * 60)
    print("OBIDSS ETL Pipeline — Odoo 18 → Analytics Mart")
    print("=" * 60)

    # ── STEP 1: EXTRACT ──────────────────────────────────────
    print("\n[PHASE 1] Extracting from Odoo 18...")
    raw = extract_all()

    empty = pd.DataFrame()

    # ── STEP 2: TRANSFORM — Dimensions ───────────────────────
    print("\n[PHASE 2] Building Dimensions...")
    dim_date = build_dim_date("2024-01-01", "2024-12-31")
    dim_product = build_dim_product(
        raw.get("product_product", empty),
        raw.get("product_template", empty),
        raw.get("product_category", empty),
    )
    dim_customer = build_dim_customer(raw.get("res_partner_customer", empty))
    dim_vendor = build_dim_vendor(raw.get("res_partner_vendor", empty))
    dim_company = build_dim_company(raw.get("res_company", empty))
    dim_warehouse = build_dim_warehouse(raw.get("stock_warehouse", empty))

    print(f"  dim_date: {len(dim_date)} rows")
    print(f"  dim_product: {len(dim_product)} rows")
    print(f"  dim_customer: {len(dim_customer)} rows")
    print(f"  dim_vendor: {len(dim_vendor)} rows")
    print(f"  dim_company: {len(dim_company)} rows")
    print(f"  dim_warehouse: {len(dim_warehouse)} rows")

    # ── STEP 3: TRANSFORM — Facts ────────────────────────────
    print("\n[PHASE 3] Building Facts (with derived metrics)...")
    fact_sales = build_fact_sales(
        raw.get("sale_order", empty),
        raw.get("sale_order_line", empty),
        dim_product, dim_customer, dim_date,
    )
    fact_purchase = build_fact_purchase(
        raw.get("purchase_order", empty),
        raw.get("purchase_order_line", empty),
        dim_product, dim_vendor, dim_date,
    )
    fact_inventory = build_fact_inventory(
        raw.get("stock_move", empty),
        dim_product=dim_product,
    )
    fact_accounting = build_fact_accounting(
        raw.get("account_move", empty),
        raw.get("account_move_line", empty),
    )

    print(f"  fact_sales: {len(fact_sales)} rows (revenue, cost, margin)")
    print(f"  fact_purchase: {len(fact_purchase)} rows (lead_time_days)")
    print(f"  fact_inventory: {len(fact_inventory)} rows (movement_type, value)")
    print(f"  fact_accounting: {len(fact_accounting)} rows (source_module)")

    # ── STEP 4: LOAD ─────────────────────────────────────────
    print("\n[PHASE 4] Loading to Analytics Mart (schema: mart)...")
    tables = {
        "dim_date": dim_date,
        "dim_product": dim_product,
        "dim_customer": dim_customer,
        "dim_vendor": dim_vendor,
        "dim_company": dim_company,
        "dim_warehouse": dim_warehouse,
        "fact_sales": fact_sales,
        "fact_purchase": fact_purchase,
        "fact_inventory": fact_inventory,
        "fact_accounting": fact_accounting,
    }
    results = load_all(tables)

    # ── STEP 5: LOG ──────────────────────────────────────────
    for table_name, rows in results.items():
        logger.log_metric(table_name, loaded=rows)

    logger.end()

    print("\n" + "=" * 60)
    print("ETL Pipeline COMPLETED.")
    total = sum(results.values())
    print(f"Total rows loaded: {total}")
    print("=" * 60)

    return results


if __name__ == "__main__":
    run_pipeline()
