"""
Transform module — Build Star Schema from Odoo 18 raw data.

Transforms extracted Odoo tables into Fact & Dimension tables
following Kimball dimensional modeling methodology.

Derived Metrics:
- fact_sales: revenue, cost, margin
- fact_purchase: lead_time_days
- fact_inventory: movement_type, value
- fact_accounting: source_module
"""
import pandas as pd
import numpy as np


# ── Dimension Builders ──────────────────────────────────────

def build_dim_date(start="2024-01-01", end="2024-12-31") -> pd.DataFrame:
    """Generate a calendar dimension table."""
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
    return dim


def build_dim_product(df_pp, df_pt, df_pc) -> pd.DataFrame:
    """Build product dimension from product_product + template + category."""
    if df_pp.empty or df_pt.empty:
        return pd.DataFrame()

    dim = df_pp.merge(df_pt, left_on="product_tmpl_id", right_on="id",
                      suffixes=("", "_tmpl"))
    if not df_pc.empty:
        dim = dim.merge(df_pc, left_on="categ_id", right_on="id",
                        suffixes=("", "_categ"))

    result = pd.DataFrame({
        "sk_product_id": range(1, len(dim) + 1),
        "odoo_product_id": dim["id"].values,
        "product_name": dim.get("name", pd.Series(["Unknown"] * len(dim))).fillna("Unknown").values,
        "category": dim.get("name_categ", pd.Series(["Uncategorized"] * len(dim))).fillna("Uncategorized").values,
        "default_code": dim.get("default_code", pd.Series([""] * len(dim))).fillna("").values,
        "list_price": dim.get("list_price", pd.Series([0] * len(dim))).fillna(0).values,
        "standard_price": dim.get("standard_price", pd.Series([0] * len(dim))).fillna(0).values,
    })
    return result


def build_dim_customer(df_partner) -> pd.DataFrame:
    """Build customer dimension from res_partner (customer_rank > 0)."""
    if df_partner.empty:
        return pd.DataFrame()

    return pd.DataFrame({
        "sk_customer_id": range(1, len(df_partner) + 1),
        "odoo_partner_id": df_partner["id"].values,
        "customer_name": df_partner["name"].values,
        "city": df_partner.get("city", pd.Series(["Unknown"] * len(df_partner))).fillna("Unknown").values,
        "industry": "Distribution",  # Default for MVP simulation
    })


def build_dim_vendor(df_partner) -> pd.DataFrame:
    """Build vendor dimension from res_partner (supplier_rank > 0)."""
    if df_partner.empty:
        return pd.DataFrame()

    return pd.DataFrame({
        "sk_vendor_id": range(1, len(df_partner) + 1),
        "odoo_partner_id": df_partner["id"].values,
        "vendor_name": df_partner["name"].values,
        "city": df_partner.get("city", pd.Series(["Unknown"] * len(df_partner))).fillna("Unknown").values,
    })


def build_dim_company(df_company) -> pd.DataFrame:
    """Build company dimension from res_company."""
    if df_company.empty:
        return pd.DataFrame()

    return pd.DataFrame({
        "sk_company_id": range(1, len(df_company) + 1),
        "odoo_company_id": df_company["id"].values,
        "company_name": df_company["name"].values,
    })


def build_dim_warehouse(df_wh) -> pd.DataFrame:
    """Build warehouse dimension from stock_warehouse."""
    if df_wh.empty:
        return pd.DataFrame()

    return pd.DataFrame({
        "sk_warehouse_id": range(1, len(df_wh) + 1),
        "odoo_warehouse_id": df_wh["id"].values,
        "warehouse_name": df_wh["name"].values,
        "warehouse_code": df_wh["code"].values,
    })


# ── Fact Builders ───────────────────────────────────────────

def build_fact_sales(df_so, df_sol, dim_product, dim_customer, dim_date) -> pd.DataFrame:
    """Build fact_sales from sale_order + sale_order_line.

    Derived metrics:
    - revenue = qty × price_unit × (1 - discount/100)
    - cost = qty × standard_price (from dim_product)
    - margin = revenue - cost
    """
    if df_so.empty or df_sol.empty:
        return pd.DataFrame()

    fact = df_sol.merge(df_so, left_on="order_id", right_on="id",
                        suffixes=("_line", "_order"))
    fact = fact.drop_duplicates()

    # Measures
    qty = fact.get("product_uom_qty", pd.Series([0] * len(fact))).fillna(0)
    price = fact.get("price_unit_line", fact.get("price_unit", pd.Series([0] * len(fact)))).fillna(0)
    discount = fact.get("discount", pd.Series([0] * len(fact))).fillna(0)

    # DERIVED: revenue
    revenue = (qty * price * (1 - discount / 100)).round(2)

    # DERIVED: cost (from dim_product standard_price lookup)
    cost_series = pd.Series(0.0, index=fact.index)
    if not dim_product.empty and "product_id" in fact.columns:
        price_lookup = dim_product.set_index("odoo_product_id")["standard_price"].to_dict()
        cost_series = (qty * fact["product_id"].map(price_lookup).fillna(0)).round(2)

    # DERIVED: margin
    margin = (revenue - cost_series).round(2)

    # Date surrogate key
    date_id = pd.Series(0, index=fact.index)
    if "date_order" in fact.columns:
        date_id = pd.to_datetime(fact["date_order"]).dt.strftime("%Y%m%d").astype(int)

    # Map to surrogate keys
    product_sk = fact.get("product_id", pd.Series([0] * len(fact)))
    customer_sk = fact.get("partner_id", pd.Series([0] * len(fact)))
    company_sk = pd.Series(1, index=fact.index)  # Default company

    if not dim_product.empty and "product_id" in fact.columns:
        product_map = dim_product.set_index("odoo_product_id")["sk_product_id"].to_dict()
        product_sk = fact["product_id"].map(product_map).fillna(0).astype(int)

    if not dim_customer.empty and "partner_id" in fact.columns:
        customer_map = dim_customer.set_index("odoo_partner_id")["sk_customer_id"].to_dict()
        customer_sk = fact["partner_id"].map(customer_map).fillna(0).astype(int)

    result = pd.DataFrame({
        "sk_sales_id": range(1, len(fact) + 1),
        "date_id": date_id,
        "product_id": product_sk,
        "customer_id": customer_sk,
        "company_id": company_sk,
        "quantity": qty,
        "price_unit": price,
        "discount": discount,
        "subtotal": fact.get("price_subtotal_line", fact.get("price_subtotal", pd.Series([0] * len(fact)))).fillna(0),
        "revenue": revenue,
        "cost": cost_series,
        "margin": margin,
    })
    return result


def build_fact_purchase(df_po, df_pol, dim_product, dim_vendor, dim_date) -> pd.DataFrame:
    """Build fact_purchase from purchase_order + purchase_order_line.

    Derived metrics:
    - lead_time_days = date_planned - date_order (in days)
    """
    if df_po.empty or df_pol.empty:
        return pd.DataFrame()

    fact = df_pol.merge(df_po, left_on="order_id", right_on="id",
                        suffixes=("_line", "_order"))
    fact = fact.drop_duplicates()

    date_id = pd.Series(0, index=fact.index)
    if "date_order" in fact.columns:
        date_id = pd.to_datetime(fact["date_order"]).dt.strftime("%Y%m%d").astype(int)

    # DERIVED: lead_time_days
    lead_time = pd.Series(0, index=fact.index, dtype=int)
    if "date_order" in fact.columns:
        date_planned_col = "date_planned_order" if "date_planned_order" in fact.columns else "date_planned_line" if "date_planned_line" in fact.columns else None
        if date_planned_col:
            lead_time = (
                pd.to_datetime(fact[date_planned_col], utc=True)
                - pd.to_datetime(fact["date_order"], utc=True)
            ).dt.days.fillna(0).astype(int)

    # Surrogate key mapping
    product_sk = pd.Series(0, index=fact.index)
    vendor_sk = pd.Series(0, index=fact.index)

    if not dim_product.empty and "product_id" in fact.columns:
        product_map = dim_product.set_index("odoo_product_id")["sk_product_id"].to_dict()
        product_sk = fact["product_id"].map(product_map).fillna(0).astype(int)

    if not dim_vendor.empty and "partner_id" in fact.columns:
        vendor_map = dim_vendor.set_index("odoo_partner_id")["sk_vendor_id"].to_dict()
        vendor_sk = fact["partner_id"].map(vendor_map).fillna(0).astype(int)

    result = pd.DataFrame({
        "sk_purchase_id": range(1, len(fact) + 1),
        "date_id": date_id,
        "product_id": product_sk,
        "vendor_id": vendor_sk,
        "company_id": pd.Series(1, index=fact.index),
        "quantity": fact.get("product_qty", pd.Series([0] * len(fact))).fillna(0),
        "price_unit": fact.get("price_unit_line", fact.get("price_unit", pd.Series([0] * len(fact)))).fillna(0),
        "subtotal": fact.get("price_subtotal_line", fact.get("price_subtotal", pd.Series([0] * len(fact)))).fillna(0),
        "lead_time_days": lead_time,
    })
    return result


def build_fact_inventory(df_sm, dim_product=None, internal_locations=None) -> pd.DataFrame:
    """Build fact_inventory from stock_move (state='done').

    Derived metrics:
    - movement_type = 'incoming' or 'outgoing' based on location logic
    - value = quantity × standard_price (from dim_product)
    """
    if df_sm.empty:
        return pd.DataFrame()

    fact = df_sm.drop_duplicates()

    date_id = pd.Series(0, index=fact.index)
    if "date" in fact.columns:
        date_id = pd.to_datetime(fact["date"]).dt.strftime("%Y%m%d").astype(int)

    # DERIVED: movement_type
    if internal_locations and "location_dest_id" in fact.columns:
        movement_type = np.where(
            fact["location_dest_id"].isin(internal_locations),
            "incoming",
            "outgoing"
        )
    elif "location_dest_id" in fact.columns and "location_id" in fact.columns:
        movement_type = np.where(
            fact["location_dest_id"] > fact["location_id"],
            "incoming",
            "outgoing"
        )
    else:
        movement_type = "incoming"

    # DERIVED: value (qty × standard_price)
    value = pd.Series(0.0, index=fact.index)
    if dim_product is not None and not dim_product.empty and "product_id" in fact.columns:
        price_lookup = dim_product.set_index("odoo_product_id")["standard_price"].to_dict()
        value = (fact.get("product_uom_qty", 0).fillna(0) * fact["product_id"].map(price_lookup).fillna(0)).round(2)

    # Product SK mapping
    product_sk = fact.get("product_id", pd.Series([0] * len(fact)))
    if dim_product is not None and not dim_product.empty and "product_id" in fact.columns:
        product_map = dim_product.set_index("odoo_product_id")["sk_product_id"].to_dict()
        product_sk = fact["product_id"].map(product_map).fillna(0).astype(int)

    result = pd.DataFrame({
        "sk_inventory_id": range(1, len(fact) + 1),
        "date_id": date_id,
        "product_id": product_sk,
        "warehouse_id": pd.Series(1, index=fact.index),  # Default for MVP
        "quantity": fact.get("product_uom_qty", pd.Series([0] * len(fact))).fillna(0),
        "value": value,
        "movement_type": movement_type,
        "reference": fact.get("reference", pd.Series([""] * len(fact))).fillna(""),
    })
    return result


def build_fact_accounting(df_am, df_aml) -> pd.DataFrame:
    """Build fact_accounting from account_move + account_move_line.

    Derived metrics:
    - source_module = 'sales', 'purchase', or 'manual' (from move_type)
    """
    if df_am.empty or df_aml.empty:
        return pd.DataFrame()

    fact = df_aml.merge(df_am, left_on="move_id", right_on="id",
                        suffixes=("_line", "_move"))
    fact = fact.drop_duplicates()

    date_col = "date_line" if "date_line" in fact.columns else "date"
    date_id = pd.Series(0, index=fact.index)
    if date_col in fact.columns:
        date_id = pd.to_datetime(fact[date_col]).dt.strftime("%Y%m%d").astype(int)

    # DERIVED: source_module
    module_map = {
        "out_invoice": "sales",
        "out_refund": "sales",
        "in_invoice": "purchase",
        "in_refund": "purchase",
        "entry": "manual",
    }
    source_module = fact.get("move_type", pd.Series(["entry"] * len(fact))).map(module_map).fillna("other")

    result = pd.DataFrame({
        "sk_accounting_id": range(1, len(fact) + 1),
        "date_id": date_id,
        "company_id": pd.Series(1, index=fact.index),
        "debit": fact.get("debit", pd.Series([0] * len(fact))).fillna(0),
        "credit": fact.get("credit", pd.Series([0] * len(fact))).fillna(0),
        "account_name": fact.get("name_line", pd.Series([""] * len(fact))).fillna(""),
        "move_type": fact.get("move_type", pd.Series(["entry"] * len(fact))).fillna("entry"),
        "source_module": source_module,
    })
    return result
