# Gate 1: Targeted Test on Sales Operations Dashboard (ID 30)
# Testing #date:month and #categ_id syntax on Sales Operations pilot

import json
import base64

dashboard = env.ref('obidss_operational_bi.dashboard_sales')
print(f"Targeting pilot dashboard: {dashboard.name} (ID: {dashboard.id})")

# Let's inspect the sale.order model for pivot usage
# Model: sale.order
# Pivot 1: Confirmed Sales Value (measure: amount_untaxed)
# Pivot 2: Top Categories (rows: categ_id via sale.order.line or sale.report)
# Pivot 3: Top Products (rows: product_id via sale.order.line or sale.report)
# Pivot 4: Top Salespeople (rows: user_id)
# Pivot 5: Monthly Sales Trend (columns: date_order:month)

payload = {
    "version": 21,
    "settings": {
        "locale": {"name": "English (US)", "code": "en_US", "formulaPrefix": "="}
    },
    "pivots": {
        "1": {
            "type": "ODOO", "id": "1", "formulaId": "1",
            "name": "Confirmed Sales Value",
            "model": "sale.order",
            "domain": [["company_id", "=", 2], ["state", "=", "sale"], ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]],
            "measures": [{"id": "amount_untaxed", "fieldName": "amount_untaxed"}],
            "rows": [], "columns": [], "fieldMatching": {}
        },
        "2": {
            "type": "ODOO", "id": "2", "formulaId": "2",
            "name": "Top Categories",
            "model": "sale.report",
            "domain": [["company_id", "=", 2], ["state", "=", "sale"], ["date", ">=", "2026-01-01"], ["date", "<", "2027-01-01"]],
            "measures": [{"id": "price_subtotal", "fieldName": "price_subtotal"}],
            "rows": [{"fieldName": "categ_id"}], "columns": [], "fieldMatching": {}
        },
        "3": {
            "type": "ODOO", "id": "3", "formulaId": "3",
            "name": "Top Products",
            "model": "sale.report",
            "domain": [["company_id", "=", 2], ["state", "=", "sale"], ["date", ">=", "2026-01-01"], ["date", "<", "2027-01-01"]],
            "measures": [{"id": "price_subtotal", "fieldName": "price_subtotal"}],
            "rows": [{"fieldName": "product_tmpl_id"}], "columns": [], "fieldMatching": {}
        },
        "4": {
            "type": "ODOO", "id": "4", "formulaId": "4",
            "name": "Top Salespeople",
            "model": "sale.order",
            "domain": [["company_id", "=", 2], ["state", "=", "sale"], ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]],
            "measures": [{"id": "amount_untaxed", "fieldName": "amount_untaxed"}],
            "rows": [{"fieldName": "user_id"}], "columns": [], "fieldMatching": {}
        },
        "5": {
            "type": "ODOO", "id": "5", "formulaId": "5",
            "name": "Monthly Sales Trend",
            "model": "sale.order",
            "domain": [["company_id", "=", 2], ["state", "=", "sale"], ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]],
            "measures": [{"id": "amount_untaxed", "fieldName": "amount_untaxed"}],
            "rows": [], "columns": [{"fieldName": "date_order:month"}], "fieldMatching": {}
        }
    },
    "lists": {},
    "globalFilters": [],
    "sheets": [
        {
            "id": "sales_dashboard", "name": "Sales Dashboard",
            "colNumber": 26, "rowNumber": 100,
            "cells": {
                "A1": {"content": "Sales Overview (FY 2026)", "style": 1},
                "A3": {"content": "Total Confirmed Sales Value (Untaxed)", "style": 2},
                "B3": {"content": "=PIVOT.VALUE(1,\"amount_untaxed\")", "style": 3},
            },
            "figures": [
                {
                    "id": "chart_categories", "tag": "chart", "width": 500, "height": 300, "x": 20, "y": 120,
                    "data": {
                        "type": "bar", "title": {"text": "Sales by Category"},
                        "background": "#FFFFFF", "legendPosition": "none", "axesDesign": {"x": {}, "y": {}},
                        "dataSetsHaveTitle": False, "dataSets": [{"dataRange": "Data!B2:B6"}], "labelRange": "Data!A2:A6"
                    }
                },
                {
                    "id": "chart_products", "tag": "chart", "width": 500, "height": 300, "x": 540, "y": 120,
                    "data": {
                        "type": "bar", "title": {"text": "Top Products"},
                        "background": "#FFFFFF", "legendPosition": "none", "axesDesign": {"x": {}, "y": {}},
                        "dataSetsHaveTitle": False, "dataSets": [{"dataRange": "Data!D2:D6"}], "labelRange": "Data!C2:C6"
                    }
                },
                {
                    "id": "chart_salespeople", "tag": "chart", "width": 500, "height": 300, "x": 20, "y": 440,
                    "data": {
                        "type": "bar", "title": {"text": "Sales by Salesperson"},
                        "background": "#FFFFFF", "legendPosition": "none", "axesDesign": {"x": {}, "y": {}},
                        "dataSetsHaveTitle": False, "dataSets": [{"dataRange": "Data!F2:F6"}], "labelRange": "Data!E2:E6"
                    }
                },
                {
                    "id": "chart_monthly", "tag": "chart", "width": 500, "height": 300, "x": 540, "y": 440,
                    "data": {
                        "type": "line", "title": {"text": "Monthly Sales Trend"},
                        "background": "#FFFFFF", "legendPosition": "none", "axesDesign": {"x": {}, "y": {}},
                        "dataSetsHaveTitle": False, "dataSets": [{"dataRange": "Data!I2:I13"}], "labelRange": "Data!H2:H13"
                    }
                }
            ]
        },
        {
            "id": "sales_data", "name": "Data",
            "colNumber": 26, "rowNumber": 100,
            "cells": {
                "A1": {"content": "Category"}, "B1": {"content": "Value"},
                "A2": {"content": "=PIVOT.HEADER(2,\"#categ_id\",1)"}, "B2": {"content": "=PIVOT.VALUE(2,\"price_subtotal\",\"#categ_id\",1)"},
                "A3": {"content": "=PIVOT.HEADER(2,\"#categ_id\",2)"}, "B3": {"content": "=PIVOT.VALUE(2,\"price_subtotal\",\"#categ_id\",2)"},
                "A4": {"content": "=PIVOT.HEADER(2,\"#categ_id\",3)"}, "B4": {"content": "=PIVOT.VALUE(2,\"price_subtotal\",\"#categ_id\",3)"},
                "A5": {"content": "=PIVOT.HEADER(2,\"#categ_id\",4)"}, "B5": {"content": "=PIVOT.VALUE(2,\"price_subtotal\",\"#categ_id\",4)"},
                "A6": {"content": "=PIVOT.HEADER(2,\"#categ_id\",5)"}, "B6": {"content": "=PIVOT.VALUE(2,\"price_subtotal\",\"#categ_id\",5)"},

                "C1": {"content": "Product"}, "D1": {"content": "Value"},
                "C2": {"content": "=PIVOT.HEADER(3,\"#product_tmpl_id\",1)"}, "D2": {"content": "=PIVOT.VALUE(3,\"price_subtotal\",\"#product_tmpl_id\",1)"},
                "C3": {"content": "=PIVOT.HEADER(3,\"#product_tmpl_id\",2)"}, "D3": {"content": "=PIVOT.VALUE(3,\"price_subtotal\",\"#product_tmpl_id\",2)"},
                "C4": {"content": "=PIVOT.HEADER(3,\"#product_tmpl_id\",3)"}, "D4": {"content": "=PIVOT.VALUE(3,\"price_subtotal\",\"#product_tmpl_id\",3)"},
                "C5": {"content": "=PIVOT.HEADER(3,\"#product_tmpl_id\",4)"}, "D5": {"content": "=PIVOT.VALUE(3,\"price_subtotal\",\"#product_tmpl_id\",4)"},
                "C6": {"content": "=PIVOT.HEADER(3,\"#product_tmpl_id\",5)"}, "D6": {"content": "=PIVOT.VALUE(3,\"price_subtotal\",\"#product_tmpl_id\",5)"},

                "E1": {"content": "Salesperson"}, "F1": {"content": "Value"},
                "E2": {"content": "=PIVOT.HEADER(4,\"#user_id\",1)"}, "F2": {"content": "=PIVOT.VALUE(4,\"amount_untaxed\",\"#user_id\",1)"},
                "E3": {"content": "=PIVOT.HEADER(4,\"#user_id\",2)"}, "F3": {"content": "=PIVOT.VALUE(4,\"amount_untaxed\",\"#user_id\",2)"},
                "E4": {"content": "=PIVOT.HEADER(4,\"#user_id\",3)"}, "F4": {"content": "=PIVOT.VALUE(4,\"amount_untaxed\",\"#user_id\",3)"},
                "E5": {"content": "=PIVOT.HEADER(4,\"#user_id\",4)"}, "F5": {"content": "=PIVOT.VALUE(4,\"amount_untaxed\",\"#user_id\",4)"},
                "E6": {"content": "=PIVOT.HEADER(4,\"#user_id\",5)"}, "F6": {"content": "=PIVOT.VALUE(4,\"amount_untaxed\",\"#user_id\",5)"},

                "H1": {"content": "Month"}, "I1": {"content": "Sales Value"},
                "H2": {"content": "=PIVOT.HEADER(5,\"#date_order:month\",1)"}, "I2": {"content": "=PIVOT.VALUE(5,\"amount_untaxed\",\"#date_order:month\",1)"},
                "H3": {"content": "=PIVOT.HEADER(5,\"#date_order:month\",2)"}, "I3": {"content": "=PIVOT.VALUE(5,\"amount_untaxed\",\"#date_order:month\",2)"},
                "H4": {"content": "=PIVOT.HEADER(5,\"#date_order:month\",3)"}, "I4": {"content": "=PIVOT.VALUE(5,\"amount_untaxed\",\"#date_order:month\",3)"},
                "H5": {"content": "=PIVOT.HEADER(5,\"#date_order:month\",4)"}, "I5": {"content": "=PIVOT.VALUE(5,\"amount_untaxed\",\"#date_order:month\",4)"},
                "H6": {"content": "=PIVOT.HEADER(5,\"#date_order:month\",5)"}, "I6": {"content": "=PIVOT.VALUE(5,\"amount_untaxed\",\"#date_order:month\",5)"},
                "H7": {"content": "=PIVOT.HEADER(5,\"#date_order:month\",6)"}, "I7": {"content": "=PIVOT.VALUE(5,\"amount_untaxed\",\"#date_order:month\",6)"},
                "H8": {"content": "=PIVOT.HEADER(5,\"#date_order:month\",7)"}, "I8": {"content": "=PIVOT.VALUE(5,\"amount_untaxed\",\"#date_order:month\",7)"},
                "H9": {"content": "=PIVOT.HEADER(5,\"#date_order:month\",8)"}, "I9": {"content": "=PIVOT.VALUE(5,\"amount_untaxed\",\"#date_order:month\",8)"},
                "H10": {"content": "=PIVOT.HEADER(5,\"#date_order:month\",9)"}, "I10": {"content": "=PIVOT.VALUE(5,\"amount_untaxed\",\"#date_order:month\",9)"},
                "H11": {"content": "=PIVOT.HEADER(5,\"#date_order:month\",10)"}, "I11": {"content": "=PIVOT.VALUE(5,\"amount_untaxed\",\"#date_order:month\",10)"},
                "H12": {"content": "=PIVOT.HEADER(5,\"#date_order:month\",11)"}, "I12": {"content": "=PIVOT.VALUE(5,\"amount_untaxed\",\"#date_order:month\",11)"},
                "H13": {"content": "=PIVOT.HEADER(5,\"#date_order:month\",12)"}, "I13": {"content": "=PIVOT.VALUE(5,\"amount_untaxed\",\"#date_order:month\",12)"},
            }
        }
    ],
    "styles": {
        "1": {"fontSize": 16, "bold": True, "textColor": "#1E3A8A"},
        "2": {"fontSize": 12, "bold": True},
        "3": {"fontSize": 18, "bold": True, "textColor": "#065F46"}
    }
}

b64_bytes = base64.b64encode(json.dumps(payload).encode('utf-8'))
dashboard.write({'spreadsheet_binary_data': b64_bytes})
env.cr.commit()

print("Gate 1 Pilot payload written successfully to Sales Operations dashboard!")
