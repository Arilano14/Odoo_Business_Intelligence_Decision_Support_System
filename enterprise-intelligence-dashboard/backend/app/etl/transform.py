import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Basic cleaning for any dataframe."""
    if df.empty:
        return df
    # Drop rows where all columns are NA
    df = df.dropna(how='all')
    return df

def transform_date_dimension(dates_series: pd.Series) -> pd.DataFrame:
    """Generate Date Dimension from a series of dates."""
    dates_series = pd.to_datetime(dates_series).dt.date.dropna().unique()
    dim_date = pd.DataFrame({'date_id': dates_series})
    dim_date['year'] = pd.to_datetime(dim_date['date_id']).dt.year
    dim_date['month'] = pd.to_datetime(dim_date['date_id']).dt.month
    dim_date['quarter'] = pd.to_datetime(dim_date['date_id']).dt.quarter
    return dim_date

def transform_customer_dimension(partners_df: pd.DataFrame) -> pd.DataFrame:
    """Transform Odoo partners into Customer Dimension."""
    if partners_df.empty:
        return pd.DataFrame(columns=['customer_id', 'customer_name', 'segment', 'region'])
    
    df = partners_df.copy()
    df.rename(columns={'id': 'customer_id', 'name': 'customer_name'}, inplace=True)
    df['segment'] = 'General'  # Placeholder for segmentation logic
    df['region'] = 'Global'    # Placeholder for region logic
    return df[['customer_id', 'customer_name', 'segment', 'region']]

def transform_product_dimension(products_df: pd.DataFrame, templates_df: pd.DataFrame) -> pd.DataFrame:
    """Transform Odoo products into Product Dimension."""
    if products_df.empty or templates_df.empty:
        return pd.DataFrame(columns=['product_id', 'product_name', 'category'])
    
    df = pd.merge(products_df, templates_df, left_on='product_tmpl_id', right_on='id', how='left')
    df.rename(columns={'id_x': 'product_id', 'name': 'product_name'}, inplace=True)
    df['category'] = df['categ_id'].astype(str)  # Should map to real category name if available
    
    def extract_name(val):
        if isinstance(val, dict):
            return val.get('en_US', list(val.values())[0] if val else 'Unknown')
        return str(val)
        
    df['product_name'] = df['product_name'].apply(extract_name)
    return df[['product_id', 'product_name', 'category']]

def transform_sales_fact(sales_line_df: pd.DataFrame, sales_df: pd.DataFrame) -> pd.DataFrame:
    """Transform Odoo sales into Sales Fact."""
    if sales_line_df.empty or sales_df.empty:
        return pd.DataFrame(columns=['sales_id', 'date_id', 'customer_id', 'product_id', 'sales_amount', 'quantity', 'margin'])
    
    df = pd.merge(sales_line_df, sales_df, left_on='order_id', right_on='id', how='left')
    df.rename(columns={
        'id_x': 'sales_id', 
        'date_order': 'date_id', 
        'partner_id': 'customer_id', 
        'product_uom_qty': 'quantity', 
        'price_subtotal': 'sales_amount'
    }, inplace=True)
    
    df['date_id'] = pd.to_datetime(df['date_id']).dt.date
    df['margin'] = df['sales_amount'] * 0.20  # Mock margin calculation (20%)
    
    return df[['sales_id', 'date_id', 'customer_id', 'product_id', 'sales_amount', 'quantity', 'margin']]

def transform_data(raw_data: dict) -> dict:
    """Applies transformations to generate Dimensions and Facts."""
    print("Transforming data...")
    
    # 1. Clean Data
    cleaned_data = {k: clean_data(v) for k, v in raw_data.items()}
    
    # 2. Dimensions
    dim_customer = transform_customer_dimension(cleaned_data.get('partners', pd.DataFrame()))
    dim_product = transform_product_dimension(cleaned_data.get('products', pd.DataFrame()), cleaned_data.get('product_templates', pd.DataFrame()))
    
    # Extract all dates for dim_date
    sales_dates = cleaned_data.get('sales', pd.DataFrame()).get('date_order', pd.Series())
    dim_date = transform_date_dimension(sales_dates)
    
    # 3. Facts
    fact_sales = transform_sales_fact(cleaned_data.get('sales_line', pd.DataFrame()), cleaned_data.get('sales', pd.DataFrame()))
    
    # Empty placeholders for other facts for now, they follow the same pattern
    fact_inventory = pd.DataFrame(columns=['inventory_id', 'date_id', 'product_id', 'stock_level', 'stock_in', 'stock_out'])
    fact_purchase = pd.DataFrame(columns=['purchase_id', 'date_id', 'supplier_id', 'product_id', 'purchase_amount', 'lead_time_days'])
    fact_finance = pd.DataFrame(columns=['finance_id', 'date_id', 'revenue', 'expense', 'cash_in', 'cash_out'])
    fact_crm = pd.DataFrame(columns=['crm_id', 'date_id', 'lead_count', 'conversion_rate', 'expected_revenue'])

    print("Transformation complete.")
    
    return {
        "dim_date": dim_date,
        "dim_customer": dim_customer,
        "dim_product": dim_product,
        "fact_sales": fact_sales,
        "fact_inventory": fact_inventory,
        "fact_purchase": fact_purchase,
        "fact_finance": fact_finance,
        "fact_crm": fact_crm
    }
