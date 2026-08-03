"""
Extract module — Odoo 18 PostgreSQL Data Extraction.

Extracts data from Odoo 18 operational tables using SQL queries
that match actual Odoo 18 table and column names.
"""
import pandas as pd
from config.database import db
from config.settings import settings


# ── Odoo 18 Extraction Queries ──────────────────────────────
# Each query selects only the columns needed for the Star Schema.

QUERIES = {
    # Master Data
    "product_product": """
        SELECT pp.id, pp.product_tmpl_id, pp.default_code, pp.active,
               CAST(pp.standard_price->>'1' AS NUMERIC) as standard_price
        FROM product_product pp
        WHERE pp.active = True
    """,
    "product_template": """
        SELECT pt.id, pt.name->>'en_US' as name, pt.list_price,
               pt.categ_id, pt.type, pt.sale_ok, pt.purchase_ok
        FROM product_template pt
    """,
    "product_category": """
        SELECT pc.id, pc.name as name, pc.parent_id
        FROM product_category pc
    """,
    "res_partner_customer": f"""
        SELECT rp.id, rp.name, rp.email, rp.phone, rp.city,
               rp.customer_rank, rp.is_company, rp.ref
        FROM res_partner rp
        WHERE rp.customer_rank > 0 AND rp.active = True
          AND (rp.ref LIKE '{settings.CUSTOMER_REF_PREFIX}%%' OR rp.ref IS NOT NULL)
    """,
    "res_partner_vendor": f"""
        SELECT rp.id, rp.name, rp.email, rp.phone, rp.city,
               rp.supplier_rank, rp.is_company, rp.ref
        FROM res_partner rp
        WHERE rp.supplier_rank > 0 AND rp.active = True
          AND (rp.ref LIKE '{settings.VENDOR_REF_PREFIX}%%' OR rp.ref IS NOT NULL)
    """,
    "res_company": f"""
        SELECT rc.id, rc.name FROM res_company rc
        WHERE rc.id = {settings.TARGET_COMPANY_ID}
    """,
    "stock_warehouse": f"""
        SELECT sw.id, sw.name, sw.code, sw.company_id
        FROM stock_warehouse sw
        WHERE sw.company_id = {settings.TARGET_COMPANY_ID}
    """,

    # Transactional Data
    "sale_order": f"""
        SELECT so.id, so.name, so.partner_id, so.date_order,
               so.amount_total, so.amount_untaxed, so.state, so.company_id
        FROM sale_order so
        WHERE so.state = 'sale'
          AND so.company_id = {settings.TARGET_COMPANY_ID}
          AND so.date_order >= DATE '{settings.ANALYSIS_START_DATE}'
          AND so.date_order <= TIMESTAMP '{settings.ANALYSIS_END_DATE} 23:59:59'
    """,
    "sale_order_line": """
        SELECT sol.id, sol.order_id, sol.product_id,
               sol.product_uom_qty, sol.price_unit,
               sol.price_subtotal, sol.discount
        FROM sale_order_line sol
    """,
    "purchase_order": f"""
        SELECT po.id, po.name, po.partner_id, po.date_order,
               po.date_planned, po.amount_total, po.state, po.company_id
        FROM purchase_order po
        WHERE po.state = 'purchase'
          AND po.company_id = {settings.TARGET_COMPANY_ID}
          AND po.date_order >= DATE '{settings.ANALYSIS_START_DATE}'
          AND po.date_order <= TIMESTAMP '{settings.ANALYSIS_END_DATE} 23:59:59'
    """,
    "purchase_order_line": """
        SELECT pol.id, pol.order_id, pol.product_id,
               pol.product_qty, pol.price_unit, pol.price_subtotal,
               pol.date_planned
        FROM purchase_order_line pol
    """,
    "stock_move": f"""
        SELECT sm.id, sm.name, sm.product_id, sm.product_uom_qty,
               sm.location_id, sm.location_dest_id, sm.state,
               sm.date, sm.reference, sm.company_id
        FROM stock_move sm
        WHERE sm.company_id = {settings.TARGET_COMPANY_ID}
          AND sm.date >= DATE '{settings.ANALYSIS_START_DATE}'
          AND sm.date <= TIMESTAMP '{settings.ANALYSIS_END_DATE} 23:59:59'
    """,
    "stock_quant": """
        SELECT sq.id, sq.product_id, sq.location_id, sq.quantity
        FROM stock_quant sq
    """,
    "account_move": f"""
        SELECT am.id, am.name, am.move_type, am.partner_id,
               am.date, am.amount_total, am.state, am.journal_id, am.company_id
        FROM account_move am
        WHERE am.state = 'posted'
          AND am.company_id = {settings.TARGET_COMPANY_ID}
          AND am.date >= DATE '{settings.ANALYSIS_START_DATE}'
          AND am.date <= DATE '{settings.ANALYSIS_END_DATE}'
    """,
    "account_move_line": """
        SELECT aml.id, aml.move_id, aml.account_id,
               aml.debit, aml.credit, aml.name, aml.date
        FROM account_move_line aml
    """,
}


def extract_table(table_key: str) -> pd.DataFrame:
    """Extract a single table from Odoo 18 PostgreSQL.

    Args:
        table_key: Key from QUERIES dict (e.g. 'sale_order', 'res_partner_customer')

    Returns:
        DataFrame with extracted data. Empty DataFrame on failure.
    """
    if table_key not in QUERIES:
        print(f"[WARN] Unknown table key: {table_key}")
        return pd.DataFrame()

    query = QUERIES[table_key]
    try:
        df = pd.read_sql(query, db.source_engine)
        print(f"[OK] Extracted {table_key}: {len(df)} rows")
        return df
    except Exception as e:
        print(f"[FAIL] Error extracting {table_key}: {e}")
        return pd.DataFrame()


def extract_all() -> dict:
    """Extract all tables defined in QUERIES.

    Returns:
        Dictionary mapping table_key -> DataFrame
    """
    data = {}
    for key in QUERIES:
        data[key] = extract_table(key)
    return data
