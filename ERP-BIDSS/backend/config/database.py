from sqlalchemy import create_engine, text
from .settings import settings


class DatabaseConnection:
    """Manages connections to Odoo source DB and Analytics Mart target."""

    def __init__(self):
        self.source_engine = create_engine(settings.SOURCE_DB_URL)
        self.target_engine = create_engine(settings.TARGET_DB_URL)

    def test_connections(self):
        """Test both source and target database connections."""
        results = {}
        try:
            with self.source_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            results["source"] = True
            print("[OK] Source DB (Odoo 18) connected.")
        except Exception as e:
            results["source"] = False
            print(f"[FAIL] Source DB: {e}")

        try:
            with self.target_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                # Ensure mart schema exists
                conn.execute(text(
                    f"CREATE SCHEMA IF NOT EXISTS {settings.TARGET_SCHEMA}"
                ))
                conn.commit()
            results["target"] = True
            print(f"[OK] Target DB (schema '{settings.TARGET_SCHEMA}') connected.")
        except Exception as e:
            results["target"] = False
            print(f"[FAIL] Target DB: {e}")

        return results


db = DatabaseConnection()
