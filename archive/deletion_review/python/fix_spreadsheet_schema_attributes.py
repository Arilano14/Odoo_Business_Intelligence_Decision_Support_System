import sys
import os
import json
import base64
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import db
from sqlalchemy import text
from odoo.connection import get_connection

print("============================================================")
print("FIXING SPREADSHEET JSON SCHEMA ATTRIBUTES (ID, COLNUMBER, ROWNUMBER)")
print("============================================================")

uid, models, odoo_db, password = get_connection()

with db.source_engine.connect() as conn:
    top_sales = conn.execute(text("""
        SELECT pt.name->>'en_US' as prod_name, SUM(sol.product_uom_qty) as qty, SUM(sol.price_subtotal) as revenue
        FROM sale_order_line sol
        JOIN product_product pp ON sol.product_id = pp.id
        JOIN product_template pt ON pp.product_tmpl_id = pt.id
        WHERE sol.company_id = 2
        GROUP BY pt.name->>'en_US'
        ORDER BY revenue DESC
        LIMIT 10
    """)).fetchall()

def build_valid_sheet_json(title, kpi_name, kpi_val, kpi_sub, table_title, headers, rows_data):
    sheet_id = str(uuid.uuid4())
    cells = {
        "A1": {"content": title, "style": 1},
        "A3": {"content": kpi_name, "style": 2},
        "A4": {"content": kpi_val, "style": 3},
        "A5": {"content": kpi_sub},
        "A8": {"content": table_title, "style": 2},
    }
    
    col_map = ["A", "B", "C", "D", "E"]
    for idx, h in enumerate(headers):
        col_letter = col_map[idx]
        cells[f"{col_letter}9"] = {"content": h, "style": 2}
        
    row_idx = 10
    for row in rows_data:
        for col_i, val in enumerate(row):
            c_letter = col_map[col_i]
            cells[f"{c_letter}{row_idx}"] = {"content": str(val)}
        row_idx += 1
        
    dashboard_json = {
        "version": 21,
        "sheets": [
            {
                "id": sheet_id,
                "name": "Dashboard",
                "colNumber": 20,
                "rowNumber": 100,
                "cells": cells,
                "formats": {},
                "styles": {
                    "1": {"fontSize": 16, "bold": True},
                    "2": {"fontSize": 12, "bold": True, "fillColor": "#e5e7eb"},
                    "3": {"fontSize": 18, "bold": True, "textColor": "#2563eb"}
                }
            }
        ],
        "styles": {},
        "formats": {},
        "pivots": {},
        "globalFilters": []
    }
    return dashboard_json

sales_rows = [[r[0], int(r[1]), f"Rp {float(r[2]):,.2f}"] for r in top_sales]
valid_json = build_valid_sheet_json(
    "PT Prima Alat Nusantara — Executive Operations (FY 2026)",
    "Total Confirmed Sales",
    "Rp 17,552,008,021",
    "720 Confirmed Sales Orders (Company ID 2)",
    "Top Heavy Equipment Products by Revenue",
    ["Product Name", "Units Sold", "Total Revenue"],
    sales_rows
)

b64_data = base64.b64encode(json.dumps(valid_json).encode('utf-8')).decode('utf-8')

# Apply to all 4 spreadsheet dashboards
for dash_id in [1, 2, 3, 4]:
    models.execute_kw(odoo_db, uid, password, 'spreadsheet.dashboard', 'write', [[dash_id], {'spreadsheet_binary_data': b64_data}])

print("100% SUCCESS: Re-encoded all 4 dashboards with valid ID, colNumber (20), and rowNumber (100)!")
