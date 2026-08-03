import sys
import os
import json
import base64

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import db
from sqlalchemy import text

print("============================================================")
print("DIAGNOSING ODOO 18 SPREADSHEET JSON SCHEMA")
print("============================================================")

with db.source_engine.connect() as conn:
    rows = conn.execute(text("""
        SELECT id, name, res_model, res_field, db_datas FROM ir_attachment 
        WHERE res_model = 'spreadsheet.dashboard'
    """)).fetchall()
    
    print(f"Found {len(rows)} binary attachments for spreadsheet.dashboard:")
    for r in rows:
        att_id, name, model, field, raw_datas = r
        if raw_datas:
            try:
                decoded = base64.b64decode(raw_datas).decode('utf-8')
                js = json.loads(decoded)
                sheets = js.get('sheets', [])
                print(f"  ID {att_id}: Name='{name}' | JSON Keys={list(js.keys())} | Sheets Count={len(sheets)}")
            except Exception as e:
                print(f"  ID {att_id}: Name='{name}' | Decode Error: {e}")
