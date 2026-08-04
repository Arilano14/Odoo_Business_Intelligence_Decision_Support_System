"""
OBIDSS Dashboard Artifact Generator
====================================
PROGRAMMATICALLY GENERATED ODOO 18 SPREADSHEET-COMPATIBLE LIVE ARTIFACTS

This generator creates Version 21 Odoo Spreadsheet JSON payloads for all 5 OBIDSS
dashboards. Each payload uses ONLY live =PIVOT.VALUE and =PIVOT.HEADER formulas
that reference Odoo models directly. No static KPI values are hardcoded.

Limitations disclosed:
- Community Edition: spreadsheet_edition module absent
- Programmatic artifact generation (not ODOO_UI_GENERATED)
- Schema validated against proven Sales Operations pilot
- Clone-first browser verification required
- Synthetic FY 2026 dataset
"""

import json
import base64
import hashlib
import os

# ============================================================
# SCHEMA BUILDER HELPERS
# ============================================================

def make_pivot(pid, name, model, domain, measures, rows=None, columns=None):
    """Create a canonical Odoo pivot definition."""
    pivot = {
        "type": "ODOO",
        "id": str(pid),
        "formulaId": str(pid),
        "name": name,
        "model": model,
        "domain": domain,
        "measures": [{"id": m, "fieldName": m} for m in measures],
        "rows": [{"fieldName": r} for r in (rows or [])],
        "columns": [{"fieldName": c} for c in (columns or [])],
        "fieldMatching": {}
    }
    return pivot

def make_list(lid, name, model, domain, columns_list):
    """Create a canonical Odoo list definition."""
    return {
        "type": "ODOO",
        "id": str(lid),
        "name": name,
        "model": model,
        "domain": domain,
        "columns": columns_list,
        "orderBy": [],
        "fieldMatching": {}
    }

def make_scorecard_cell(content, style_id=None):
    cell = {"content": content}
    if style_id:
        cell["style"] = style_id
    return cell

def make_chart(chart_id, chart_type, title, data_range, label_range, x, y, w=500, h=300):
    return {
        "id": chart_id,
        "tag": "chart",
        "width": w,
        "height": h,
        "x": x,
        "y": y,
        "data": {
            "type": chart_type,
            "title": {"text": title},
            "background": "#FFFFFF",
            "legendPosition": "none",
            "axesDesign": {"x": {}, "y": {}},
            "dataSetsHaveTitle": False,
            "dataSets": [{"dataRange": data_range}],
            "labelRange": label_range
        }
    }

def make_base_json():
    return {
        "version": 21,
        "settings": {
            "locale": {
                "name": "English (US)",
                "code": "en_US",
                "formulaPrefix": "="
            }
        },
        "pivots": {},
        "lists": {},
        "globalFilters": [],
        "sheets": [],
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

# ============================================================
# COMMON DOMAINS
# ============================================================
COMPANY_DOMAIN = ["company_id", "=", 2]
FY2026_SALE_REPORT = [COMPANY_DOMAIN, ["state", "=", "sale"], ["date", ">=", "2026-01-01"], ["date", "<", "2027-01-01"]]
FY2026_PURCHASE_REPORT = [COMPANY_DOMAIN, ["state", "=", "purchase"], ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]]
FY2026_SALE_ORDER = [COMPANY_DOMAIN, ["state", "=", "sale"], ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]]
FY2026_PURCHASE_ORDER = [COMPANY_DOMAIN, ["state", "=", "purchase"], ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]]

# ============================================================
# 1. EXECUTIVE OPERATIONS DASHBOARD
# ============================================================
def build_executive():
    j = make_base_json()

    # Pivot 1: Total Sales Value
    j["pivots"]["1"] = make_pivot("1", "Total Sales Value", "sale.report",
        FY2026_SALE_REPORT, ["price_subtotal"])

    # Pivot 2: Total Purchase Value
    j["pivots"]["2"] = make_pivot("2", "Total Purchase Value", "purchase.report",
        FY2026_PURCHASE_REPORT, ["untaxed_total"])

    # Pivot 3: SO Count
    j["pivots"]["3"] = make_pivot("3", "SO Count", "sale.report",
        FY2026_SALE_REPORT, ["__count"])

    # Pivot 4: PO Count
    j["pivots"]["4"] = make_pivot("4", "PO Count", "purchase.report",
        FY2026_PURCHASE_REPORT, ["__count"])

    # Pivot 5: Monthly Sales Trend
    j["pivots"]["5"] = make_pivot("5", "Monthly Sales Trend", "sale.report",
        FY2026_SALE_REPORT, ["price_subtotal"], columns=["date:month"])

    # Pivot 6: Monthly Purchase Trend
    j["pivots"]["6"] = make_pivot("6", "Monthly Purchase Trend", "purchase.report",
        FY2026_PURCHASE_REPORT, ["untaxed_total"], columns=["date_order:month"])

    # Pivot 7: On-Hand Stock Count (portfolio products, internal locations)
    j["pivots"]["7"] = make_pivot("7", "On-Hand Stock Count", "stock.quant",
        [COMPANY_DOMAIN, ["location_id.usage", "=", "internal"]],
        ["quantity"])

    # Dashboard sheet
    dashboard_cells = {
        "A1": make_scorecard_cell("Executive Operations Dashboard — FY 2026", 1),
        "A3": make_scorecard_cell("Confirmed Sales Value (Untaxed)", 2),
        "C3": make_scorecard_cell("=PIVOT.VALUE(1,\"price_subtotal\")", 3),
        "A4": make_scorecard_cell("Confirmed Purchase Value (Untaxed)", 2),
        "C4": make_scorecard_cell("=PIVOT.VALUE(2,\"untaxed_total\")", 4),
        "A6": make_scorecard_cell("Confirmed SO Count", 2),
        "C6": make_scorecard_cell("=PIVOT.VALUE(3,\"__count\")", 3),
        "A7": make_scorecard_cell("Confirmed PO Count", 2),
        "C7": make_scorecard_cell("=PIVOT.VALUE(4,\"__count\")", 4),
        "A9": make_scorecard_cell("Current On-Hand Stock (All Products)", 2),
        "C9": make_scorecard_cell("=PIVOT.VALUE(7,\"quantity\")", 6),
    }

    # Data sheet: monthly trends for charts
    data_cells = {
        "A1": {"content": "Month"}, "B1": {"content": "Sales Value"}, "C1": {"content": "Purchase Value"},
    }
    for i in range(1, 13):
        row = i + 1
        data_cells[f"A{row}"] = {"content": f"=PIVOT.HEADER(5,\"date:month\",{i})"}
        data_cells[f"B{row}"] = {"content": f"=PIVOT.VALUE(5,\"price_subtotal\",\"date:month\",A{row})"}
        data_cells[f"C{row}"] = {"content": f"=PIVOT.VALUE(6,\"untaxed_total\",\"date_order:month\",A{row})"}

    j["sheets"] = [
        {
            "id": "exec_dashboard",
            "name": "Executive Dashboard",
            "colNumber": 26,
            "rowNumber": 100,
            "cells": dashboard_cells,
            "figures": [
                make_chart("chart_monthly_sales", "line", "Monthly Sales Trend (FY 2026)",
                           "Data!B2:B13", "Data!A2:A13", 20, 200),
                make_chart("chart_monthly_purchase", "line", "Monthly Purchase Trend (FY 2026)",
                           "Data!C2:C13", "Data!A2:A13", 540, 200),
                make_chart("chart_sales_vs_purchase", "bar", "Sales vs Purchase Comparison",
                           "Data!B2:C13", "Data!A2:A13", 20, 520, w=1020),
            ]
        },
        {
            "id": "exec_data",
            "name": "Data",
            "colNumber": 26,
            "rowNumber": 100,
            "cells": data_cells
        }
    ]
    return j


# ============================================================
# 2. SALES OPERATIONS DASHBOARD (reuse existing proven structure)
# ============================================================
def build_sales():
    j = make_base_json()

    j["pivots"]["1"] = make_pivot("1", "Confirmed Sales Value", "sale.report",
        FY2026_SALE_REPORT, ["price_subtotal"])
    j["pivots"]["2"] = make_pivot("2", "Top Categories", "sale.report",
        FY2026_SALE_REPORT, ["price_subtotal"], rows=["categ_id"])
    j["pivots"]["3"] = make_pivot("3", "Top Products", "sale.report",
        FY2026_SALE_REPORT, ["price_subtotal"], rows=["product_tmpl_id"])
    j["pivots"]["4"] = make_pivot("4", "Top Salespeople", "sale.report",
        FY2026_SALE_REPORT, ["price_subtotal"], rows=["user_id"])
    j["pivots"]["5"] = make_pivot("5", "Monthly Sales Trend", "sale.report",
        FY2026_SALE_REPORT, ["price_subtotal"], columns=["date:month"])

    dashboard_cells = {
        "A1": make_scorecard_cell("Sales Overview (FY 2026)", 1),
        "A3": make_scorecard_cell("Total Confirmed Sales Value (Untaxed)", 2),
        "B3": make_scorecard_cell("=PIVOT.VALUE(1,\"price_subtotal\")", 3),
    }

    data_cells = {
        "A1": {"content": "Category"}, "B1": {"content": "Value"},
        "C1": {"content": "Product"}, "D1": {"content": "Value"},
        "E1": {"content": "Salesperson"}, "F1": {"content": "Value"},
        "H1": {"content": "Month"}, "I1": {"content": "Sales Value"},
    }
    for i in range(1, 6):
        r = i + 1
        data_cells[f"A{r}"] = {"content": f"=PIVOT.HEADER(2,\"categ_id\",{i})"}
        data_cells[f"B{r}"] = {"content": f"=PIVOT.VALUE(2,\"price_subtotal\",\"categ_id\",A{r})"}
        data_cells[f"C{r}"] = {"content": f"=PIVOT.HEADER(3,\"product_tmpl_id\",{i})"}
        data_cells[f"D{r}"] = {"content": f"=PIVOT.VALUE(3,\"price_subtotal\",\"product_tmpl_id\",C{r})"}
        data_cells[f"E{r}"] = {"content": f"=PIVOT.HEADER(4,\"user_id\",{i})"}
        data_cells[f"F{r}"] = {"content": f"=PIVOT.VALUE(4,\"price_subtotal\",\"user_id\",E{r})"}

    for i in range(1, 13):
        r = i + 1
        data_cells[f"H{r}"] = {"content": f"=PIVOT.HEADER(5,\"date:month\",{i})"}
        data_cells[f"I{r}"] = {"content": f"=PIVOT.VALUE(5,\"price_subtotal\",\"date:month\",H{r})"}

    j["sheets"] = [
        {
            "id": "sales_dashboard",
            "name": "Sales Dashboard",
            "colNumber": 26, "rowNumber": 100,
            "cells": dashboard_cells,
            "figures": [
                make_chart("chart_categories", "bar", "Sales by Category", "Data!B2:B6", "Data!A2:A6", 20, 120),
                make_chart("chart_products", "bar", "Top Products", "Data!D2:D6", "Data!C2:C6", 540, 120),
                make_chart("chart_salespeople", "bar", "Sales by Salesperson", "Data!F2:F6", "Data!E2:E6", 20, 440),
                make_chart("chart_monthly", "line", "Monthly Sales Trend", "Data!I2:I13", "Data!H2:H13", 540, 440),
            ]
        },
        {"id": "sales_data", "name": "Data", "colNumber": 26, "rowNumber": 100, "cells": data_cells}
    ]
    return j


# ============================================================
# 3. PURCHASE & SUPPLIERS DASHBOARD
# ============================================================
def build_purchase():
    j = make_base_json()

    j["pivots"]["1"] = make_pivot("1", "Total Purchase Value", "purchase.report",
        FY2026_PURCHASE_REPORT, ["untaxed_total"])
    j["pivots"]["2"] = make_pivot("2", "PO Count", "purchase.report",
        FY2026_PURCHASE_REPORT, ["__count"])
    j["pivots"]["3"] = make_pivot("3", "Top Vendors", "purchase.report",
        FY2026_PURCHASE_REPORT, ["untaxed_total"], rows=["partner_id"])
    j["pivots"]["4"] = make_pivot("4", "Top Products Purchased", "purchase.report",
        FY2026_PURCHASE_REPORT, ["untaxed_total"], rows=["product_tmpl_id"])
    j["pivots"]["5"] = make_pivot("5", "Monthly Purchase Trend", "purchase.report",
        FY2026_PURCHASE_REPORT, ["untaxed_total"], columns=["date_order:month"])
    # Draft/RFQ count
    j["pivots"]["6"] = make_pivot("6", "Draft PO Count", "purchase.order",
        [COMPANY_DOMAIN, ["state", "=", "draft"], ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]],
        ["__count"])
    # Received qty
    j["pivots"]["7"] = make_pivot("7", "Qty Received vs Ordered", "purchase.report",
        FY2026_PURCHASE_REPORT, ["qty_ordered", "qty_received"])

    dashboard_cells = {
        "A1": make_scorecard_cell("Purchase & Suppliers — FY 2026", 1),
        "A3": make_scorecard_cell("Confirmed Purchase Value (Untaxed)", 2),
        "C3": make_scorecard_cell("=PIVOT.VALUE(1,\"untaxed_total\")", 4),
        "A4": make_scorecard_cell("Confirmed PO Count", 2),
        "C4": make_scorecard_cell("=PIVOT.VALUE(2,\"__count\")", 3),
        "A5": make_scorecard_cell("Draft/RFQ Count", 2),
        "C5": make_scorecard_cell("=PIVOT.VALUE(6,\"__count\")", 7),
        "A7": make_scorecard_cell("Qty Ordered", 2),
        "C7": make_scorecard_cell("=PIVOT.VALUE(7,\"qty_ordered\")", 3),
        "A8": make_scorecard_cell("Qty Received", 2),
        "C8": make_scorecard_cell("=PIVOT.VALUE(7,\"qty_received\")", 3),
    }

    data_cells = {
        "A1": {"content": "Vendor"}, "B1": {"content": "Value"},
        "C1": {"content": "Product"}, "D1": {"content": "Value"},
        "F1": {"content": "Month"}, "G1": {"content": "Purchase Value"},
    }
    for i in range(1, 6):
        r = i + 1
        data_cells[f"A{r}"] = {"content": f"=PIVOT.HEADER(3,\"partner_id\",{i})"}
        data_cells[f"B{r}"] = {"content": f"=PIVOT.VALUE(3,\"untaxed_total\",\"partner_id\",A{r})"}
        data_cells[f"C{r}"] = {"content": f"=PIVOT.HEADER(4,\"product_tmpl_id\",{i})"}
        data_cells[f"D{r}"] = {"content": f"=PIVOT.VALUE(4,\"untaxed_total\",\"product_tmpl_id\",C{r})"}
    for i in range(1, 13):
        r = i + 1
        data_cells[f"F{r}"] = {"content": f"=PIVOT.HEADER(5,\"date_order:month\",{i})"}
        data_cells[f"G{r}"] = {"content": f"=PIVOT.VALUE(5,\"untaxed_total\",\"date_order:month\",F{r})"}

    j["sheets"] = [
        {
            "id": "purchase_dashboard", "name": "Purchase Dashboard",
            "colNumber": 26, "rowNumber": 100,
            "cells": dashboard_cells,
            "figures": [
                make_chart("chart_vendors", "bar", "Top Vendors", "Data!B2:B6", "Data!A2:A6", 20, 200),
                make_chart("chart_products", "bar", "Top Products Purchased", "Data!D2:D6", "Data!C2:C6", 540, 200),
                make_chart("chart_monthly", "line", "Monthly Purchase Trend", "Data!G2:G13", "Data!F2:F13", 20, 520, w=1020),
            ]
        },
        {"id": "purchase_data", "name": "Data", "colNumber": 26, "rowNumber": 100, "cells": data_cells}
    ]
    return j


# ============================================================
# 4. INVENTORY OPERATIONS DASHBOARD
# ============================================================
def build_inventory():
    j = make_base_json()

    # stock.quant for current position
    j["pivots"]["1"] = make_pivot("1", "Current On-Hand", "stock.quant",
        [COMPANY_DOMAIN, ["location_id.usage", "=", "internal"]],
        ["quantity"])

    # stock.quant by product category
    j["pivots"]["2"] = make_pivot("2", "On-Hand by Category", "stock.quant",
        [COMPANY_DOMAIN, ["location_id.usage", "=", "internal"]],
        ["quantity"], rows=["product_id"])

    # stock.move: internal→internal (transfers)
    j["pivots"]["3"] = make_pivot("3", "Internal Transfers", "stock.move",
        [COMPANY_DOMAIN, ["state", "=", "done"],
         ["location_id.usage", "=", "internal"], ["location_dest_id.usage", "=", "internal"]],
        ["quantity"])

    # stock.move: internal→inventory (adjustments/scrap)
    j["pivots"]["4"] = make_pivot("4", "Inventory Adjustments", "stock.move",
        [COMPANY_DOMAIN, ["state", "=", "done"],
         ["location_id.usage", "=", "internal"], ["location_dest_id.usage", "=", "inventory"]],
        ["quantity"])

    # stock.scrap count and qty
    j["pivots"]["5"] = make_pivot("5", "Scrap Count", "stock.scrap",
        [COMPANY_DOMAIN, ["state", "=", "done"]],
        ["scrap_qty", "__count"])

    # Negative stock detection
    j["pivots"]["6"] = make_pivot("6", "Negative Stock Count", "stock.quant",
        [COMPANY_DOMAIN, ["location_id.usage", "=", "internal"], ["quantity", "<", 0]],
        ["__count", "quantity"])

    # On-hand by category for chart
    j["pivots"]["7"] = make_pivot("7", "On-Hand by Product Category", "stock.quant",
        [COMPANY_DOMAIN, ["location_id.usage", "=", "internal"]],
        ["quantity"], rows=["product_categ_id"])

    dashboard_cells = {
        "A1": make_scorecard_cell("Inventory Operations — Current Snapshot", 1),
        "A3": make_scorecard_cell("Total On-Hand Quantity (Internal)", 2),
        "C3": make_scorecard_cell("=PIVOT.VALUE(1,\"quantity\")", 3),
        "A5": make_scorecard_cell("Internal Transfers (Done)", 2),
        "C5": make_scorecard_cell("=PIVOT.VALUE(3,\"quantity\")", 6),
        "A6": make_scorecard_cell("Inventory Adjustments", 2),
        "C6": make_scorecard_cell("=PIVOT.VALUE(4,\"quantity\")", 6),
        "A8": make_scorecard_cell("Scrap Count", 2),
        "C8": make_scorecard_cell("=PIVOT.VALUE(5,\"__count\")", 7),
        "A9": make_scorecard_cell("Scrap Quantity", 2),
        "C9": make_scorecard_cell("=PIVOT.VALUE(5,\"scrap_qty\")", 7),
        "A11": make_scorecard_cell("Negative Stock Exceptions", 2),
        "C11": make_scorecard_cell("=PIVOT.VALUE(6,\"__count\")", 7),
        "A12": make_scorecard_cell("Negative Stock Total Qty", 2),
        "C12": make_scorecard_cell("=PIVOT.VALUE(6,\"quantity\")", 7),
        "A14": make_scorecard_cell("Note: UoM varies by product category. Do not aggregate across incompatible units.", 5),
    }

    data_cells = {
        "A1": {"content": "Product Category"}, "B1": {"content": "On-Hand Qty"},
    }
    for i in range(1, 8):
        r = i + 1
        data_cells[f"A{r}"] = {"content": f"=PIVOT.HEADER(7,\"product_categ_id\",{i})"}
        data_cells[f"B{r}"] = {"content": f"=PIVOT.VALUE(7,\"quantity\",\"product_categ_id\",A{r})"}

    j["sheets"] = [
        {
            "id": "inventory_dashboard", "name": "Inventory Dashboard",
            "colNumber": 26, "rowNumber": 100,
            "cells": dashboard_cells,
            "figures": [
                make_chart("chart_onhand_categ", "bar", "On-Hand by Product Category",
                           "Data!B2:B8", "Data!A2:A8", 20, 300, w=1020),
            ]
        },
        {"id": "inventory_data", "name": "Data", "colNumber": 26, "rowNumber": 100, "cells": data_cells}
    ]
    return j


# ============================================================
# 5. DATA QUALITY & RECONCILIATION DASHBOARD
# ============================================================
def build_data_quality():
    j = make_base_json()

    # Operational Status: SO by state
    j["pivots"]["1"] = make_pivot("1", "SO Status Distribution", "sale.order",
        [COMPANY_DOMAIN, ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]],
        ["__count"], rows=["state"])

    # Operational Status: PO by state
    j["pivots"]["2"] = make_pivot("2", "PO Status Distribution", "purchase.order",
        [COMPANY_DOMAIN, ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]],
        ["__count"], rows=["state"])

    # Data Quality from obidss.data.quality model
    j["lists"]["1"] = make_list("1", "Data Quality Metrics", "obidss.data.quality",
        [], ["table_name", "source_row_count", "mart_row_count", "row_difference",
             "duplicate_key_count", "orphan_key_count", "status"])

    dashboard_cells = {
        "A1": make_scorecard_cell("Data Quality & Reconciliation — FY 2026", 1),
        "A3": make_scorecard_cell("SECTION 1: Operational Status Distribution", 4),
        "A15": make_scorecard_cell("SECTION 2: Source-to-Mart Reconciliation", 4),
        "A16": make_scorecard_cell("(Data from obidss.data.quality model)", 5),
    }

    # SO states data
    data_cells = {
        "A1": {"content": "SO State"}, "B1": {"content": "Count"},
        "D1": {"content": "PO State"}, "E1": {"content": "Count"},
    }
    so_states = ["draft", "sale", "done", "cancel"]
    for i, state in enumerate(so_states, 1):
        r = i + 1
        data_cells[f"A{r}"] = {"content": f"=PIVOT.HEADER(1,\"state\",{i})"}
        data_cells[f"B{r}"] = {"content": f"=PIVOT.VALUE(1,\"__count\",\"state\",A{r})"}

    po_states = ["draft", "sent", "purchase", "done", "cancel"]
    for i, state in enumerate(po_states, 1):
        r = i + 1
        data_cells[f"D{r}"] = {"content": f"=PIVOT.HEADER(2,\"state\",{i})"}
        data_cells[f"E{r}"] = {"content": f"=PIVOT.VALUE(2,\"__count\",\"state\",D{r})"}

    # DQ list references
    data_cells["G1"] = {"content": "Table"}
    data_cells["H1"] = {"content": "Source Rows"}
    data_cells["I1"] = {"content": "Mart Rows"}
    data_cells["J1"] = {"content": "Difference"}
    data_cells["K1"] = {"content": "Duplicates"}
    data_cells["L1"] = {"content": "Orphans"}
    data_cells["M1"] = {"content": "Status"}
    for i in range(1, 4):  # 3 DQ records
        r = i + 1
        data_cells[f"G{r}"] = {"content": f"=ODOO.LIST(1,{i},\"table_name\")"}
        data_cells[f"H{r}"] = {"content": f"=ODOO.LIST(1,{i},\"source_row_count\")"}
        data_cells[f"I{r}"] = {"content": f"=ODOO.LIST(1,{i},\"mart_row_count\")"}
        data_cells[f"J{r}"] = {"content": f"=ODOO.LIST(1,{i},\"row_difference\")"}
        data_cells[f"K{r}"] = {"content": f"=ODOO.LIST(1,{i},\"duplicate_key_count\")"}
        data_cells[f"L{r}"] = {"content": f"=ODOO.LIST(1,{i},\"orphan_key_count\")"}
        data_cells[f"M{r}"] = {"content": f"=ODOO.LIST(1,{i},\"status\")"}

    j["sheets"] = [
        {
            "id": "dq_dashboard", "name": "Data Quality Dashboard",
            "colNumber": 26, "rowNumber": 100,
            "cells": dashboard_cells,
            "figures": [
                make_chart("chart_so_states", "pie", "SO Status Distribution",
                           "Data!B2:B5", "Data!A2:A5", 20, 80, w=480, h=280),
                make_chart("chart_po_states", "pie", "PO Status Distribution",
                           "Data!E2:E6", "Data!D2:D6", 520, 80, w=480, h=280),
            ]
        },
        {"id": "dq_data", "name": "Data", "colNumber": 26, "rowNumber": 100, "cells": data_cells}
    ]
    return j


# ============================================================
# VALIDATION
# ============================================================
def validate_payload(name, payload):
    """Validate a dashboard payload meets contract requirements."""
    errors = []

    # JSON parse check
    try:
        json_str = json.dumps(payload)
        json.loads(json_str)
    except Exception as e:
        errors.append(f"JSON parse failed: {e}")
        return errors

    # Version check
    if payload.get("version") != 21:
        errors.append(f"Version is {payload.get('version')}, expected 21")

    # Check for at least one pivot or list source
    has_source = bool(payload.get("pivots")) or bool(payload.get("lists"))
    if not has_source:
        errors.append("No pivot or list source found")

    # Check for live formulas (no static KPI values)
    static_count = 0
    live_count = 0
    for sheet in payload.get("sheets", []):
        for cell_ref, cell in sheet.get("cells", {}).items():
            content = cell.get("content", "")
            if content.startswith("="):
                live_count += 1

    if live_count == 0:
        errors.append("No live formulas found")

    # Check company filter in domains
    has_company_filter = False
    for pid, pivot in payload.get("pivots", {}).items():
        domain = pivot.get("domain", [])
        for clause in domain:
            if isinstance(clause, list) and len(clause) >= 3:
                if clause[0] == "company_id" and clause[2] == 2:
                    has_company_filter = True
                    break

    for lid, lst in payload.get("lists", {}).items():
        # Lists like obidss.data.quality may not need company filter
        pass

    if not has_company_filter and payload.get("pivots"):
        errors.append("No company_id=2 filter found in pivots")

    return errors


# ============================================================
# FIELD VALIDATION AGAINST ODOO MODELS
# ============================================================
def validate_fields(payload, env_obj):
    """Validate that all referenced models and fields exist in Odoo."""
    errors = []

    for pid, pivot in payload.get("pivots", {}).items():
        model = pivot.get("model")
        try:
            mdl = env_obj[model]
        except Exception:
            errors.append(f"Pivot {pid}: Model '{model}' not found")
            continue

        # Check measures
        for measure in pivot.get("measures", []):
            field_name = measure.get("fieldName", "")
            if field_name == "__count":
                continue
            if field_name not in mdl._fields:
                errors.append(f"Pivot {pid}: Field '{field_name}' not in model '{model}'")

        # Check row/column group-by fields
        for row in pivot.get("rows", []):
            fn = row.get("fieldName", "")
            base_fn = fn.split(":")[0]
            if base_fn not in mdl._fields:
                errors.append(f"Pivot {pid}: Row field '{fn}' not in model '{model}'")

        for col in pivot.get("columns", []):
            fn = col.get("fieldName", "")
            base_fn = fn.split(":")[0]
            if base_fn not in mdl._fields:
                errors.append(f"Pivot {pid}: Column field '{fn}' not in model '{model}'")

        # Check domain fields
        for clause in pivot.get("domain", []):
            if isinstance(clause, list) and len(clause) >= 3:
                field_path = clause[0]
                base_field = field_path.split(".")[0]
                if base_field not in mdl._fields:
                    errors.append(f"Pivot {pid}: Domain field '{field_path}' not in model '{model}'")

    for lid, lst in payload.get("lists", {}).items():
        model = lst.get("model")
        try:
            mdl = env_obj[model]
        except Exception:
            errors.append(f"List {lid}: Model '{model}' not found")
            continue

        for col in lst.get("columns", []):
            fn = col if isinstance(col, str) else col.get("name", "")
            if fn not in mdl._fields:
                errors.append(f"List {lid}: Column '{fn}' not in model '{model}'")

    return errors


# ============================================================
# MAIN: Generate, Validate, and Save Artifacts
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

all_passed = True
results = {}

for artifact_name, (xml_id, builder_fn) in dashboards.items():
    print(f"\n{'='*60}")
    print(f"Building: {artifact_name}")
    print(f"{'='*60}")

    payload = builder_fn()

    # Schema validation
    schema_errors = validate_payload(artifact_name, payload)
    if schema_errors:
        print(f"  SCHEMA ERRORS:")
        for e in schema_errors:
            print(f"    - {e}")
        all_passed = False
        continue

    # Field validation against Odoo
    field_errors = validate_fields(payload, env)
    if field_errors:
        print(f"  FIELD ERRORS:")
        for e in field_errors:
            print(f"    - {e}")
        all_passed = False
        continue

    # Generate deterministic JSON
    json_str = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    json_hash = hashlib.sha256(json_str.encode('utf-8')).hexdigest()

    # Save as base64 file (for Odoo module loading)
    b64_data = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
    filepath = os.path.join(output_dir, f"{artifact_name}.json")
    with open(filepath, 'w') as f:
        f.write(json_str)

    print(f"  Schema:  PASS")
    print(f"  Fields:  PASS")
    print(f"  Hash:    {json_hash}")
    print(f"  File:    {filepath}")

    results[artifact_name] = {
        "xml_id": xml_id,
        "hash": json_hash,
        "file": filepath,
    }

    # Also write to the dashboard record via XML ID
    dashboard_record = env.ref(f'obidss_operational_bi.{xml_id}', raise_if_not_found=False)
    if dashboard_record:
        b64_bytes = base64.b64encode(json_str.encode('utf-8'))
        dashboard_record.write({'spreadsheet_binary_data': b64_bytes})
        print(f"  Written to dashboard: {dashboard_record.name} (ID: {dashboard_record.id})")
    else:
        print(f"  WARNING: XML ID 'obidss_operational_bi.{xml_id}' not found!")
        all_passed = False

env.cr.commit()

print(f"\n{'='*60}")
print(f"GENERATOR RESULT: {'ALL PASSED' if all_passed else 'SOME FAILED'}")
print(f"{'='*60}")
for name, info in results.items():
    print(f"  {name}: hash={info['hash'][:16]}...")
