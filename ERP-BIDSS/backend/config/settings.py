import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SOURCE_DB_URL = os.getenv("SOURCE_DB_URL", "postgresql://odoo:odoo@localhost:5432/odoo_db")
    TARGET_DB_URL = os.getenv("TARGET_DB_URL", "postgresql://odoo:odoo@localhost:5432/odoo_mart")
    ETL_BATCH_SIZE = int(os.getenv("ETL_BATCH_SIZE", "5000"))

settings = Settings()
