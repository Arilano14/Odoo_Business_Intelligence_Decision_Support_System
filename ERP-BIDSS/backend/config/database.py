from sqlalchemy import create_engine
from .settings import settings
import pandas as pd

class DatabaseConnection:
    def __init__(self):
        self.source_engine = create_engine(settings.SOURCE_DB_URL)
        self.target_engine = create_engine(settings.TARGET_DB_URL)
        
    def test_connections(self):
        try:
            with self.source_engine.connect() as conn:
                print("Source DB connected")
            with self.target_engine.connect() as conn:
                print("Target DB connected")
            return True
        except Exception as e:
            print(f"Connection failed: {str(e)}")
            return False

db = DatabaseConnection()
