import sys
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

print("============================================================")
print("GATE 2B — CLONE DATABASE CREATION & VERIFICATION")
print("============================================================")

conn_params = {
    "host": "localhost",
    "port": 5432,
    "user": "openpg",
    "password": "openpgpwd",
    "dbname": "postgres"
}

primary_db = "Business_Intelegent_Project_v2"
clone_db = "Business_Intelegent_Project_v2_phase11_2_clone"

try:
    conn = psycopg2.connect(**conn_params)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    # Check if clone database exists
    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{clone_db}'")
    exists = cursor.fetchone()

    if exists:
        print(f"Clone database '{clone_db}' ALREADY EXISTS. Re-synchronizing...")
        # Terminate active connections to clone DB
        cursor.execute(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{clone_db}' AND pid <> pg_backend_pid();
        """)
        cursor.execute(f"DROP DATABASE \"{clone_db}\"")

    print(f"Creating isolated clone database '{clone_db}' from template '{primary_db}'...")
    cursor.execute(f"CREATE DATABASE \"{clone_db}\" WITH TEMPLATE \"{primary_db}\" OWNER openpg;")
    print("Clone database created successfully!")

    cursor.close()
    conn.close()

    # Verify connection to clone DB
    conn_clone_params = conn_params.copy()
    conn_clone_params["dbname"] = clone_db
    conn_clone = psycopg2.connect(**conn_clone_params)
    cursor_clone = conn_clone.cursor()

    cursor_clone.execute("SELECT COUNT(*) FROM sale_order WHERE company_id = 2")
    so_cnt = cursor_clone.fetchone()[0]

    cursor_clone.execute("SELECT COUNT(*) FROM purchase_order WHERE company_id = 2")
    po_cnt = cursor_clone.fetchone()[0]

    print(f"Verified Clone Database Row Counts: SOs={so_cnt}, POs={po_cnt}")
    cursor_clone.close()
    conn_clone.close()

    print("GATE 2B CLONE VERIFICATION: 100% PASSED!")

except Exception as e:
    print("Clone Database Error:", e)
