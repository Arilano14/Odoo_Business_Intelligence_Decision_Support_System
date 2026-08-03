import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from odoo.connection import get_connection
from config.database import db
from sqlalchemy import text

print("--- Odoo Connection ---")
uid, models, odoo_db, password = get_connection()
print("Odoo XML-RPC Auth OK, UID:", uid)

with db.source_engine.connect() as conn:
    print("\n--- Odoo Source DB Preflight ---")
    print("Companies:", conn.execute(text("SELECT id, name FROM res_company")).fetchall())
    print("Products:", conn.execute(text("SELECT COUNT(*) FROM product_product WHERE active=true")).fetchone()[0])
    print("Customers (portfolio):", conn.execute(text("SELECT COUNT(*) FROM res_partner WHERE ref LIKE 'PORTFOLIO_2026_V1-CUST-%'")).fetchone()[0])
    print("Vendors (portfolio):", conn.execute(text("SELECT COUNT(*) FROM res_partner WHERE ref LIKE 'PORTFOLIO_2026_V1-VEND-%'")).fetchone()[0])
    print("Sales Orders:", conn.execute(text("SELECT state, COUNT(*) FROM sale_order GROUP BY state")).fetchall())
    print("Purchase Orders:", conn.execute(text("SELECT state, COUNT(*) FROM purchase_order GROUP BY state")).fetchall())
    print("Stock Moves:", conn.execute(text("SELECT state, COUNT(*) FROM stock_move GROUP BY state")).fetchall())
    print("Account Moves:", conn.execute(text("SELECT state, move_type, COUNT(*) FROM account_move GROUP BY state, move_type")).fetchall())
    
    # Dates check
    so_dates = conn.execute(text("SELECT MIN(date_order), MAX(date_order) FROM sale_order")).fetchone()
    print("SO Date Range:", so_dates)
    po_dates = conn.execute(text("SELECT MIN(date_order), MAX(date_order) FROM purchase_order")).fetchone()
    print("PO Date Range:", po_dates)

with db.target_engine.connect() as conn:
    print("\n--- Target Mart Schema Preflight ---")
    tables = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='mart'")).fetchall()
    tables_list = [t[0] for t in tables]
    print("Current mart tables:", tables_list)
    for t in sorted(tables_list):
        cnt = conn.execute(text(f"SELECT COUNT(*) FROM mart.{t}")).fetchone()[0]
        dates_str = ""
        if "date_id" in [c[0] for c in conn.execute(text(f"SELECT column_name FROM information_schema.columns WHERE table_schema='mart' AND table_name='{t}'")).fetchall()]:
            min_max = conn.execute(text(f"SELECT MIN(date_id), MAX(date_id) FROM mart.{t}")).fetchone()
            dates_str = f" | Date Range: {min_max[0]} to {min_max[1]}"
        print(f"  mart.{t}: {cnt} rows{dates_str}")
