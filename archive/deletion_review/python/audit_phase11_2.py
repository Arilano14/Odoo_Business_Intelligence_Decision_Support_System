import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import db
from sqlalchemy import text

print("============================================================")
print("PHASE 11.2 READ-ONLY COMPREHENSIVE AUDIT")
print("============================================================")

with db.source_engine.connect() as conn:
    # 1. Company Scope
    company = conn.execute(text("SELECT id, name FROM res_company WHERE id = 2")).fetchall()
    print("Company ID 2:", company[0] if company else "NOT FOUND")

    # 2. Portfolio Counts Verification
    prods = conn.execute(text("SELECT COUNT(*) FROM product_product WHERE active=True")).scalar()
    custs = conn.execute(text("SELECT COUNT(*) FROM res_partner WHERE ref LIKE 'PORTFOLIO_2026_V1-CUST-%%'")).scalar()
    vends = conn.execute(text("SELECT COUNT(*) FROM res_partner WHERE ref LIKE 'PORTFOLIO_2026_V1-VEND-%%'")).scalar()
    sos = conn.execute(text("SELECT COUNT(*) FROM sale_order WHERE company_id = 2")).scalar()
    pos = conn.execute(text("SELECT COUNT(*) FROM purchase_order WHERE company_id = 2")).scalar()
    transfers = conn.execute(text("""
        SELECT COUNT(DISTINCT picking_id) FROM stock_move 
        WHERE company_id = 2 AND picking_type_id IN (
            SELECT id FROM stock_picking_type WHERE code = 'internal' AND warehouse_id IN (
                SELECT id FROM stock_warehouse WHERE company_id = 2
            )
        )
    """)).scalar()
    scraps = conn.execute(text("SELECT COUNT(*) FROM stock_scrap WHERE company_id = 2")).scalar()

    print(f"Portfolio Dataset Counts: Prods={prods}, Custs={custs}, Vends={vends}, SOs={sos}, POs={pos}, Transfers={transfers}, Scraps={scraps}")

    # 3. App Launcher Menus Audit
    menus = conn.execute(text("""
        SELECT m.id, m.name->>'en_US' as menu_name, m.sequence, m.parent_id, m.action,
               d.module as module_owner,
               (SELECT COUNT(*) FROM ir_ui_menu WHERE parent_id = m.id) as child_count
        FROM ir_ui_menu m
        LEFT JOIN ir_model_data d ON d.model = 'ir.ui.menu' AND d.res_id = m.id
        WHERE m.parent_id IS NULL
        ORDER BY m.sequence
    """)).fetchall()
    print("\nCurrent Top-Level Launcher Menus:")
    for m in menus:
        print(f"  Menu ID {m[0]:4d} | Name: {m[1]:25s} | Seq: {m[2]:3d} | Module: {str(m[5]):20s} | Children: {m[6]}")

    # 4. Spreadsheet Dashboard Records Audit
    dashboards = conn.execute(text("""
        SELECT d.id, d.name->>'en_US' as dash_name, d.dashboard_group_id, g.name->>'en_US' as group_name,
               (SELECT file_size FROM ir_attachment WHERE res_model='spreadsheet.dashboard' AND res_id=d.id LIMIT 1) as att_size
        FROM spreadsheet_dashboard d
        LEFT JOIN spreadsheet_dashboard_group g ON d.dashboard_group_id = g.id
        ORDER BY d.id
    """)).fetchall()
    print("\nCurrent Spreadsheet Dashboard Records:")
    for d in dashboards:
        print(f"  Dash ID {d[0]:2d} | Name: {d[1]:25s} | Group: {str(d[3]):20s} | Attachment Size: {d[4]} Bytes")
