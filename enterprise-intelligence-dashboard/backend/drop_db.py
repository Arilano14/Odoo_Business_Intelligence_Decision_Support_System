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
