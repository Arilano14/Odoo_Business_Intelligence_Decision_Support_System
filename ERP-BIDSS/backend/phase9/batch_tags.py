"""
Phase 9 Batch Tags and Deterministic Reference Helper Module.

Provides reference generators and XML-RPC search utilities to enforce idempotency.
"""

from phase9.config import REF_PATTERNS

def get_so_ref(seq: int) -> str:
    """Generate SO reference e.g. PORTFOLIO_2026_V1-SO-0001"""
    return REF_PATTERNS['sale.order'].format(seq)

def get_po_ref(seq: int) -> str:
    """Generate PO reference e.g. PORTFOLIO_2026_V1-PO-0001"""
    return REF_PATTERNS['purchase.order'].format(seq)

def get_inv_ref(seq: int) -> str:
    """Generate Customer Invoice reference e.g. PORTFOLIO_2026_V1-INV-0001"""
    return REF_PATTERNS['account.move.invoice'].format(seq)

def get_bill_ref(seq: int) -> str:
    """Generate Vendor Bill reference e.g. PORTFOLIO_2026_V1-BILL-0001"""
    return REF_PATTERNS['account.move.bill'].format(seq)

def get_int_ref(seq: int) -> str:
    """Generate Internal Transfer reference e.g. PORTFOLIO_2026_V1-INT-01"""
    return REF_PATTERNS['stock.picking.internal'].format(seq)

def get_scrap_ref(seq: int) -> str:
    """Generate Scrap reference e.g. PORTFOLIO_2026_V1-SCRAP-01"""
    return REF_PATTERNS['stock.scrap'].format(seq)

def record_exists(models, db, uid, password, model_name, field_name, ref_value):
    """
    Checks if a record with the given reference already exists in Odoo.
    Returns record ID if found, else None.
    """
    res = models.execute_kw(db, uid, password, model_name, 'search_read',
        [[ (field_name, '=', ref_value) ]], {'fields': ['id'], 'limit': 1})
    if res:
        return res[0]['id']
    return None
