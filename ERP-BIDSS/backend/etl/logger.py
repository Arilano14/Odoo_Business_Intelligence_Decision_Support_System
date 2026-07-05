import logging
import time

logging.basicConfig(
    filename='etl_execution.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ETLLogger:
    def __init__(self, process_name):
        self.process_name = process_name
        self.start_time = None
        
    def start(self):
        self.start_time = time.time()
        logging.info(f"START {self.process_name}")
        
    def log_metric(self, table, extracted=0, transformed=0, loaded=0, failed=0):
        logging.info(f"TABLE: {table} | Extracted: {extracted} | Transformed: {transformed} | Loaded: {loaded} | Failed: {failed}")
        
    def end(self):
        duration = time.time() - self.start_time
        logging.info(f"END {self.process_name} | Duration: {duration:.2f}s")
