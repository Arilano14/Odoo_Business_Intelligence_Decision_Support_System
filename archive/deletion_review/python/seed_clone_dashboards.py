import sys
import os
import psycopg2

print("============================================================")
print("SEEDING SPREADSHEET DASHBOARD GROUPS & RECORDS ON CLONE DB")
print("============================================================")

conn_clone = psycopg2.connect(
    host="localhost",
    port=5432,
    user="openpg",
    password="openpgpwd",
    dbname="Business_Intelegent_Project_v2_phase11_2_clone"
)
cursor = conn_clone.cursor()

# 1. Create or fetch OBIDSS Group
cursor.execute("SELECT id FROM spreadsheet_dashboard_group WHERE name->>'en_US' = 'OBIDSS Operational BI'")
group_row = cursor.fetchone()

if not group_row:
    cursor.execute("""
        INSERT INTO spreadsheet_dashboard_group (name, sequence)
        VALUES ('{"en_US": "OBIDSS Operational BI"}'::jsonb, 5)
        RETURNING id
    """)
    group_id = cursor.fetchone()[0]
    print(f"Created Dashboard Group 'OBIDSS Operational BI' with ID: {group_id}")
else:
    group_id = group_row[0]
    print(f"Dashboard Group 'OBIDSS Operational BI' exists with ID: {group_id}")

# 2. Register Dashboard Records
dashboards_spec = [
    ("Executive Operations", 10),
    ("Sales Operations", 20),
    ("Purchase & Suppliers", 30),
    ("Inventory Operations", 40),
    ("Finance & Invoicing", 50),
    ("Data Quality & Reconciliation", 60),
]

for name, seq in dashboards_spec:
    cursor.execute(f"SELECT id FROM spreadsheet_dashboard WHERE dashboard_group_id = {group_id} AND name->>'en_US' = '{name}'")
    dash_row = cursor.fetchone()
    if not dash_row:
        cursor.execute(f"""
            INSERT INTO spreadsheet_dashboard (name, dashboard_group_id, sequence)
            VALUES ('{{"en_US": "{name}"}}'::jsonb, {group_id}, {seq})
            RETURNING id
        """)
        dash_id = cursor.fetchone()[0]
        print(f"Created Dashboard '{name}' with ID: {dash_id}")
    else:
        print(f"Dashboard '{name}' exists with ID: {dash_row[0]}")

# 3. Reparent menu 377 under host app 177
cursor.execute("""
    UPDATE ir_ui_menu 
    SET parent_id = 177, parent_path = '177/377/' 
    WHERE id = 377
""")
print("Reparented OBIDSS root menu (ID 377) -> Host App (ID 177)")

conn_clone.commit()
cursor.close()
conn_clone.close()
print("CLONE DATABASE SEEDING COMPLETED 100%!")
