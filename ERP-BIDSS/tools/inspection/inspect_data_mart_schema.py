import sys
sys.path.append('backend')
import pandas as pd
from config.database import db
from sqlalchemy import text

with db.source_engine.connect() as conn:
    df = pd.read_sql(text("SELECT date_order, client_order_ref FROM sale_order WHERE client_order_ref LIKE 'SYNTH_V2_%' LIMIT 10"), conn)
    print(df)
