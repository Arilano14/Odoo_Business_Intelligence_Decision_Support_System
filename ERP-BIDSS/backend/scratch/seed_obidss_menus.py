import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import db
from sqlalchemy import text

print("============================================================")
print("SEEDING OBIDSS TOP-LEVEL MENUS & SUBMENUS INTO ODOO")
print("============================================================")

with db.source_engine.connect() as conn:
    # 1. Check or create Top Level Menu 'OBIDSS'
    top_menu = conn.execute(text("SELECT id FROM ir_ui_menu WHERE name->>'en_US' = 'OBIDSS'")).scalar()
    if not top_menu:
        res = conn.execute(text("""
            INSERT INTO ir_ui_menu (name, sequence, active, web_icon)
            VALUES ('{"en_US": "OBIDSS"}'::jsonb, 5, True, 'obidss_operational_bi,static/description/icon.png')
            RETURNING id
        """))
        top_menu = res.scalar()
        print(f"Created Top-Level Menu 'OBIDSS' with ID: {top_menu}")
    else:
        print(f"Top-Level Menu 'OBIDSS' already exists with ID: {top_menu}")

    # Register in ir_model_data
    conn.execute(text(f"""
        INSERT INTO ir_model_data (module, name, model, res_id, noupdate)
        VALUES ('obidss_operational_bi', 'menu_obidss_root', 'ir.ui.menu', {top_menu}, False)
        ON CONFLICT (module, name) DO NOTHING
    """))

    # 2. Get action IDs for Odoo standard views
    act_dash = conn.execute(text("SELECT id FROM ir_act_window WHERE res_model = 'spreadsheet.dashboard' ORDER BY id LIMIT 1")).scalar() or 1
    act_sale = conn.execute(text("SELECT id FROM ir_act_window WHERE res_model = 'sale.order' ORDER BY id LIMIT 1")).scalar() or 1
    act_purchase = conn.execute(text("SELECT id FROM ir_act_window WHERE res_model = 'purchase.order' ORDER BY id LIMIT 1")).scalar() or 1
    act_stock = conn.execute(text("SELECT id FROM ir_act_window WHERE res_model = 'stock.quant' ORDER BY id LIMIT 1")).scalar() or 1
    act_account = conn.execute(text("SELECT id FROM ir_act_window WHERE res_model = 'account.move' ORDER BY id LIMIT 1")).scalar() or 1

    submenus = [
        ("Executive Operations", 10, f"ir.actions.act_window,{act_dash}"),
        ("Sales Operations", 20, f"ir.actions.act_window,{act_sale}"),
        ("Purchase & Suppliers", 30, f"ir.actions.act_window,{act_purchase}"),
        ("Inventory Operations", 40, f"ir.actions.act_window,{act_stock}"),
        ("Finance & Invoicing", 50, f"ir.actions.act_window,{act_account}"),
        ("Data Quality & Reconciliation", 60, f"ir.actions.act_window,{act_dash}"),
        ("Configuration", 70, f"ir.actions.act_window,{act_dash}"),
    ]

    for name, seq, act_str in submenus:
        sub_id = conn.execute(text(f"SELECT id FROM ir_ui_menu WHERE parent_id = {top_menu} AND name->>'en_US' = '{name}'")).scalar()
        if not sub_id:
            res = conn.execute(text(f"""
                INSERT INTO ir_ui_menu (name, parent_id, sequence, active, action)
                VALUES ('{{"en_US": "{name}"}}'::jsonb, {top_menu}, {seq}, True, '{act_str}')
                RETURNING id
            """))
            sub_id = res.scalar()
            print(f"Created Submenu '{name}' with ID: {sub_id}")
        else:
            print(f"Submenu '{name}' exists with ID: {sub_id}")

    conn.commit()
    print("OBIDSS Menu Seeding Completed Successfully!")
