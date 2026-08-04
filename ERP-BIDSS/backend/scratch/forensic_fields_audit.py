import sys
import os
import psycopg2

print("============================================================")
print("FORENSIC INSPECTION OF SPREADSHEET DASHBOARD COLUMNS & ATTACHMENTS")
print("============================================================")

primary_db = "Business_Intelegent_Project_v2"
conn_params = {
    "host": "localhost",
    "port": 5432,
    "user": "openpg",
    "password": "openpgpwd",
    "dbname": primary_db
}

conn = psycopg2.connect(**conn_params)
cursor = conn.cursor()

# 1. Get column names of spreadsheet.dashboard
cursor.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'spreadsheet_dashboard'
""")
cols = cursor.fetchall()
print("Columns in 'spreadsheet_dashboard' table:")
for c in cols:
    print(f"  {c[0]:30s} | {c[1]}")

# 2. Inspect dashboards in spreadsheet_dashboard
cursor.execute("""
    SELECT id, name->>'en_US', dashboard_group_id
    FROM spreadsheet_dashboard
    ORDER BY id
""")
dashes = cursor.fetchall()
print("\nAll Dashboards in Primary DB:")
for d in dashes:
    cursor.execute(f"SELECT id, name, file_size, checksum FROM ir_attachment WHERE res_model='spreadsheet.dashboard' AND res_id={d[0]}")
    att = cursor.fetchone()
    att_str = f"Attachment ID {att[0]} ({att[2]} bytes)" if att else "NO ATTACHMENT!"
    print(f"  Dash ID: {d[0]:2d} | Name: {d[1]:30s} | Group ID: {d[2]} | {att_str}")

# 3. Check official Odoo sample dashboards (IDs 1, 2, 3, 4) vs OBIDSS dashboards (IDs 5, 6, 7, 8, 9, 10)
print("\nAttachment Comparison:")
for d in dashes:
    cursor.execute(f"SELECT id, name, file_size FROM ir_attachment WHERE res_model='spreadsheet.dashboard' AND res_id={d[0]}")
    att = cursor.fetchall()
    if not att:
        print(f"  [MISSING ATTACHMENT] Dashboard ID {d[0]} ('{d[1]}') has ZERO attached JSON data!")

cursor.close()
conn.close()
