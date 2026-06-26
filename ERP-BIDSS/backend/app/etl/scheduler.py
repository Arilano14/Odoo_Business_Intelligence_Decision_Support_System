from apscheduler.schedulers.background import BackgroundScheduler
import time
from app.etl.extract import extract_all
from app.etl.transform import transform_data
from app.etl.load import load_data

def run_etl_pipeline():
    print("--- Starting ETL Pipeline ---")
    try:
        raw_data = extract_all()
        transformed_data = transform_data(raw_data)
        load_data(transformed_data)
        print("--- ETL Pipeline Completed Successfully ---")
    except Exception as e:
        print(f"--- ETL Pipeline Failed: {e} ---")

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Schedule to run every hour for testing, in production it could be daily or weekly
    scheduler.add_job(run_etl_pipeline, 'interval', hours=1)
    scheduler.start()
    print("ETL Scheduler started.")
    
if __name__ == "__main__":
    # If run directly, execute the pipeline once
    run_etl_pipeline()
