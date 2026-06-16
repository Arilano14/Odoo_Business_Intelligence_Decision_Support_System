import pandas as pd
from app.database.connection import engine

def load_data(transformed_data: dict):
    """Loads transformed data into the analytics database."""
    print("Loading data into Analytics Database...")
    
    for table_name, df in transformed_data.items():
        if df.empty:
            continue
            
        try:
            # Using SQLAlchemy engine to load data
            # if_exists='append' will add to existing tables
            # In a real ETL, you'd likely want an upsert or truncate/load strategy
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            print(f"Successfully loaded {len(df)} rows into {table_name}.")
        except Exception as e:
            print(f"Error loading {table_name}: {e}")
            
    print("Loading complete.")
