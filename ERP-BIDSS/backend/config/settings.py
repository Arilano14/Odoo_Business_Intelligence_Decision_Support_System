import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Configuration for OBIDSS ETL Pipeline.
    
    Source: Odoo 18 PostgreSQL (operational database)
    Target: Analytics Mart (PostgreSQL schema 'mart')
    """
    SOURCE_DB_URL = os.getenv(
        "SOURCE_DB_URL",
        "postgresql://openpg:openpgpwd@localhost:5432/Business_Intelegent_Project_v2"
    )
    TARGET_DB_URL = os.getenv(
        "TARGET_DB_URL",
        "postgresql://openpg:openpgpwd@localhost:5432/Business_Intelegent_Project_v2"
    )
    TARGET_SCHEMA = os.getenv("TARGET_SCHEMA", "mart")
    ETL_BATCH_SIZE = int(os.getenv("ETL_BATCH_SIZE", "5000"))
    LOG_FILE = os.getenv("ETL_LOG_FILE", "etl_execution.log")


settings = Settings()
