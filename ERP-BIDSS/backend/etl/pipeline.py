from etl.logger import ETLLogger
from etl.extract import extract_table
from etl.transform import transform_sales
from etl.load import load_table

def run_pipeline():
    logger = ETLLogger("OBIDSS_ETL_PIPELINE")
    logger.start()
    
    print("Starting ETL Pipeline...")
    
    # 1. Extract
    df_so = extract_table('sale_order')
    df_sol = extract_table('sale_order_line')
    
    # 2. Transform
    fact_sales = transform_sales(df_so, df_sol)
    
    # 3. Load
    loaded_rows = load_table(fact_sales, 'fact_sales')
    
    logger.log_metric('fact_sales', extracted=len(df_sol), transformed=len(fact_sales), loaded=loaded_rows)
    logger.end()
    print("ETL Pipeline completed.")

if __name__ == "__main__":
    run_pipeline()
