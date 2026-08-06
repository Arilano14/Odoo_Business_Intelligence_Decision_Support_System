import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import db
from sqlalchemy import text

print("============================================================")
print("PHASE 11.2 REVISION — READ-ONLY DATA & MODEL TRUTH AUDIT")
print("============================================================")

with db.source_engine.connect() as conn:
    # ---------------------------------------------------------
    # Question A: Sales Order Classification (740 vs 720)
    # ---------------------------------------------------------
    print("\n--- QUESTION A: SALES ORDER AUDIT (company_id = 2) ---")
    so_total = conn.execute(text("SELECT COUNT(*) FROM sale_order WHERE company_id = 2")).scalar()
    so_by_state = conn.execute(text("""
        SELECT state, COUNT(*), SUM(amount_total) 
        FROM sale_order 
        WHERE company_id = 2 
        GROUP BY state
    """)).fetchall()
    print(f"Total Sales Orders in DB (Company 2): {so_total}")
    for s in so_by_state:
        print(f"  State: {s[0]:10s} | Count: {s[1]:4d} | Amount Total: Rp {float(s[2]):,.2f}")

    so_by_name = conn.execute(text("""
        SELECT 
            CASE 
                WHEN name LIKE 'SO/2026/%%' THEN 'SO/2026/XXXX (Generator Batch)'
                WHEN name LIKE 'S00%%' THEN 'S00XX (Standard Odoo Default)'
                ELSE 'Other Pattern'
            END as pattern,
            state,
            COUNT(*),
            SUM(amount_total)
        FROM sale_order
        WHERE company_id = 2
        GROUP BY 1, 2
        ORDER BY 1, 2
    """)).fetchall()
    print("Sales Orders Classification by Name Pattern:")
    for p in so_by_name:
        print(f"  Pattern: {p[0]:35s} | State: {p[1]:10s} | Count: {p[2]:4d} | Total: Rp {float(p[3]):,.2f}")

    # ---------------------------------------------------------
    # Question B: Purchase Order Classification (251 vs 240)
    # ---------------------------------------------------------
    print("\n--- QUESTION B: PURCHASE ORDER AUDIT (company_id = 2) ---")
    po_total = conn.execute(text("SELECT COUNT(*) FROM purchase_order WHERE company_id = 2")).scalar()
    po_by_state = conn.execute(text("""
        SELECT state, COUNT(*), SUM(amount_total) 
        FROM purchase_order 
        WHERE company_id = 2 
        GROUP BY state
    """)).fetchall()
    print(f"Total Purchase Orders in DB (Company 2): {po_total}")
    for s in po_by_state:
        print(f"  State: {s[0]:10s} | Count: {s[1]:4d} | Amount Total: Rp {float(s[2]):,.2f}")

    po_by_name = conn.execute(text("""
        SELECT 
            CASE 
                WHEN name LIKE 'PO/2026/%%' THEN 'PO/2026/XXXX (Generator Batch)'
                WHEN name LIKE 'P00%%' THEN 'P00XX (Standard Odoo Default)'
                ELSE 'Other Pattern'
            END as pattern,
            state,
            COUNT(*),
            SUM(amount_total)
        FROM purchase_order
        WHERE company_id = 2
        GROUP BY 1, 2
        ORDER BY 1, 2
    """)).fetchall()
    print("Purchase Orders Classification by Name Pattern:")
    for p in po_by_name:
        print(f"  Pattern: {p[0]:35s} | State: {p[1]:10s} | Count: {p[2]:4d} | Total: Rp {float(p[3]):,.2f}")

    # ---------------------------------------------------------
    # Question C: Product Templates vs Variants (240 vs 283)
    # ---------------------------------------------------------
    print("\n--- QUESTION C: PRODUCT TEMPLATES vs VARIANTS AUDIT ---")
    tmpl_active = conn.execute(text("SELECT COUNT(*) FROM product_template WHERE active=True")).scalar()
    tmpl_all = conn.execute(text("SELECT COUNT(*) FROM product_template")).scalar()
    prod_active = conn.execute(text("SELECT COUNT(*) FROM product_product WHERE active=True")).scalar()
    prod_all = conn.execute(text("SELECT COUNT(*) FROM product_product")).scalar()

    tmpl_portfolio = conn.execute(text("SELECT COUNT(*) FROM product_template WHERE name->>'en_US' LIKE 'Heavy Equipment%%' OR name->>'en_US' LIKE 'Consumables Item%%'")).scalar()
    prod_portfolio = conn.execute(text("""
        SELECT COUNT(*) FROM product_product pp 
        JOIN product_template pt ON pp.product_tmpl_id = pt.id 
        WHERE pt.name->>'en_US' LIKE 'Heavy Equipment%%' OR pt.name->>'en_US' LIKE 'Consumables Item%%'
    """)).scalar()

    print(f"Product Templates (Active / Total) : {tmpl_active} / {tmpl_all}")
    print(f"Product Variants  (Active / Total) : {prod_active} / {prod_all}")
    print(f"Portfolio Product Templates        : {tmpl_portfolio}")
    print(f"Portfolio Product Variants         : {prod_portfolio}")

    # ---------------------------------------------------------
    # Question D: Odoo 18 Spreadsheet Dashboard Object Model
    # ---------------------------------------------------------
    print("\n--- QUESTION D: SPREADSHEET DASHBOARD OBJECT MODEL ---")
    groups = conn.execute(text("SELECT id, name->>'en_US', sequence FROM spreadsheet_dashboard_group ORDER BY sequence")).fetchall()
    print("Spreadsheet Dashboard Groups in DB:")
    for g in groups:
        print(f"  Group ID: {g[0]:2d} | Name: {g[1]:20s} | Sequence: {g[2]}")

    dashboards = conn.execute(text("""
        SELECT d.id, d.name->>'en_US', d.dashboard_group_id, g.name->>'en_US' as group_name
        FROM spreadsheet_dashboard d
        JOIN spreadsheet_dashboard_group g ON d.dashboard_group_id = g.id
        ORDER BY d.id
    """)).fetchall()
    print("Spreadsheet Dashboards in DB:")
    for d in dashboards:
        print(f"  Dashboard ID: {d[0]:2d} | Name: {d[1]:20s} | Group ID: {d[2]} ({d[3]})")
