import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import db
from sqlalchemy import text

print("============================================================")
print("GATE 2A — AUTHORITATIVE DATA SCOPE AUDIT")
print("============================================================")

with db.source_engine.connect() as conn:
    # 1. Sales Order Breakdown
    sos = conn.execute(text("""
        SELECT state, COUNT(*), SUM(amount_total)
        FROM sale_order
        WHERE company_id = 2
        GROUP BY state
    """)).fetchall()
    
    print("Sales Orders Breakdown (Company 2):")
    so_confirmed_qty, so_confirmed_val = 0, 0.0
    for s in sos:
        print(f"  State: {s[0]:10s} | Count: {s[1]:4d} | Total: Rp {float(s[2]):,.2f}")
        if s[0] == 'sale':
            so_confirmed_qty, so_confirmed_val = s[1], float(s[2])

    # 2. Purchase Order Breakdown
    pos = conn.execute(text("""
        SELECT state, COUNT(*), SUM(amount_total)
        FROM purchase_order
        WHERE company_id = 2
        GROUP BY state
    """)).fetchall()
    
    print("\nPurchase Orders Breakdown (Company 2):")
    po_confirmed_qty, po_confirmed_val = 0, 0.0
    for p in pos:
        print(f"  State: {p[0]:10s} | Count: {p[1]:4d} | Total: Rp {float(p[2]):,.2f}")
        if p[0] == 'purchase':
            po_confirmed_qty, po_confirmed_val = p[1], float(p[2])

    # 3. Product Scope Breakdown
    portfolio_prods = conn.execute(text("""
        SELECT COUNT(*) FROM product_product pp
        JOIN product_template pt ON pp.product_tmpl_id = pt.id
        WHERE pt.name->>'en_US' LIKE 'Heavy Equipment%%' OR pt.name->>'en_US' LIKE 'Consumables Item%%'
    """)).scalar()

    base_prods = conn.execute(text("""
        SELECT COUNT(*) FROM product_product pp
        JOIN product_template pt ON pp.product_tmpl_id = pt.id
        WHERE pt.name->>'en_US' NOT LIKE 'Heavy Equipment%%' AND pt.name->>'en_US' NOT LIKE 'Consumables Item%%'
    """)).scalar()

    print(f"\nProduct Scope Breakdown:")
    print(f"  Portfolio Active Variants (Heavy & Consumables): {portfolio_prods}")
    print(f"  Base Odoo Default Variants                    : {base_prods}")
    print(f"  Total Product Variants                        : {portfolio_prods + base_prods}")

    # Summary
    print("\nAuthoritative Scope Summary:")
    print(f"  Valid Portfolio Confirmed Sales Revenue: Rp {so_confirmed_val:,.2f} ({so_confirmed_qty} SOs)")
    print(f"  Valid Portfolio Confirmed Purchase Value: Rp {po_confirmed_val:,.2f} ({po_confirmed_qty} POs)")
    print(f"  Valid Portfolio Active Products          : {portfolio_prods} Variants")
