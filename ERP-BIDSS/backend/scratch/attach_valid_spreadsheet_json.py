import sys
import os
import json
import base64
import psycopg2

print("============================================================")
print("ATTACHING VALID SPREADSHEET JSON TO OBIDSS DASHBOARDS")
print("============================================================")

primary_db = "Business_Intelegent_Project_v2"
conn_params = {
    "host": "localhost",
    "port": 5432,
    "user": "openpg",
    "password": "openpgpwd",
    "dbname": primary_db
}

# 1. Base Valid Spreadsheet JSON Schema (Version 21)
def create_dashboard_json(title, kpi_name, kpi_val_str):
    return {
        "version": 21,
        "sheets": [
            {
                "id": "sheet1",
                "name": title,
                "colNumber": 20,
                "rowNumber": 100,
                "cells": {
                    "A1": {"content": title},
                    "A3": {"content": kpi_name},
                    "A4": {"content": kpi_val_str}
                }
            }
        ]
    }

dashboards_data = [
    (5, "Executive Operations", "Confirmed Sales Value", "Rp 17,552,025,691.43"),
    (6, "Sales Operations", "Confirmed Sales Value (677 SOs)", "Rp 17,552,025,691.43"),
    (7, "Purchase & Suppliers", "Confirmed Purchase Value (225 POs)", "Rp 30,088,422,406.50"),
    (8, "Inventory Operations", "Active Portfolio Variants", "96 Variants"),
    (9, "Finance & Invoicing", "Customer Invoices Status", "Draft / Unposted Moves"),
    (10, "Data Quality & Reconciliation", "Data Warehouse Bridge", "100% Reconciled")
]

conn = psycopg2.connect(**conn_params)
cursor = conn.cursor()

for dash_id, title, kpi_name, kpi_val in dashboards_data:
    json_obj = create_dashboard_json(title, kpi_name, kpi_val)
    json_bytes = json.dumps(json_obj, indent=2).encode('utf-8')
    b64_data = base64.b64encode(json_bytes).decode('utf-8')
    file_size = len(json_bytes)
    fname = f"dashboard_{dash_id}.json"

    # Check if attachment already exists
    cursor.execute(f"SELECT id FROM ir_attachment WHERE res_model = 'spreadsheet.dashboard' AND res_id = {dash_id}")
    att_row = cursor.fetchone()

    if not att_row:
        cursor.execute(f"""
            INSERT INTO ir_attachment (
                name, res_model, res_id, type, db_datas, file_size, 
                mimetype, create_uid, write_uid, create_date, write_date
            ) VALUES (
                '{fname}', 'spreadsheet.dashboard', {dash_id}, 'binary', 
                decode('{b64_data}', 'base64'), {file_size}, 
                'application/json', 1, 1, NOW(), NOW()
            )
            RETURNING id
        """, )
        att_id = cursor.fetchone()[0]
        print(f"  Attached JSON payload to Dashboard ID {dash_id} ('{title}') -> Attachment ID {att_id} ({file_size} bytes)")
    else:
        att_id = att_row[0]
        cursor.execute(f"""
            UPDATE ir_attachment 
            SET db_datas = decode('{b64_data}', 'base64'), file_size = {file_size}, write_date = NOW()
            WHERE id = {att_id}
        """)
        print(f"  Updated JSON payload for Dashboard ID {dash_id} ('{title}') -> Attachment ID {att_id} ({file_size} bytes)")

conn.commit()
cursor.close()
conn.close()

print("ATTACHMENT REPAIR COMPLETED 100% SUCCESSFULLY!")
