import sys
import os
import json
import base64

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import db
from sqlalchemy import text
from odoo.connection import get_connection

print("============================================================")
print("STAGE 1 READ-ONLY DEEP DIAGNOSTIC AUDIT")
print("============================================================")

uid, models, odoo_db, password = get_connection()
print("Odoo XML-RPC Auth OK, UID:", uid)

with db.source_engine.connect() as conn:
    print("\n--- 1. Spreadsheet Dashboard Record Audit ---")
    dashboards = conn.execute(text("""
        SELECT d.id, d.name, d.dashboard_group_id, d.company_id, d.is_published, d.sample_dashboard_file_path,
               m.module, m.name as xml_id, m.noupdate
        FROM spreadsheet_dashboard d
        LEFT JOIN ir_model_data m ON (m.model='spreadsheet.dashboard' AND m.res_id=d.id)
        ORDER BY d.id
    """)).fetchall()
    for d in dashboards:
        print(f"ID: {d[0]:2d} | Name: {d[1]} | Group: {d[2]} | Comp: {d[3]} | Pub: {d[4]} | Path: {d[5]} | Module: {d[6]} | XML_ID: {d[7]} | noupdate: {d[8]}")

    print("\n--- 2. ID 8 Search in ir_model_data & spreadsheet_dashboard ---")
    id8_dash = conn.execute(text("SELECT * FROM spreadsheet_dashboard WHERE id=8")).fetchall()
    print("spreadsheet_dashboard ID 8:", id8_dash)
    id8_model_data = conn.execute(text("SELECT * FROM ir_model_data WHERE model='spreadsheet.dashboard' AND res_id=8")).fetchall()
    print("ir_model_data for res_id=8:", id8_model_data)

    print("\n--- 3. ir.attachment Audit for spreadsheet.dashboard ---")
    attachments = conn.execute(text("""
        SELECT id, name, res_model, res_id, res_field, checksum, file_size, store_fname
        FROM ir_attachment
        WHERE res_model='spreadsheet.dashboard' OR name LIKE '%spreadsheet%' OR name LIKE '%json%'
    """)).fetchall()
    print(f"Found {len(attachments)} related ir_attachment records:")
    for att in attachments:
        print(f"  Att ID: {att[0]} | Name: {att[1]} | Model: {att[2]} | Res_ID: {att[3]} | Field: {att[4]} | Checksum: {att[5]} | Size: {att[6]}")

    print("\n--- 4. Purchase Dashboard Module Check ---")
    purchase_modules = conn.execute(text("""
        SELECT name, state FROM ir_module_module 
        WHERE name LIKE '%spreadsheet_dashboard_purchase%' OR name LIKE '%purchase%'
        ORDER BY state, name
    """)).fetchall()
    print("Purchase related modules:")
    for pm in purchase_modules:
        if "spreadsheet" in pm[0] or pm[0] in ['purchase', 'purchase_stock', 'purchase_requisition']:
            print(f"  Module: {pm[0]:<35} | State: {pm[1]}")
