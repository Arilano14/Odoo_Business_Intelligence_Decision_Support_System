import psycopg2, json, base64, zlib

conn = psycopg2.connect(host='localhost', port=5432, user='openpg', password='openpgpwd', dbname='Business_Intelegent_Project_v2')
cursor = conn.cursor()

# First: understand how official dashboards store data
cursor.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'spreadsheet_dashboard'
    ORDER BY ordinal_position
""")
print("=== TABLE SCHEMA: spreadsheet_dashboard ===")
for c in cursor.fetchall():
    print(f"  {c[0]:35s} | {c[1]}")

# Check if data is stored in the record itself or only via attachment
print("\n=== CHECKING DASHBOARD DATA STORAGE ===")
cursor.execute("""
    SELECT d.id, d.name->>'en_US', d.sample_dashboard_file_path,
           (SELECT COUNT(*) FROM ir_attachment a 
            WHERE a.res_model='spreadsheet.dashboard' AND a.res_id=d.id) as att_count,
           (SELECT a.file_size FROM ir_attachment a 
            WHERE a.res_model='spreadsheet.dashboard' AND a.res_id=d.id 
            ORDER BY a.id DESC LIMIT 1) as att_size,
           (SELECT a.store_fname FROM ir_attachment a 
            WHERE a.res_model='spreadsheet.dashboard' AND a.res_id=d.id 
            ORDER BY a.id DESC LIMIT 1) as store_fname,
           (SELECT a.db_datas IS NOT NULL FROM ir_attachment a 
            WHERE a.res_model='spreadsheet.dashboard' AND a.res_id=d.id 
            ORDER BY a.id DESC LIMIT 1) as has_db_data
    FROM spreadsheet_dashboard d
    ORDER BY d.id
""")
for row in cursor.fetchall():
    print(f"  Dash {row[0]:2d} | {row[1]:35s} | sample_path: {str(row[2]):50s} | att_count: {row[3]} | att_size: {row[4]} | store_fname: {row[5]} | has_db: {row[6]}")

# Inspect ONE official attachment fully
print("\n=== OFFICIAL SALES DASHBOARD (ID 3) ATTACHMENT DETAIL ===")
cursor.execute("""
    SELECT a.id, a.name, a.file_size, a.store_fname, a.db_datas IS NOT NULL, a.checksum, a.mimetype
    FROM ir_attachment a 
    WHERE a.res_model='spreadsheet.dashboard' AND a.res_id=3
""")
att = cursor.fetchone()
if att:
    print(f"  Attach ID: {att[0]} | Name: {att[1]} | Size: {att[2]} | store_fname: {att[3]} | db_datas present: {att[4]} | checksum: {att[5]} | mime: {att[6]}")

# Now try reading via store_fname (filestore)
if att and att[3]:
    import os
    filestore_base = r"C:\Program Files\Odoo 18.0.20241229\sessions\filestore\Business_Intelegent_Project_v2"
    fpath = os.path.join(filestore_base, att[3])
    if os.path.exists(fpath):
        with open(fpath, 'rb') as f:
            raw = f.read()
        print(f"  Filestore file exists: {fpath} ({len(raw)} bytes)")
        # Try direct JSON parse
        try:
            obj = json.loads(raw)
            print(f"  Direct JSON parse OK!")
        except:
            # Try decompression
            try:
                decompressed = zlib.decompress(raw)
                obj = json.loads(decompressed)
                print(f"  Zlib-decompressed JSON parse OK! ({len(decompressed)} bytes)")
            except:
                print(f"  Cannot parse as JSON or zlib+JSON")
                obj = None
        
        if obj:
            print(f"  Top-level keys: {sorted(obj.keys())}")
            ver = obj.get("version")
            print(f"  Version: {ver}")
            pivots = obj.get("pivots", {})
            lists_ = obj.get("lists", {})
            gf = obj.get("globalFilters", [])
            print(f"  Pivots: {len(pivots)}")
            print(f"  Lists: {len(lists_)}")
            print(f"  GlobalFilters: {len(gf)}")
            for pid, pdata in pivots.items():
                print(f"    Pivot '{pid}': model={pdata.get('model')}, measures={pdata.get('measures',[])}") 
            for lid, ldata in lists_.items():
                print(f"    List '{lid}': model={ldata.get('model')}")
    else:
        print(f"  Filestore file NOT found: {fpath}")

# Now inspect OBIDSS dashboard attachments
print("\n=== OBIDSS DASHBOARD ATTACHMENTS ===")
for did in [5, 6, 7, 8, 9, 10]:
    cursor.execute("""
        SELECT a.id, a.name, a.file_size, a.store_fname, a.db_datas IS NOT NULL, a.checksum
        FROM ir_attachment a 
        WHERE a.res_model='spreadsheet.dashboard' AND a.res_id=%s
    """, (did,))
    att2 = cursor.fetchone()
    if att2:
        print(f"  Dash {did}: Attach ID={att2[0]} | Size={att2[2]} | store={att2[3]} | db_present={att2[4]} | cksum={att2[5]}")
        # Try reading db_datas
        if att2[4]:
            cursor.execute("SELECT encode(db_datas, 'escape') FROM ir_attachment WHERE id=%s", (att2[0],))
            raw_str = cursor.fetchone()[0]
            if raw_str:
                try:
                    obj2 = json.loads(raw_str)
                    pivots2 = obj2.get("pivots", {})
                    lists2 = obj2.get("lists", {})
                    charts2 = obj2.get("charts", {})
                    gf2 = obj2.get("globalFilters", [])
                    cells2 = obj2.get("sheets", [{}])[0].get("cells", {})
                    print(f"         Pivots={len(pivots2)} Lists={len(lists2)} Charts={len(charts2)} Filters={len(gf2)} Cells={len(cells2)}")
                    if len(pivots2) == 0 and len(lists2) == 0 and len(charts2) == 0:
                        print(f"         CLASSIFICATION: STATIC_PLACEHOLDER (no live datasources)")
                    else:
                        print(f"         CLASSIFICATION: LIVE_OPERATIONAL_DASHBOARD")
                except Exception as e:
                    print(f"         JSON parse error: {e}")
    else:
        print(f"  Dash {did}: NO ATTACHMENT!")

cursor.close()
conn.close()
