"""
ETL Logger — Logs pipeline execution metrics.
"""
import logging
import time
from config.settings import settings


logging.basicConfig(
    filename=settings.LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class ETLLogger:
    """Logs ETL pipeline execution metrics."""

    def __init__(self, process_name: str):
        self.process_name = process_name
        self.start_time = None

    def start(self):
        self.start_time = time.time()
        logging.info(f"START {self.process_name}")

    def log_metric(self, table: str, extracted=0, transformed=0, loaded=0, failed=0):
        logging.info(
            f"TABLE: {table} | "
            f"Extracted: {extracted} | Transformed: {transformed} | "
            f"Loaded: {loaded} | Failed: {failed}"
        )

    def end(self):
        duration = time.time() - self.start_time
        logging.info(f"END {self.process_name} | Duration: {duration:.2f}s")
        print(f"\n[LOG] Pipeline duration: {duration:.2f}s")
