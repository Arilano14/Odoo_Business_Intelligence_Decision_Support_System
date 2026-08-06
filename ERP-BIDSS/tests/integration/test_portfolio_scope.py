import sys
sys.path.append('backend')
import pandas as pd
from config.database import db

df = pd.read_sql("SELECT sk_product_id, odoo_product_id, product_name, category, default_code FROM mart.dim_product", db.target_engine)

print(f"Total Products in dim_product: {len(df)}")
demo_cats = ['Office Furniture', 'Outdoor furniture', 'Home Construction', 'Software', 'Services', 'Expenses']
portfolio_df = df[~df['category'].isin(demo_cats) & (df['default_code'].str.startswith('PORTFOLIO', na=False) | df['category'].isin(['Engine and Hydraulic Parts', 'Filters and Maintenance Parts', 'Undercarriage Parts', 'Heavy Equipment', 'Consumables']))]

print(f"Verified Portfolio Products: {len(portfolio_df)}")
print("\nSample Portfolio Products:")
print(portfolio_df.head(10))
