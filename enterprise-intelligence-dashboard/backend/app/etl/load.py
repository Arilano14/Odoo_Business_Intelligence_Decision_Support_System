import pandas as pd
from app.database.connection import engine

def load_data(transformed_data: dict):
    """Loads transformed data into the analytics database."""
    print("Loading data into Analytics Database...")
    
    from sqlalchemy import text
    try:
        with engine.connect() as conn:
            # Truncate dimension tables, cascading to fact tables
            conn.execute(text("TRUNCATE TABLE dim_date, dim_customer, dim_product CASCADE;"))
            conn.commit()
    except Exception as e:
        print(f"Truncate info: {e}")

    for table_name, df in transformed_data.items():
        if df.empty:
            continue
            
        try:
            # Using append to respect existing foreign key constraints
            df.to_sql(table_name, engine, if_exists='append', index=False)
            print(f"Successfully loaded {len(df)} rows into {table_name}.")
        except Exception as e:
            print(f"Error loading {table_name}: {e}")
            
    print("Loading complete.")
