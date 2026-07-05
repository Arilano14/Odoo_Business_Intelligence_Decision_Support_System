"""
Transform module — Build Star Schema from Odoo 18 raw data.

Transforms extracted Odoo tables into Fact & Dimension tables
following Kimball dimensional modeling methodology.
"""
import pandas as pd
import numpy as np


# ── Dimension Builders ──────────────────────────────────────

def build_dim_date(start="2024-01-01", end="2024-12-31") -> pd.DataFrame:
    """Generate a calendar dimension table."""
    dates = pd.date_range(start=start, end=end, freq="D")
    dim = pd.DataFrame({
        "date_id": dates.strftime("%Y%m%d").astype(int),
        "full_date": dates,
        "year": dates.year,
        "month": dates.month,
        "day": dates.day,
        "month_name": dates.strftime("%B"),
        "quarter": dates.quarter,
        "day_of_week": dates.strftime("%A"),
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
        "odoo_product_id": dim["id"],
        "product_name": dim.get("name", "Unknown"),
        "category": dim.get("name_categ", "Uncategorized"),
        "default_code": dim.get("default_code", ""),
        "list_price": dim.get("list_price", 0),
        "standard_price": dim.get("standard_price", 0),
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
        "city": df_partner.get("city", pd.Series([""] * len(df_partner))).values,
    })


def build_dim_vendor(df_partner) -> pd.DataFrame:
    """Build vendor dimension from res_partner (supplier_rank > 0)."""
    if df_partner.empty:
        return pd.DataFrame()

    return pd.DataFrame({
        "sk_vendor_id": range(1, len(df_partner) + 1),
        "odoo_partner_id": df_partner["id"].values,
        "vendor_name": df_partner["name"].values,
        "city": df_partner.get("city", pd.Series([""] * len(df_partner))).values,
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
    """Build fact_sales from sale_order + sale_order_line."""
    if df_so.empty or df_sol.empty:
        return pd.DataFrame()

    # Join order line with order header
    fact = df_sol.merge(df_so, left_on="order_id", right_on="id",
                        suffixes=("_line", "_order"))

    # Clean
    fact = fact.drop_duplicates()

    # Calculate revenue
    qty = fact.get("product_uom_qty", 0)
    price = fact.get("price_unit_line", fact.get("price_unit", 0))
    discount = fact.get("discount", 0)
    fact["revenue"] = qty * price * (1 - discount / 100)

    # Generate date_id
    if "date_order" in fact.columns:
        fact["date_id"] = pd.to_datetime(fact["date_order"]).dt.strftime("%Y%m%d").astype(int)

    # Map to surrogate keys via lookup
    if not dim_product.empty and "product_id" in fact.columns:
        product_map = dim_product.set_index("odoo_product_id")["sk_product_id"].to_dict()
        fact["product_id_sk"] = fact["product_id"].map(product_map)

    if not dim_customer.empty and "partner_id" in fact.columns:
        customer_map = dim_customer.set_index("odoo_partner_id")["sk_customer_id"].to_dict()
        fact["customer_id_sk"] = fact["partner_id"].map(customer_map)

    result = pd.DataFrame({
        "sk_sales_id": range(1, len(fact) + 1),
        "date_id": fact.get("date_id", 0),
        "product_id": fact.get("product_id_sk", fact.get("product_id", 0)),
        "customer_id": fact.get("customer_id_sk", fact.get("partner_id", 0)),
        "quantity": qty,
        "price_unit": price,
        "discount": discount,
        "subtotal": fact.get("price_subtotal_line", fact.get("price_subtotal", 0)),
        "revenue": fact["revenue"],
    })
    return result


def build_fact_purchase(df_po, df_pol, dim_product, dim_vendor, dim_date) -> pd.DataFrame:
    """Build fact_purchase from purchase_order + purchase_order_line."""
    if df_po.empty or df_pol.empty:
        return pd.DataFrame()

    fact = df_pol.merge(df_po, left_on="order_id", right_on="id",
                        suffixes=("_line", "_order"))
    fact = fact.drop_duplicates()

    if "date_order" in fact.columns:
        fact["date_id"] = pd.to_datetime(fact["date_order"]).dt.strftime("%Y%m%d").astype(int)

    if not dim_product.empty and "product_id" in fact.columns:
        product_map = dim_product.set_index("odoo_product_id")["sk_product_id"].to_dict()
        fact["product_id_sk"] = fact["product_id"].map(product_map)

    if not dim_vendor.empty and "partner_id" in fact.columns:
        vendor_map = dim_vendor.set_index("odoo_partner_id")["sk_vendor_id"].to_dict()
        fact["vendor_id_sk"] = fact["partner_id"].map(vendor_map)

    result = pd.DataFrame({
        "sk_purchase_id": range(1, len(fact) + 1),
        "date_id": fact.get("date_id", 0),
        "product_id": fact.get("product_id_sk", fact.get("product_id", 0)),
        "vendor_id": fact.get("vendor_id_sk", fact.get("partner_id", 0)),
        "quantity": fact.get("product_qty", 0),
        "price_unit": fact.get("price_unit_line", fact.get("price_unit", 0)),
        "subtotal": fact.get("price_subtotal_line", fact.get("price_subtotal", 0)),
    })
    return result


def build_fact_inventory(df_sm) -> pd.DataFrame:
    """Build fact_inventory from stock_move (state='done')."""
    if df_sm.empty:
        return pd.DataFrame()

    fact = df_sm.drop_duplicates()

    if "date" in fact.columns:
        fact["date_id"] = pd.to_datetime(fact["date"]).dt.strftime("%Y%m%d").astype(int)

    result = pd.DataFrame({
        "sk_inventory_id": range(1, len(fact) + 1),
        "date_id": fact.get("date_id", 0),
        "product_id": fact.get("product_id", 0),
        "quantity": fact.get("product_uom_qty", 0),
        "reference": fact.get("reference", ""),
    })
    return result


def build_fact_accounting(df_am, df_aml) -> pd.DataFrame:
    """Build fact_accounting from account_move + account_move_line."""
    if df_am.empty or df_aml.empty:
        return pd.DataFrame()

    fact = df_aml.merge(df_am, left_on="move_id", right_on="id",
                        suffixes=("_line", "_move"))
    fact = fact.drop_duplicates()

    if "date_line" in fact.columns:
        fact["date_id"] = pd.to_datetime(fact["date_line"]).dt.strftime("%Y%m%d").astype(int)
    elif "date" in fact.columns:
        fact["date_id"] = pd.to_datetime(fact["date"]).dt.strftime("%Y%m%d").astype(int)

    result = pd.DataFrame({
        "sk_accounting_id": range(1, len(fact) + 1),
        "date_id": fact.get("date_id", 0),
        "debit": fact.get("debit", 0),
        "credit": fact.get("credit", 0),
        "account_name": fact.get("name_line", ""),
        "move_type": fact.get("move_type", ""),
    })
    return result
