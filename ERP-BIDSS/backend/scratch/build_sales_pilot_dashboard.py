import json
import base64
import psycopg2
import os

print("=" * 80)
print("GATE 2E.4 — BUILDING SALES OPERATIONS PILOT DASHBOARD WITH LIVE DATA SOURCES")
print("=" * 80)

# Global filter IDs
GF_PERIOD_ID = "gf_period_sales_01"
GF_CATEG_ID = "gf_categ_sales_02"
GF_PARTNER_ID = "gf_partner_sales_03"
GF_STATE_ID = "gf_state_sales_04"

# 1. Construct live Sales Operations Dashboard JSON (Version 21)
sales_dashboard_json = {
    "version": 21,
    "settings": {
        "locale": {
            "name": "English (US)",
            "code": "en_US",
            "thousandsSeparator": ",",
            "decimalSeparator": ".",
            "dateFormat": "MM/DD/YYYY",
            "timeFormat": "hh:mm:ss a",
            "formulaPrefix": "="
        }
    },
    "pivots": {
        "1": {
            "type": "ODOO",
            "id": "1",
            "formulaId": "1",
            "name": "Confirmed Sales Summary (Company 2 FY2026)",
            "model": "sale.report",
            "domain": [
                ["company_id", "=", 2],
                ["state", "in", ["sale", "done"]]
            ],
            "measures": [
                {"id": "price_subtotal", "fieldName": "price_subtotal"},
                {"id": "untaxed_amount_to_invoice", "fieldName": "untaxed_amount_to_invoice"},
                {"id": "order_reference", "fieldName": "order_reference"}
            ],
            "rows": [],
            "columns": [],
            "fieldMatching": {
                GF_PERIOD_ID: {"chain": "date", "type": "datetime", "offset": 0},
                GF_CATEG_ID: {"chain": "categ_id", "type": "many2one"},
                GF_PARTNER_ID: {"chain": "partner_id", "type": "many2one"}
            },
            "context": {"group_by": []}
        },
        "2": {
            "type": "ODOO",
            "id": "2",
            "formulaId": "2",
            "name": "Cancelled Sales Summary (Company 2 FY2026)",
            "model": "sale.report",
            "domain": [
                ["company_id", "=", 2],
                ["state", "=", "cancel"]
            ],
            "measures": [
                {"id": "order_reference", "fieldName": "order_reference"},
                {"id": "price_subtotal", "fieldName": "price_subtotal"}
            ],
            "rows": [],
            "columns": [],
            "fieldMatching": {
                GF_PERIOD_ID: {"chain": "date", "type": "datetime", "offset": 0},
                GF_CATEG_ID: {"chain": "categ_id", "type": "many2one"},
                GF_PARTNER_ID: {"chain": "partner_id", "type": "many2one"}
            },
            "context": {"group_by": []}
        },
        "3": {
            "type": "ODOO",
            "id": "3",
            "formulaId": "3",
            "name": "Top Product Categories Sales",
            "model": "sale.report",
            "domain": [
                ["company_id", "=", 2],
                ["state", "in", ["sale", "done"]]
            ],
            "measures": [
                {"id": "price_subtotal", "fieldName": "price_subtotal"},
                {"id": "order_reference", "fieldName": "order_reference"}
            ],
            "rows": [{"fieldName": "categ_id"}],
            "columns": [],
            "sortedColumn": {
                "groupId": [[], []],
                "measure": "price_subtotal",
                "order": "desc"
            },
            "fieldMatching": {
                GF_PERIOD_ID: {"chain": "date", "type": "datetime", "offset": 0},
                GF_CATEG_ID: {"chain": "categ_id", "type": "many2one"},
                GF_PARTNER_ID: {"chain": "partner_id", "type": "many2one"}
            },
            "context": {"group_by": []}
        }
    },
    "lists": {
        "1": {
            "id": "1",
            "name": "Recent Confirmed Sales Orders",
            "model": "sale.order",
            "domain": [
                ["company_id", "=", 2],
                ["state", "in", ["sale", "done"]]
            ],
            "columns": ["name", "partner_id", "date_order", "amount_total", "state"],
            "orderBy": [{"name": "date_order", "asc": False}],
            "fieldMatching": {
                GF_PERIOD_ID: {"chain": "date_order", "type": "datetime", "offset": 0},
                GF_PARTNER_ID: {"chain": "partner_id", "type": "many2one"}
            }
        }
    },
    "globalFilters": [
        {
            "id": GF_PERIOD_ID,
            "type": "date",
            "label": "Date Period",
            "defaultValue": "this_year",
            "rangeType": "relative"
        },
        {
            "id": GF_CATEG_ID,
            "type": "relation",
            "label": "Product Category",
            "modelName": "product.category",
            "defaultValue": [],
            "defaultValueDisplayNames": []
        },
        {
            "id": GF_PARTNER_ID,
            "type": "relation",
            "label": "Customer",
            "modelName": "res.partner",
            "defaultValue": [],
            "defaultValueDisplayNames": []
        }
    ],
    "sheets": [
        {
            "id": "sheet_dashboard",
            "name": "Sales Operations",
            "colNumber": 12,
            "rowNumber": 60,
            "cells": {
                "A1": {"content": "PT Prima Alat Nusantara — Sales Operations Dashboard (FY 2026)", "style": 1},
                
                # Navigation links (drill-down)
                "A3": {"content": "[View All Sales Orders](odoo://view/{\"viewType\":\"list\",\"action\":{\"domain\":[[\"company_id\",\"=\",2]],\"modelName\":\"sale.order\",\"views\":[[false,\"list\"],[false,\"form\"]]},\"name\":\"Sales Orders\"})"},
                "D3": {"content": "[View Sales Analysis Pivot](odoo://view/{\"viewType\":\"pivot\",\"action\":{\"domain\":[[\"company_id\",\"=\",2]],\"context\":{\"group_by\":[\"date:month\",\"categ_id\"],\"pivot_measures\":[\"price_subtotal\",\"order_reference\"]},\"modelName\":\"sale.report\",\"views\":[[false,\"pivot\"]]},\"name\":\"Sales Analysis\"})"},
                "G3": {"content": "[View Product Catalog](odoo://view/{\"viewType\":\"list\",\"action\":{\"domain\":[],\"modelName\":\"product.product\",\"views\":[[false,\"list\"],[false,\"form\"]]},\"name\":\"Products\"})"},
                
                # Section Header: Category Breakdown
                "A16": {"content": "Top Sales Categories Breakdown", "style": 2},
                "A17": {"content": "Category", "style": 3},
                "B17": {"content": "Revenue (IDR)", "style": 3},
                "C17": {"content": "Orders Count", "style": 3},
                
                # Dynamic Pivot Header & Values
                "A18": {"content": "=PIVOT.HEADER(3,\"#categ_id\",1)"},
                "B18": {"content": "=PIVOT.VALUE(3,\"price_subtotal\",\"#categ_id\",1)"},
                "C18": {"content": "=PIVOT.VALUE(3,\"order_reference\",\"#categ_id\",1)"},
                
                "A19": {"content": "=PIVOT.HEADER(3,\"#categ_id\",2)"},
                "B19": {"content": "=PIVOT.VALUE(3,\"price_subtotal\",\"#categ_id\",2)"},
                "C19": {"content": "=PIVOT.VALUE(3,\"order_reference\",\"#categ_id\",2)"},
                
                "A20": {"content": "=PIVOT.HEADER(3,\"#categ_id\",3)"},
                "B20": {"content": "=PIVOT.VALUE(3,\"price_subtotal\",\"#categ_id\",3)"},
                "C20": {"content": "=PIVOT.VALUE(3,\"order_reference\",\"#categ_id\",3)"},
                
                "A21": {"content": "=PIVOT.HEADER(3,\"#categ_id\",4)"},
                "B21": {"content": "=PIVOT.VALUE(3,\"price_subtotal\",\"#categ_id\",4)"},
                "C21": {"content": "=PIVOT.VALUE(3,\"order_reference\",\"#categ_id\",4)"},

                "A22": {"content": "=PIVOT.HEADER(3,\"#categ_id\",5)"},
                "B22": {"content": "=PIVOT.VALUE(3,\"price_subtotal\",\"#categ_id\",5)"},
                "C22": {"content": "=PIVOT.VALUE(3,\"order_reference\",\"#categ_id\",5)"}
            },
            "figures": [
                # Scorecard 1: Confirmed Sales Value
                {
                    "id": "scorecard_confirmed_sales",
                    "tag": "chart",
                    "width": 260,
                    "height": 110,
                    "x": 20,
                    "y": 60,
                    "data": {
                        "type": "scorecard",
                        "title": {"text": "Confirmed Sales Value", "bold": True, "color": "#1E3A8A"},
                        "keyValue": "Data!B2",
                        "background": "#EFF6FF",
                        "humanize": False
                    }
                },
                # Scorecard 2: Confirmed Orders Count
                {
                    "id": "scorecard_so_count",
                    "tag": "chart",
                    "width": 260,
                    "height": 110,
                    "x": 300,
                    "y": 60,
                    "data": {
                        "type": "scorecard",
                        "title": {"text": "Confirmed Orders (SOs)", "bold": True, "color": "#065F46"},
                        "keyValue": "Data!B3",
                        "background": "#ECFDF5",
                        "humanize": False
                    }
                },
                # Scorecard 3: Average Order Value
                {
                    "id": "scorecard_aov",
                    "tag": "chart",
                    "width": 260,
                    "height": 110,
                    "x": 580,
                    "y": 60,
                    "data": {
                        "type": "scorecard",
                        "title": {"text": "Average Order Value (AOV)", "bold": True, "color": "#92400E"},
                        "keyValue": "Data!B4",
                        "background": "#FFFBEB",
                        "humanize": False
                    }
                },
                # Scorecard 4: Cancelled Orders Count
                {
                    "id": "scorecard_cancelled_so",
                    "tag": "chart",
                    "width": 260,
                    "height": 110,
                    "x": 860,
                    "y": 60,
                    "data": {
                        "type": "scorecard",
                        "title": {"text": "Cancelled Orders", "bold": True, "color": "#991B1B"},
                        "keyValue": "Data!B5",
                        "background": "#FEF2F2",
                        "humanize": False
                    }
                },
                # Odoo Line Chart: Monthly Sales Trend
                {
                    "id": "chart_monthly_sales_trend",
                    "tag": "chart",
                    "width": 640,
                    "height": 320,
                    "x": 480,
                    "y": 200,
                    "data": {
                        "type": "odoo_line",
                        "title": {"text": "Monthly Sales Revenue Trend (FY 2026)", "bold": True},
                        "background": "#FFFFFF",
                        "legendPosition": "none",
                        "resModel": "sale.report",
                        "metaData": {
                            "resModel": "sale.report",
                            "groupBy": ["date:month"],
                            "measure": "price_subtotal",
                            "mode": "line",
                            "order": None
                        },
                        "searchParams": {
                            "domain": [["company_id", "=", 2], ["state", "in", ["sale", "done"]]],
                            "groupBy": ["date:month"],
                            "orderBy": [],
                            "context": {}
                        },
                        "verticalAxisPosition": "left",
                        "stacked": False,
                        "fillArea": True,
                        "fieldMatching": {
                            GF_PERIOD_ID: {"chain": "date", "type": "datetime", "offset": 0},
                            GF_CATEG_ID: {"chain": "categ_id", "type": "many2one"},
                            GF_PARTNER_ID: {"chain": "partner_id", "type": "many2one"}
                        }
                    }
                }
            ]
        },
        {
            "id": "sheet_data",
            "name": "Data",
            "colNumber": 10,
            "rowNumber": 30,
            "cells": {
                "A1": {"content": "Metric Name", "style": 3},
                "B1": {"content": "Value (Live Pivot Formula)", "style": 3},
                
                "A2": {"content": "Confirmed Sales Revenue"},
                "B2": {"content": "=PIVOT.VALUE(1,\"price_subtotal\")"},
                
                "A3": {"content": "Confirmed Order Count"},
                "B3": {"content": "=PIVOT.VALUE(1,\"order_reference\")"},
                
                "A4": {"content": "Average Order Value"},
                "B4": {"content": "=IFERROR(B2/B3, 0)"},
                
                "A5": {"content": "Cancelled Order Count"},
                "B5": {"content": "=PIVOT.VALUE(2,\"order_reference\")"}
            }
        }
    ],
    "styles": {
        "1": {"fontSize": 14, "bold": True, "textColor": "#1E3A8A"},
        "2": {"fontSize": 12, "bold": True, "textColor": "#1F2937"},
        "3": {"bold": True, "fillColor": "#F3F4F6", "textColor": "#111827"}
    }
}

# Save JSON to module data directory: custom_addons/obidss_operational_bi/data/files/sales_operations_dashboard.json
json_bytes = json.dumps(sales_dashboard_json, indent=2).encode('utf-8')
file_size = len(json_bytes)
b64_payload = base64.b64encode(json_bytes).decode('utf-8')

save_path = r"c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\custom_addons\obidss_operational_bi\data\files\sales_operations_dashboard.json"
os.makedirs(os.path.dirname(save_path), exist_ok=True)
with open(save_path, 'wb') as f:
    f.write(json_bytes)

print(f"Saved Sales Operations Dashboard JSON to: {save_path} ({file_size} bytes)")

# 2. Deploy payload to Database ID 6 (Sales Operations) with correct res_field='spreadsheet_binary_data'
conn = psycopg2.connect(host='localhost', port=5432, user='openpg', password='openpgpwd', dbname='Business_Intelegent_Project_v2')
cur = conn.cursor()

# Set is_published = True for Dashboard ID 6
cur.execute("UPDATE spreadsheet_dashboard SET is_published = true WHERE id = 6")

# Check if correct attachment already exists
cur.execute("""
    SELECT id FROM ir_attachment 
    WHERE res_model = 'spreadsheet.dashboard' 
      AND res_id = 6 
      AND res_field = 'spreadsheet_binary_data'
""")
row = cur.fetchone()

if not row:
    cur.execute(f"""
        INSERT INTO ir_attachment (
            name, res_model, res_id, res_field, type, db_datas, file_size, 
            mimetype, create_uid, write_uid, create_date, write_date
        ) VALUES (
            'spreadsheet_binary_data', 'spreadsheet.dashboard', 6, 'spreadsheet_binary_data', 'binary', 
            decode('{b64_payload}', 'base64'), {file_size}, 
            'application/json', 1, 1, NOW(), NOW()
        )
        RETURNING id
    """)
    att_id = cur.fetchone()[0]
    print(f"Created NEW live attachment ID {att_id} with res_field='spreadsheet_binary_data'")
else:
    att_id = row[0]
    cur.execute(f"""
        UPDATE ir_attachment 
        SET db_datas = decode('{b64_payload}', 'base64'), 
            file_size = {file_size}, 
            mimetype = 'application/json',
            write_date = NOW()
        WHERE id = {att_id}
    """)
    print(f"Updated EXISTING live attachment ID {att_id} with res_field='spreadsheet_binary_data'")

conn.commit()

# Verify attachment in DB
cur.execute("""
    SELECT a.id, a.res_model, a.res_id, a.res_field, a.name, a.file_size, a.mimetype,
           d.name->>'en_US' as dash_name, d.is_published
    FROM ir_attachment a
    JOIN spreadsheet_dashboard d ON a.res_id = d.id
    WHERE a.res_model = 'spreadsheet.dashboard' AND a.res_id = 6 AND a.res_field = 'spreadsheet_binary_data'
""")
verif = cur.fetchone()
print("\nVERIFICATION RESULT FROM DB:")
print(f"  Dashboard ID: {verif[2]} ({verif[7]}) | Published: {verif[8]}")
print(f"  Attachment ID: {verif[0]} | Name: {verif[4]} | Field: {verif[3]} | Size: {verif[5]} bytes | Mime: {verif[6]}")

cur.close()
conn.close()
