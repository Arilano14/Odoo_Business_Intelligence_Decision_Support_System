import pandas as pd
from config.database import db

def extract_table(table_name):
    query = f"SELECT * FROM {table_name}"
    try:
        # For simulation without live DB, we can use Faker data if connection fails
        df = pd.read_sql(query, db.source_engine)
        return df
    except Exception as e:
        print(f"Error extracting {table_name}: {str(e)}")
        # Return empty dataframe as fallback for MVP template
        return pd.DataFrame()
