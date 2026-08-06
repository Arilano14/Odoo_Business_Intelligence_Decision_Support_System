import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import db
from sqlalchemy import text

print("============================================================")
print("DEEP ODOO DATASET & CLEANLINESS AUDIT REPORT")
print("============================================================")

with db.source_engine.connect() as conn:
    # 1. Company Audit
    company = conn.execute(text("SELECT id, name FROM res_company WHERE id = 2")).fetchall()
    print("\n--- 1. ACTIVE COMPANY ---")
    print(f"Company ID 2: {company[0] if company else 'NOT FOUND'}")

    # 2. Master Data Connectivity Audit
    print("\n--- 2. MASTER DATA CONNECTIVITY (Company ID 2) ---")
    prods = conn.execute(text("SELECT COUNT(*) FROM product_template WHERE active=True")).scalar()
    prod_variants = conn.execute(text("SELECT COUNT(*) FROM product_product WHERE active=True")).scalar()
    custs = conn.execute(text("SELECT COUNT(*) FROM res_partner WHERE ref LIKE 'PORTFOLIO_2026_V1-CUST-%%'")).scalar()
    vends = conn.execute(text("SELECT COUNT(*) FROM res_partner WHERE ref LIKE 'PORTFOLIO_2026_V1-VEND-%%'")).scalar()
    
    print(f"Active Product Templates : {prods} (Target: 240)")
    print(f"Active Product Variants  : {prod_variants} (Target: 283)")
    print(f"Portfolio Customers      : {custs} (Target: 48)")
    print(f"Portfolio Vendors        : {vends} (Target: 24)")

    # 3. Operational Transactions Audit
    print("\n--- 3. OPERATIONAL TRANSACTIONS AUDIT (FY 2026) ---")
    sos = conn.execute(text("SELECT COUNT(*) FROM sale_order WHERE company_id = 2")).scalar()
    so_lines = conn.execute(text("SELECT COUNT(*) FROM sale_order_line WHERE company_id = 2")).scalar()
    so_revenue = conn.execute(text("SELECT SUM(amount_total) FROM sale_order WHERE company_id = 2 AND state='sale'")).scalar()
    
    pos = conn.execute(text("SELECT COUNT(*) FROM purchase_order WHERE company_id = 2")).scalar()
    po_lines = conn.execute(text("SELECT COUNT(*) FROM purchase_order_line WHERE company_id = 2")).scalar()
    po_value = conn.execute(text("SELECT SUM(amount_total) FROM purchase_order WHERE company_id = 2 AND state='purchase'")).scalar()

    stock_moves = conn.execute(text("SELECT COUNT(*) FROM stock_move WHERE company_id = 2 AND state='done'")).scalar()
    internal_transfers = conn.execute(text("""
        SELECT COUNT(DISTINCT picking_id) FROM stock_move 
        WHERE company_id = 2 AND picking_type_id IN (
            SELECT id FROM stock_picking_type WHERE code = 'internal' AND warehouse_id IN (
                SELECT id FROM stock_warehouse WHERE company_id = 2
            )
        )
    """)).scalar()
    scraps = conn.execute(text("SELECT COUNT(*) FROM stock_scrap WHERE company_id = 2")).scalar()

    print(f"Sales Orders (SO)       : {sos} (Target: 720, Subtotal: Rp {so_revenue:,.2f})")
    print(f"Sales Order Lines       : {so_lines} lines")
    print(f"Purchase Orders (PO)    : {pos} (Target: 240, Subtotal: Rp {po_value:,.2f})")
    print(f"Purchase Order Lines    : {po_lines} lines")
    print(f"Completed Stock Moves   : {stock_moves} moves")
    print(f"Internal Transfers      : {internal_transfers} transfers (Target: 24)")
    print(f"Scrap Operations        : {scraps} scraps (Target: 12)")

    # 4. Cleanliness & Legacy Data Audit
    print("\n--- 4. SYSTEM CLEANLINESS & LEGACY AUDIT ---")
    legacy_sos = conn.execute(text("SELECT COUNT(*) FROM sale_order WHERE company_id = 2 AND date_order < '2026-01-01'")).scalar()
    legacy_pos = conn.execute(text("SELECT COUNT(*) FROM purchase_order WHERE company_id = 2 AND date_approve < '2026-01-01'")).scalar()
    other_company_sos = conn.execute(text("SELECT COUNT(*) FROM sale_order WHERE company_id != 2")).scalar()
    other_company_pos = conn.execute(text("SELECT COUNT(*) FROM purchase_order WHERE company_id != 2")).scalar()
    
    print(f"Legacy 2024/2025 Sales Orders    : {legacy_sos} (Expected: 0)")
    print(f"Legacy 2024/2025 Purchase Orders : {legacy_pos} (Expected: 0)")
    print(f"Other Company Sales Orders      : {other_company_sos} (Expected: 0)")
    print(f"Other Company Purchase Orders   : {other_company_pos} (Expected: 0)")

    # 5. OBIDSS Custom App Audit
    print("\n--- 5. OBIDSS CUSTOM APPLICATION MENU & MODULE ---")
    custom_mod = conn.execute(text("SELECT name, state FROM ir_module_module WHERE name = 'obidss_operational_bi'")).fetchall()
    obidss_menus = conn.execute(text("SELECT id, name FROM ir_ui_menu WHERE name->>'en_US' = 'OBIDSS'")).fetchall()
    print(f"OBIDSS Addon State in DB : {custom_mod[0] if custom_mod else 'NOT INSTALLED'}")
    print(f"OBIDSS Root Menu in DB  : {obidss_menus[0] if obidss_menus else 'NOT FOUND'}")
