import sys
sys.path.append('backend')
import pandas as pd
from config.database import db
from sqlalchemy import text

with db.source_engine.connect() as conn:
    df = pd.read_sql(text("SELECT COUNT(id) AS cnt FROM sale_order WHERE client_order_ref LIKE 'SYNTH_V2_%'"), conn)
    print(f"Current Scenario V2 Sales Orders in Odoo: {df['cnt'].iloc[0]}")
