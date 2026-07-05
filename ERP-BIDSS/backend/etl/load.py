import pandas as pd
from config.database import db

def load_table(df, table_name, schema='mart'):
    if df.empty:
        print(f"Empty dataframe for {table_name}, skipping load.")
        return 0
    try:
        df.to_sql(table_name, db.target_engine, schema=schema, if_exists='replace', index=False)
        return len(df)
    except Exception as e:
        print(f"Error loading {table_name}: {str(e)}")
        return 0
