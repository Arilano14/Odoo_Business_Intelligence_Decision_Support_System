"""
Fixes sale_order.date_order in Odoo clone database based on client_order_ref (SYNTH_V2_YYYY_MM_xxxx).
Odoo's action_confirm() automatically sets date_order to current timestamp, so this script restores
the intended historical order date.
"""

import sys
sys.path.append('backend')
import pandas as pd
from config.database import db
from sqlalchemy import text

def fix_dates():
    print("Fixing sale_order.date_order in Odoo database based on client_order_ref...")
    update_sql = """
        UPDATE sale_order
        SET date_order = TO_TIMESTAMP(
            SUBSTRING(client_order_ref FROM 10 FOR 4) || '-' || 
            SUBSTRING(client_order_ref FROM 15 FOR 2) || '-15 10:00:00',
            'YYYY-MM-DD HH24:MI:SS'
        )
        WHERE client_order_ref LIKE 'SYNTH_V2_%';
    """
    with db.source_engine.connect() as conn:
        res = conn.execute(text(update_sql))
        conn.commit()
        print(f"[OK] Updated date_order for {res.rowcount} Sales Orders.")

if __name__ == "__main__":
    fix_dates()
