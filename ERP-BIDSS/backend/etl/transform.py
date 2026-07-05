import pandas as pd

def clean_data(df):
    df = df.drop_duplicates()
    return df

def validate_business_rules(df, rule_type):
    if rule_type == 'sales' and 'state' in df.columns:
        return df[df['state'] == 'sale']
    if rule_type == 'inventory' and 'quantity' in df.columns:
        return df[df['quantity'] > 0]
    return df

def transform_sales(df_order, df_line):
    if df_order.empty or df_line.empty: return pd.DataFrame()
    fact_sales = pd.merge(df_line, df_order, left_on='order_id', right_on='id', suffixes=('_line', '_order'))
    fact_sales = clean_data(fact_sales)
    fact_sales = validate_business_rules(fact_sales, 'sales')
    fact_sales['revenue'] = fact_sales.get('price_unit', 0) * fact_sales.get('product_uom_qty', 0)
    return fact_sales
