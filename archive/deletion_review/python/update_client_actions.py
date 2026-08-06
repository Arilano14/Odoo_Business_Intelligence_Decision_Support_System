import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import db
from sqlalchemy import text

with db.source_engine.connect() as conn:
    acts = conn.execute(text("SELECT id, name, tag FROM ir_act_client WHERE tag = 'spreadsheet_dashboard' OR tag LIKE '%spreadsheet%'")).fetchall()
    print("Spreadsheet Client Actions:", acts)

    top_id = conn.execute(text("SELECT id FROM ir_ui_menu WHERE name->>'en_US' = 'OBIDSS'")).scalar()

    if acts:
        act_str = f"ir.actions.client,{acts[0][0]}"
        conn.execute(text(f"UPDATE ir_ui_menu SET action = '{act_str}' WHERE parent_id = {top_id} AND name->>'en_US' IN ('Executive Operations', 'Data Quality & Reconciliation', 'Configuration')"))
        conn.commit()
        print(f"Updated action for Executive Operations to: {act_str}")
