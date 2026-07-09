# Database Management Utilities

# --- From drop_db.py ---
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn = psycopg2.connect(user='openpg', password='openpgpwd', host='localhost', port='5432', database='postgres')
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()

try:
    cursor.execute("SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'eid_analytics' AND pid != pg_backend_pid();")
    cursor.execute("DROP DATABASE IF EXISTS eid_analytics")
    print("Database eid_analytics dropped successfully.")
except Exception as e:
    print(f"Error: {e}")
finally:
    cursor.close()
    conn.close()


# --- From init_db.py ---
from app.models.schema import Base
from app.database.connection import engine

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

    init_db()


# --- From setup_db.py ---
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    try:
        # Connect to the default database
        conn = psycopg2.connect(
            user="openpg",
            password="openpgpwd",
            host="localhost",
            port="5432",
            database="postgres" # Connect to default db to create a new one
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'eid_analytics'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute("CREATE DATABASE eid_analytics")
            print("Database 'eid_analytics' created successfully.")
        else:
            print("Database 'eid_analytics' already exists.")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

    create_database()


