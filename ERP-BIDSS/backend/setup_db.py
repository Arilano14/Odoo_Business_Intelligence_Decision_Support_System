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

if __name__ == "__main__":
    create_database()
