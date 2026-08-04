import psycopg2, json, base64

conn = psycopg2.connect(host='localhost', port=5432, user='openpg', password='openpgpwd', dbname='Business_Intelegent_Project_v2')
cursor = conn.cursor()

# Check how official dashboards store their binary data via the mixin field
print("=== ATTACHMENTS FOR spreadsheet_binary_data FIELD ===")
cursor.execute("""
    SELECT a.id, a.res_model, a.res_id, a.res_field, a.name, a.file_size, 
           a.store_fname, a.db_datas IS NOT NULL as has_db, a.mimetype
    FROM ir_attachment a
    WHERE a.res_model = 'spreadsheet.dashboard'
    ORDER BY a.res_id, a.id
""")
for row in cursor.fetchall():
    att_id, rm, ri, rf, name, fsize, sfn, hasdb, mime = row
    print(f"  Att {att_id}: res_id={ri} | res_field={rf} | name={name} | size={fsize} | store={sfn} | db={hasdb} | mime={mime}")

print()

# Now check: are the official dashboards using res_field='spreadsheet_binary_data'?  
print("=== OFFICIAL ATTACHMENT STRUCTURE ===")
cursor.execute("""
    SELECT a.id, a.res_id, a.res_field, a.name, a.file_size, a.store_fname
    FROM ir_attachment a
    WHERE a.res_model = 'spreadsheet.dashboard' AND a.res_id IN (1,2,3,4)
    ORDER BY a.res_id
""")
for row in cursor.fetchall():
    print(f"  Att {row[0]}: dash_id={row[1]} | field={row[2]} | name={row[3]} | size={row[4]} | store={row[5]}")

print()
print("=== OBIDSS ATTACHMENT STRUCTURE ===")
cursor.execute("""
    SELECT a.id, a.res_id, a.res_field, a.name, a.file_size, a.store_fname, a.db_datas IS NOT NULL
    FROM ir_attachment a
    WHERE a.res_model = 'spreadsheet.dashboard' AND a.res_id IN (5,6,7,8,9,10)
    ORDER BY a.res_id
""")
for row in cursor.fetchall():
    print(f"  Att {row[0]}: dash_id={row[1]} | field={row[2]} | name={row[3]} | size={row[4]} | store={row[5]} | db={row[6]}")

print()

# Critical: Check if spreadsheet_binary_data column exists on spreadsheet_dashboard table
cursor.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'spreadsheet_dashboard' AND column_name LIKE '%spreadsheet%'
""")
print("=== SPREADSHEET COLUMNS ON TABLE ===")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

# The truth: is spreadsheet_binary_data stored via attachment mechanism (not table column)
# Let's verify by checking ir_attachment with res_field

cursor.close()
conn.close()
