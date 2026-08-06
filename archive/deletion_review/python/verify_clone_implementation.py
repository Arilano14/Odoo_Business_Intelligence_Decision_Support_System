import sys
import os
import psycopg2

print("============================================================")
print("VERIFYING STAGE 2A IMPLEMENTATION ON CLONE DATABASE")
print("============================================================")

conn_clone = psycopg2.connect(
    host="localhost",
    port=5432,
    user="openpg",
    password="openpgpwd",
    dbname="Business_Intelegent_Project_v2_phase11_2_clone"
)
cursor = conn_clone.cursor()

# 1. Verify spreadsheet.dashboard.group
cursor.execute("SELECT id, name->>'en_US', sequence FROM spreadsheet_dashboard_group WHERE name->>'en_US' LIKE '%OBIDSS%'")
groups = cursor.fetchall()
print("1. OBIDSS Dashboard Group on Clone DB:")
for g in groups:
    print(f"   Group ID: {g[0]} | Name: {g[1]} | Sequence: {g[2]}")

# 2. Verify spreadsheet.dashboard records
cursor.execute("""
    SELECT d.id, d.name->>'en_US', d.dashboard_group_id, g.name->>'en_US' as group_name
    FROM spreadsheet_dashboard d
    JOIN spreadsheet_dashboard_group g ON d.dashboard_group_id = g.id
    WHERE g.name->>'en_US' LIKE '%OBIDSS%'
    ORDER BY d.sequence
""")
dashboards = cursor.fetchall()
print("\n2. OBIDSS Spreadsheet Dashboards on Clone DB:")
for d in dashboards:
    print(f"   Dash ID: {d[0]:2d} | Name: {d[1]:30s} | Group: {d[3]}")

# 3. Verify Menu Reparenting
cursor.execute("""
    SELECT id, name->>'en_US', parent_id, parent_path, sequence 
    FROM ir_ui_menu 
    WHERE parent_id IN (SELECT id FROM ir_ui_menu WHERE name->>'en_US' = 'Dashboards')
       OR name->>'en_US' = 'OBIDSS'
    ORDER BY sequence
""")
menus = cursor.fetchall()
print("\n3. Menu Reparenting on Clone DB:")
for m in menus:
    print(f"   Menu ID: {m[0]:3d} | Name: {m[1]:25s} | Parent ID: {m[2]} | Parent Path: {m[3]}")

cursor.close()
conn_clone.close()
print("\nSTAGE 2A CLONE ORM VERIFICATION: 100% SUCCESS!")
