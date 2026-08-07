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
        "postgresql://openpg:openpgpwd@localhost:5432/Business_Intelegent_Project_v2_fresh_clone"
    )
    TARGET_DB_URL = os.getenv(
        "TARGET_DB_URL",
        "postgresql://openpg:openpgpwd@localhost:5432/Business_Intelegent_Project_v2_fresh_clone"
    )
    TARGET_SCHEMA = os.getenv("TARGET_SCHEMA", "mart")
    ETL_BATCH_SIZE = int(os.getenv("ETL_BATCH_SIZE", "5000"))
    LOG_FILE = os.getenv("ETL_LOG_FILE", "etl_execution.log")

    # Phase 10 Centralized Alignment Settings
    ANALYSIS_START_DATE = os.getenv("ANALYSIS_START_DATE", "2024-01-01")
    ANALYSIS_END_DATE = os.getenv("ANALYSIS_END_DATE", "2026-12-31")
    TARGET_COMPANY_ID = int(os.getenv("TARGET_COMPANY_ID", "2"))
    CUSTOMER_REF_PREFIX = os.getenv("CUSTOMER_REF_PREFIX", "PORTFOLIO_2026_V1-CUST-")
    VENDOR_REF_PREFIX = os.getenv("VENDOR_REF_PREFIX", "PORTFOLIO_2026_V1-VEND-")


settings = Settings()
