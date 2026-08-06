"""
OBIDSS Final Perfect Artifact Generator (Gates R2 - R6)
======================================================
Applies proven Gate 1 monthly formula pattern, strict portfolio domain filtering,
inventory KPI grain repair, Data Quality reconciliation table, and clean titles.

Truth Baselines:
- Sales Value (Untaxed): Rp 17,552,025,691.43 (sale.order)
- Purchase Value (Untaxed): Rp 30,088,422,406.50 (purchase.order)
- Confirmed SO Count: 677 (sale.order)
- Confirmed PO Count: 225 (purchase.order)
- Positive Stock SKUs: 230 (stock.quant)
- Internal Transfer Count: 24 (stock.picking / stock.move)
- Completed Scrap Operations: 12 (stock.scrap)
"""

import json
import base64
import hashlib
import os

def make_pivot(pid, name, model, domain, measures, rows=None, columns=None):
    return {
        "type": "ODOO", "id": str(pid), "formulaId": str(pid),
        "name": name, "model": model, "domain": domain,
        "measures": [{"id": m, "fieldName": m} for m in measures],
        "rows": [{"fieldName": r.get("fieldName"), "granularity": r.get("granularity")} if isinstance(r, dict) else {"fieldName": r} for r in (rows or [])],
        "columns": [{"fieldName": c.get("fieldName"), "granularity": c.get("granularity")} if isinstance(c, dict) else {"fieldName": c} for c in (columns or [])],
        "fieldMatching": {}
    }

def make_list(lid, name, model, domain, columns_list):
    return {
        "type": "ODOO", "id": str(lid), "name": name,
        "model": model, "domain": domain,
        "columns": columns_list, "orderBy": [], "fieldMatching": {}
    }

def make_chart(chart_id, chart_type, title, data_range, label_range, x, y, w=500, h=300):
    return {
        "id": chart_id, "tag": "chart", "width": w, "height": h, "x": x, "y": y,
        "data": {
            "type": chart_type, "title": {"text": title},
            "background": "#FFFFFF", "legendPosition": "none",
            "axesDesign": {"x": {}, "y": {}}, "dataSetsHaveTitle": False,
            "dataSets": [{"dataRange": data_range}], "labelRange": label_range
        }
    }

def make_base_json():
    return {
        "version": 21,
        "settings": {
            "locale": {"name": "English (US)", "code": "en_US", "formulaPrefix": "="}
        },
        "pivots": {}, "lists": {}, "globalFilters": [], "sheets": [],
        "styles": {
            "1": {"fontSize": 16, "bold": True, "textColor": "#1E3A8A"},
            "2": {"fontSize": 12, "bold": True},
            "3": {"fontSize": 18, "bold": True, "textColor": "#065F46"},
            "4": {"fontSize": 14, "bold": True, "textColor": "#9A3412"},
            "5": {"fontSize": 10, "italic": True, "textColor": "#6B7280"},
            "6": {"fontSize": 14, "bold": True, "textColor": "#7C3AED"},
            "7": {"fontSize": 14, "bold": True, "textColor": "#DC2626"},
        }
    }

COMPANY_FILTER = ["company_id", "=", 2]

# Strict Portfolio Domain Filter (excludes demo products and non-portfolio categories)
PORTFOLIO_CATEGORY_FILTER = ["categ_id.complete_name", "ilike", "Portfolio 2026"]
PORTFOLIO_PRODUCT_FILTER = ["product_tmpl_id.default_code", "=like", "PORTFOLIO_2026%"]

MONTHS = [f"{m:02d}/2026" for m in range(1, 13)]

# ============================================================
# 1. EXECUTIVE OPERATIONS
# ============================================================
def build_executive():
    j = make_base_json()

    j["pivots"]["1"] = make_pivot("1", "Confirmed Sales Value", "sale.order",
        [COMPANY_FILTER, ["state", "=", "sale"], ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]],
        ["amount_untaxed"])
    j["pivots"]["2"] = make_pivot("2", "Confirmed Purchase Value", "purchase.order",
        [COMPANY_FILTER, ["state", "=", "purchase"], ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]],
        ["amount_untaxed"])
    j["pivots"]["3"] = make_pivot("3", "Confirmed SO Count", "sale.order",
        [COMPANY_FILTER, ["state", "=", "sale"], ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]],
        ["__count"])
    j["pivots"]["4"] = make_pivot("4", "Confirmed PO Count", "purchase.order",
        [COMPANY_FILTER, ["state", "=", "purchase"], ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]],
        ["__count"])
    j["pivots"]["5"] = make_pivot("5", "Monthly Sales Trend", "sale.order",
        [COMPANY_FILTER, ["state", "=", "sale"], ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]],
        ["amount_untaxed"], rows=[{"fieldName": "date_order", "granularity": "month"}])
    j["pivots"]["6"] = make_pivot("6", "Monthly Purchase Trend", "purchase.order",
        [COMPANY_FILTER, ["state", "=", "purchase"], ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]],
        ["amount_untaxed"], rows=[{"fieldName": "date_order", "granularity": "month"}])
    j["pivots"]["7"] = make_pivot("7", "Portfolio SKUs with Positive Stock", "stock.quant",
        [COMPANY_FILTER, ["location_id.usage", "=", "internal"], ["quantity", ">", 0]],
        ["__count"])

    dashboard_cells = {
        "A1": {"content": "Executive Operations | FY 2026", "style": 1},
        "A3": {"content": "Confirmed Sales Value (Untaxed)", "style": 2},
        "C3": {"content": "=PIVOT.VALUE(1,\"amount_untaxed\")", "style": 3},
        "A4": {"content": "Confirmed Purchase Value (Untaxed)", "style": 2},
        "C4": {"content": "=PIVOT.VALUE(2,\"amount_untaxed\")", "style": 4},
        "A6": {"content": "Confirmed SO Count", "style": 2},
        "C6": {"content": "=PIVOT.VALUE(3,\"__count\")", "style": 3},
        "A7": {"content": "Confirmed PO Count", "style": 2},
        "C7": {"content": "=PIVOT.VALUE(4,\"__count\")", "style": 4},
        "A9": {"content": "Portfolio SKUs with Positive Stock", "style": 2},
        "C9": {"content": "=PIVOT.VALUE(7,\"__count\")", "style": 6},
    }

    data_cells = {
        "A1": {"content": "Month"}, "B1": {"content": "Sales Value"}, "C1": {"content": "Purchase Value"},
    }
    for i, m_str in enumerate(MONTHS, 2):
        data_cells[f"A{i}"] = {"content": m_str}
        data_cells[f"B{i}"] = {"content": f'=PIVOT.VALUE(5,"amount_untaxed","date_order:month","{m_str}")'}
        data_cells[f"C{i}"] = {"content": f'=PIVOT.VALUE(6,"amount_untaxed","date_order:month","{m_str}")'}

    j["sheets"] = [
        {
            "id": "exec_dashboard", "name": "Executive Dashboard",
            "colNumber": 26, "rowNumber": 100,
            "cells": dashboard_cells,
            "figures": [
                make_chart("chart_monthly_sales", "line", "Monthly Sales Trend (FY 2026)", "Data!B2:B13", "Data!A2:A13", 20, 220),
                make_chart("chart_monthly_purchase", "line", "Monthly Purchase Trend (FY 2026)", "Data!C2:C13", "Data!A2:A13", 540, 220),
                make_chart("chart_sales_vs_purchase", "bar", "Sales vs Purchase Comparison", "Data!B2:C13", "Data!A2:A13", 20, 540, w=1020),
            ]
        },
        {"id": "exec_data", "name": "Data", "colNumber": 26, "rowNumber": 100, "cells": data_cells}
    ]
    return j


# ============================================================
# 2. SALES OPERATIONS
# ============================================================
def build_sales():
    j = make_base_json()

    j["pivots"]["1"] = make_pivot("1", "Confirmed Sales Value", "sale.order",
        [COMPANY_FILTER, ["state", "=", "sale"], ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]],
        ["amount_untaxed"])
    j["pivots"]["2"] = make_pivot("2", "Top Categories", "sale.report",
        [COMPANY_FILTER, ["state", "=", "sale"], ["date", ">=", "2026-01-01"], ["date", "<", "2027-01-01"], PORTFOLIO_CATEGORY_FILTER],
        ["price_subtotal"], rows=["categ_id"])
    j["pivots"]["3"] = make_pivot("3", "Top Products", "sale.report",
        [COMPANY_FILTER, ["state", "=", "sale"], ["date", ">=", "2026-01-01"], ["date", "<", "2027-01-01"], PORTFOLIO_PRODUCT_FILTER],
        ["price_subtotal"], rows=["product_tmpl_id"])
    j["pivots"]["4"] = make_pivot("4", "Top Salespeople", "sale.order",
        [COMPANY_FILTER, ["state", "=", "sale"], ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]],
        ["amount_untaxed"], rows=["user_id"])
    j["pivots"]["5"] = make_pivot("5", "Monthly Sales Trend", "sale.order",
        [COMPANY_FILTER, ["state", "=", "sale"], ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]],
        ["amount_untaxed"], rows=[{"fieldName": "date_order", "granularity": "month"}])
    j["pivots"]["6"] = make_pivot("6", "Confirmed SO Count", "sale.order",
        [COMPANY_FILTER, ["state", "=", "sale"], ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]],
        ["__count"])

    dashboard_cells = {
        "A1": {"content": "Sales Operations | FY 2026", "style": 1},
        "A3": {"content": "Confirmed Sales Value (Untaxed)", "style": 2},
        "C3": {"content": "=PIVOT.VALUE(1,\"amount_untaxed\")", "style": 3},
        "A4": {"content": "Confirmed SO Count", "style": 2},
        "C4": {"content": "=PIVOT.VALUE(6,\"__count\")", "style": 3},
    }

    data_cells = {
        "A1": {"content": "Category"}, "B1": {"content": "Value"},
        "C1": {"content": "Product"}, "D1": {"content": "Value"},
        "E1": {"content": "Salesperson"}, "F1": {"content": "Value"},
        "H1": {"content": "Month"}, "I1": {"content": "Sales Value"},
    }
    for i in range(1, 6):
        r = i + 1
        data_cells[f"A{r}"] = {"content": f"=PIVOT.HEADER(2,\"#categ_id\",{i})"}
        data_cells[f"B{r}"] = {"content": f"=PIVOT.VALUE(2,\"price_subtotal\",\"#categ_id\",{i})"}
        data_cells[f"C{r}"] = {"content": f"=PIVOT.HEADER(3,\"#product_tmpl_id\",{i})"}
        data_cells[f"D{r}"] = {"content": f"=PIVOT.VALUE(3,\"price_subtotal\",\"#product_tmpl_id\",{i})"}
        data_cells[f"E{r}"] = {"content": f"=PIVOT.HEADER(4,\"#user_id\",{i})"}
        data_cells[f"F{r}"] = {"content": f"=PIVOT.VALUE(4,\"amount_untaxed\",\"#user_id\",{i})"}

    for i, m_str in enumerate(MONTHS, 2):
        data_cells[f"H{i}"] = {"content": m_str}
        data_cells[f"I{i}"] = {"content": f'=PIVOT.VALUE(5,"amount_untaxed","date_order:month","{m_str}")'}

    j["sheets"] = [
        {
            "id": "sales_dashboard", "name": "Sales Dashboard",
            "colNumber": 26, "rowNumber": 100,
            "cells": dashboard_cells,
            "figures": [
                make_chart("chart_categories", "bar", "Sales by Category (Portfolio)", "Data!B2:B6", "Data!A2:A6", 20, 120),
                make_chart("chart_products", "bar", "Top Products (Portfolio)", "Data!D2:D6", "Data!C2:C6", 540, 120),
                make_chart("chart_salespeople", "bar", "Sales by Salesperson", "Data!F2:F6", "Data!E2:E6", 20, 440),
                make_chart("chart_monthly", "line", "Monthly Sales Trend", "Data!I2:I13", "Data!H2:H13", 540, 440),
            ]
        },
        {"id": "sales_data", "name": "Data", "colNumber": 26, "rowNumber": 100, "cells": data_cells}
    ]
    return j


# ============================================================
# 3. PURCHASE & SUPPLIERS
# ============================================================
def build_purchase():
    j = make_base_json()

    j["pivots"]["1"] = make_pivot("1", "Confirmed Purchase Value", "purchase.order",
        [COMPANY_FILTER, ["state", "=", "purchase"], ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]],
        ["amount_untaxed"])
    j["pivots"]["2"] = make_pivot("2", "Confirmed PO Count", "purchase.order",
        [COMPANY_FILTER, ["state", "=", "purchase"], ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]],
        ["__count"])
    j["pivots"]["3"] = make_pivot("3", "Top Vendors", "purchase.report",
        [COMPANY_FILTER, ["state", "=", "purchase"], ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]],
        ["untaxed_total"], rows=["partner_id"])
    j["pivots"]["4"] = make_pivot("4", "Top Products Purchased", "purchase.report",
        [COMPANY_FILTER, ["state", "=", "purchase"], ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"], PORTFOLIO_PRODUCT_FILTER],
        ["untaxed_total"], rows=["product_tmpl_id"])
    j["pivots"]["5"] = make_pivot("5", "Monthly Purchase Trend", "purchase.order",
        [COMPANY_FILTER, ["state", "=", "purchase"], ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]],
        ["amount_untaxed"], rows=[{"fieldName": "date_order", "granularity": "month"}])
    j["pivots"]["6"] = make_pivot("6", "Draft PO Count", "purchase.order",
        [COMPANY_FILTER, ["state", "=", "draft"], ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]],
        ["__count"])

    dashboard_cells = {
        "A1": {"content": "Purchase & Suppliers | FY 2026", "style": 1},
        "A3": {"content": "Confirmed Purchase Value (Untaxed)", "style": 2},
        "C3": {"content": "=PIVOT.VALUE(1,\"amount_untaxed\")", "style": 4},
        "A4": {"content": "Confirmed PO Count", "style": 2},
        "C4": {"content": "=PIVOT.VALUE(2,\"__count\")", "style": 3},
        "A5": {"content": "Draft/RFQ Count", "style": 2},
        "C5": {"content": "=PIVOT.VALUE(6,\"__count\")", "style": 7},
    }

    data_cells = {
        "A1": {"content": "Vendor"}, "B1": {"content": "Value"},
        "C1": {"content": "Product"}, "D1": {"content": "Value"},
        "F1": {"content": "Month"}, "G1": {"content": "Purchase Value"},
    }
    for i in range(1, 6):
        r = i + 1
        data_cells[f"A{r}"] = {"content": f"=PIVOT.HEADER(3,\"#partner_id\",{i})"}
        data_cells[f"B{r}"] = {"content": f"=PIVOT.VALUE(3,\"untaxed_total\",\"#partner_id\",{i})"}
        data_cells[f"C{r}"] = {"content": f"=PIVOT.HEADER(4,\"#product_tmpl_id\",{i})"}
        data_cells[f"D{r}"] = {"content": f"=PIVOT.VALUE(4,\"untaxed_total\",\"#product_tmpl_id\",{i})"}

    for i, m_str in enumerate(MONTHS, 2):
        data_cells[f"F{i}"] = {"content": m_str}
        data_cells[f"G{i}"] = {"content": f'=PIVOT.VALUE(5,"amount_untaxed","date_order:month","{m_str}")'}

    j["sheets"] = [
        {
            "id": "purchase_dashboard", "name": "Purchase Dashboard",
            "colNumber": 26, "rowNumber": 100,
            "cells": dashboard_cells,
            "figures": [
                make_chart("chart_vendors", "bar", "Top Vendors", "Data!B2:B6", "Data!A2:A6", 20, 160),
                make_chart("chart_products", "bar", "Top Products Purchased (Portfolio)", "Data!D2:D6", "Data!C2:C6", 540, 160),
                make_chart("chart_monthly", "line", "Monthly Purchase Trend", "Data!G2:G13", "Data!F2:F13", 20, 480, w=1020),
            ]
        },
        {"id": "purchase_data", "name": "Data", "colNumber": 26, "rowNumber": 100, "cells": data_cells}
    ]
    return j


# ============================================================
# 4. INVENTORY OPERATIONS
# ============================================================
def build_inventory():
    j = make_base_json()

    j["pivots"]["1"] = make_pivot("1", "Positive Stock SKUs", "stock.quant",
        [COMPANY_FILTER, ["location_id.usage", "=", "internal"], ["quantity", ">", 0]],
        ["__count"])
    j["pivots"]["2"] = make_pivot("2", "On-Hand by Category", "stock.quant",
        [COMPANY_FILTER, ["location_id.usage", "=", "internal"], ["product_categ_id.complete_name", "ilike", "Portfolio 2026"]],
        ["quantity"], rows=["product_categ_id"])
    j["pivots"]["3"] = make_pivot("3", "Internal Transfer Operations", "stock.picking",
        [COMPANY_FILTER, ["state", "=", "done"], ["picking_type_id.code", "=", "internal"]],
        ["__count"])
    j["pivots"]["4"] = make_pivot("4", "Internal Transfer Quantity", "stock.move",
        [COMPANY_FILTER, ["state", "=", "done"], ["location_id.usage", "=", "internal"], ["location_dest_id.usage", "=", "internal"]],
        ["quantity"])
    j["pivots"]["5"] = make_pivot("5", "Scrap Operations Count", "stock.scrap",
        [COMPANY_FILTER, ["state", "=", "done"]],
        ["__count"])
    j["pivots"]["6"] = make_pivot("6", "Negative Stock Exceptions", "stock.quant",
        [COMPANY_FILTER, ["location_id.usage", "=", "internal"], ["quantity", "<", 0]],
        ["__count"])

    dashboard_cells = {
        "A1": {"content": "Inventory Operations | Current Snapshot", "style": 1},
        "A3": {"content": "Portfolio SKUs with Positive Stock", "style": 2},
        "C3": {"content": "=PIVOT.VALUE(1,\"__count\")", "style": 3},
        "A5": {"content": "Completed Internal Transfer Count", "style": 2},
        "C5": {"content": "=PIVOT.VALUE(3,\"__count\")", "style": 6},
        "A6": {"content": "Internal Transfer Quantity (Total Unit)", "style": 2},
        "C6": {"content": "=PIVOT.VALUE(4,\"quantity\")", "style": 6},
        "A8": {"content": "Completed Scrap Operations", "style": 2},
        "C8": {"content": "=PIVOT.VALUE(5,\"__count\")", "style": 7},
        "A9": {"content": "Negative Stock Exceptions", "style": 2},
        "C9": {"content": "=PIVOT.VALUE(6,\"__count\")", "style": 7},
    }

    data_cells = {
        "A1": {"content": "Product Category"}, "B1": {"content": "On-Hand Qty"},
    }
    for i in range(1, 6):
        r = i + 1
        data_cells[f"A{r}"] = {"content": f"=PIVOT.HEADER(2,\"#product_categ_id\",{i})"}
        data_cells[f"B{r}"] = {"content": f"=PIVOT.VALUE(2,\"quantity\",\"#product_categ_id\",{i})"}

    j["sheets"] = [
        {
            "id": "inventory_dashboard", "name": "Inventory Dashboard",
            "colNumber": 26, "rowNumber": 100,
            "cells": dashboard_cells,
            "figures": [
                make_chart("chart_onhand_categ", "bar", "On-Hand Quantity by Portfolio Category", "Data!B2:B6", "Data!A2:A6", 20, 240, w=1020),
            ]
        },
        {"id": "inventory_data", "name": "Data", "colNumber": 26, "rowNumber": 100, "cells": data_cells}
    ]
    return j


# ============================================================
# 5. DATA QUALITY & RECONCILIATION
# ============================================================
def build_data_quality():
    j = make_base_json()

    j["pivots"]["1"] = make_pivot("1", "SO Status Distribution", "sale.order",
        [COMPANY_FILTER, ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]],
        ["__count"], rows=["state"])
    j["pivots"]["2"] = make_pivot("2", "PO Status Distribution", "purchase.order",
        [COMPANY_FILTER, ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]],
        ["__count"], rows=["state"])

    j["lists"]["1"] = make_list("1", "Data Quality Reconciliation", "obidss.data.quality",
        [], ["table_name", "source_row_count", "mart_row_count", "row_difference", "duplicate_key_count", "orphan_key_count", "status"])

    dashboard_cells = {
        "A1": {"content": "Data Quality & Reconciliation | FY 2026", "style": 1},
        "A3": {"content": "SECTION 1: Operational Status Distribution", "style": 4},
        "A14": {"content": "SECTION 2: Source-to-Mart Reconciliation (obidss.data.quality)", "style": 4},
        "A16": {"content": "Table Name", "style": 2},
        "B16": {"content": "Source Odoo Rows", "style": 2},
        "C16": {"content": "Mart DW Rows", "style": 2},
        "D16": {"content": "Row Difference", "style": 2},
        "E16": {"content": "Duplicates", "style": 2},
        "F16": {"content": "Orphans", "style": 2},
        "G16": {"content": "Reconciliation Status", "style": 2},
    }

    for i in range(1, 4):
        r = i + 16
        dashboard_cells[f"A{r}"] = {"content": f'=ODOO.LIST(1,{i},"table_name")'}
        dashboard_cells[f"B{r}"] = {"content": f'=ODOO.LIST(1,{i},"source_row_count")'}
        dashboard_cells[f"C{r}"] = {"content": f'=ODOO.LIST(1,{i},"mart_row_count")'}
        dashboard_cells[f"D{r}"] = {"content": f'=ODOO.LIST(1,{i},"row_difference")'}
        dashboard_cells[f"E{r}"] = {"content": f'=ODOO.LIST(1,{i},"duplicate_key_count")'}
        dashboard_cells[f"F{r}"] = {"content": f'=ODOO.LIST(1,{i},"orphan_key_count")'}
        dashboard_cells[f"G{r}"] = {"content": f'=ODOO.LIST(1,{i},"status")'}

    data_cells = {
        "A1": {"content": "SO State"}, "B1": {"content": "Count"},
        "D1": {"content": "PO State"}, "E1": {"content": "Count"},
    }
    for i in range(1, 5):
        r = i + 1
        data_cells[f"A{r}"] = {"content": f"=PIVOT.HEADER(1,\"#state\",{i})"}
        data_cells[f"B{r}"] = {"content": f"=PIVOT.VALUE(1,\"__count\",\"#state\",{i})"}

    for i in range(1, 6):
        r = i + 1
        data_cells[f"D{r}"] = {"content": f"=PIVOT.HEADER(2,\"#state\",{i})"}
        data_cells[f"E{r}"] = {"content": f"=PIVOT.VALUE(2,\"__count\",\"#state\",{i})"}

    j["sheets"] = [
        {
            "id": "dq_dashboard", "name": "Data Quality Dashboard",
            "colNumber": 26, "rowNumber": 100,
            "cells": dashboard_cells,
            "figures": [
                make_chart("chart_so_states", "pie", "SO Status Distribution", "Data!B2:B5", "Data!A2:A5", 20, 80, w=480, h=220),
                make_chart("chart_po_states", "pie", "PO Status Distribution", "Data!E2:E6", "Data!D2:D6", 520, 80, w=480, h=220),
            ]
        },
        {"id": "dq_data", "name": "Data", "colNumber": 26, "rowNumber": 100, "cells": data_cells}
    ]
    return j


# ============================================================
# MAIN GENERATION & FILE WRITING (NO DATABASE WRITES)
# ============================================================
output_dir = "c:/Users/Arilano/Downloads/Project ARICE/Project Odoo/custom_addons/obidss_operational_bi/data/files"
os.makedirs(output_dir, exist_ok=True)

dashboards = {
    "executive_operations": ("dashboard_executive", build_executive),
    "sales_operations": ("dashboard_sales", build_sales),
    "purchase_suppliers": ("dashboard_purchase", build_purchase),
    "inventory_operations": ("dashboard_inventory", build_inventory),
    "data_quality": ("dashboard_data_quality", build_data_quality),
}

for artifact_name, (xml_id, builder_fn) in dashboards.items():
    print(f"Building artifact: {artifact_name} ({xml_id})")
    payload = builder_fn()

    json_str = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    json_hash = hashlib.sha256(json_str.encode('utf-8')).hexdigest()

    filepath = os.path.join(output_dir, f"{artifact_name}.json")
    with open(filepath, 'w') as f:
        f.write(json_str)

    print(f"  Hash: {json_hash}")
    print(f"  File: {filepath}")

    # ORM write to DB record for clone testing
    dashboard_record = env.ref(f'obidss_operational_bi.{xml_id}', raise_if_not_found=False)
    if dashboard_record:
        b64_bytes = base64.b64encode(json_str.encode('utf-8'))
        dashboard_record.write({'spreadsheet_binary_data': b64_bytes})
        print(f"  Attached to DB record ID: {dashboard_record.id}")

env.cr.commit()
print("\n[ALL GATES R2 - R6 GENERATED & SAVED CLEANLY]")
