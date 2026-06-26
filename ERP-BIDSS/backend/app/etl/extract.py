import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def get_odoo_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("ODOO_DB_HOST", "localhost"),
            port=os.getenv("ODOO_DB_PORT", "5432"),
            user=os.getenv("ODOO_DB_USER", "openpg"),
            password=os.getenv("ODOO_DB_PASSWORD", "openpgpwd"),
            database=os.getenv("ODOO_DB_NAME", "odoo")
        )
        return conn
    except Exception as e:
        print(f"Error connecting to Odoo database: {e}")
        return None

def extract_table(table_name: str, columns: list = None) -> pd.DataFrame:
    """Extracts data from a specific Odoo table."""
    conn = get_odoo_connection()
    if not conn:
        return pd.DataFrame()
    
    try:
        col_str = "*" if not columns else ", ".join(columns)
        query = f"SELECT {col_str} FROM {table_name}"
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        print(f"Error extracting table {table_name}: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def extract_all():
    """Extracts all necessary data for EID-SME."""
    print("Extracting data from Odoo...")
    
    sales_df = extract_table("sale_order", ["id", "date_order", "partner_id", "amount_total", "state"])
    sales_line_df = extract_table("sale_order_line", ["id", "order_id", "product_id", "product_uom_qty", "price_subtotal"])
    
    inventory_df = extract_table("stock_move", ["id", "product_id", "location_id", "location_dest_id", "product_uom_qty", "state", "date"])
    
    purchase_df = extract_table("purchase_order", ["id", "partner_id", "date_order", "date_planned", "amount_total", "state"])
    purchase_line_df = extract_table("purchase_order_line", ["id", "order_id", "product_id", "product_qty", "price_subtotal"])
    
    accounting_move_df = extract_table("account_move", ["id", "date", "partner_id", "amount_total", "state", "move_type"])
    
    crm_df = extract_table("crm_lead", ["id", "name", "stage_id", "expected_revenue", "probability", "create_date"])
    
    partners_df = extract_table("res_partner", ["id", "name", "category_id", "country_id"])
    products_df = extract_table("product_product", ["id", "product_tmpl_id", "default_code"])
    product_tmpl_df = extract_table("product_template", ["id", "name", "categ_id"])
    
    print("Extraction complete.")
    
    return {
        "sales": sales_df,
        "sales_line": sales_line_df,
        "inventory": inventory_df,
        "purchase": purchase_df,
        "purchase_line": purchase_line_df,
        "accounting": accounting_move_df,
        "crm": crm_df,
        "partners": partners_df,
        "products": products_df,
        "product_templates": product_tmpl_df
    }

if __name__ == "__main__":
    data = extract_all()
    for name, df in data.items():
        print(f"{name}: {len(df)} records")
