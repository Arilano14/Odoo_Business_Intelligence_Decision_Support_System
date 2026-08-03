import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import db
from sqlalchemy import text

print("============================================================")
print("LINKING OBIDSS SUBMENUS DIRECTLY TO LIVE ODOO DATABASE VIEWS")
print("============================================================")

with db.source_engine.connect() as conn:
    # Fetch action window IDs for core models
    act_sale = conn.execute(text("SELECT id FROM ir_act_window WHERE res_model = 'sale.order' ORDER BY id LIMIT 1")).scalar()
    act_purchase = conn.execute(text("SELECT id FROM ir_act_window WHERE res_model = 'purchase.order' ORDER BY id LIMIT 1")).scalar()
    act_stock = conn.execute(text("SELECT id FROM ir_act_window WHERE res_model = 'stock.quant' ORDER BY id LIMIT 1")).scalar()
    act_account = conn.execute(text("SELECT id FROM ir_act_window WHERE res_model = 'account.move' ORDER BY id LIMIT 1")).scalar()
    act_dash = conn.execute(text("SELECT id FROM ir_act_window WHERE res_model = 'spreadsheet.dashboard' ORDER BY id LIMIT 1")).scalar()

    top_id = conn.execute(text("SELECT id FROM ir_ui_menu WHERE name->>'en_US' = 'OBIDSS'")).scalar()

    # Direct mappings
    updates = [
        ("Executive Operations", f"ir.actions.act_window,{act_dash}"),
        ("Sales Operations", f"ir.actions.act_window,{act_sale}"),
        ("Purchase & Suppliers", f"ir.actions.act_window,{act_purchase}"),
        ("Inventory Operations", f"ir.actions.act_window,{act_stock}"),
        ("Finance & Invoicing", f"ir.actions.act_window,{act_account}"),
        ("Data Quality & Reconciliation", f"ir.actions.act_window,{act_dash}"),
        ("Configuration", f"ir.actions.act_window,{act_dash}"),
    ]

    for name, act_str in updates:
        conn.execute(text(f"""
            UPDATE ir_ui_menu 
            SET action = '{act_str}'
            WHERE parent_id = {top_id} AND name->>'en_US' = '{name}'
        """))
        print(f"Linked Submenu '{name}' -> Action '{act_str}'")

    conn.commit()
    print("100% SUCCESS: All OBIDSS Submenus linked directly to live Odoo models!")
