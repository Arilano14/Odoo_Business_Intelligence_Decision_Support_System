"""
Phase 9 Scenario Configuration Module.

Centralized configuration constants, contracts, and parameters for Phase 9:
Operational Transaction Generation for PT Prima Alat Nusantara (FY 2026).
"""

SEED = 26072026
BATCH_PREFIX = "PORTFOLIO_2026_V1"
COMPANY_NAME = "PT Prima Alat Nusantara"
WAREHOUSE_CODE = "PAN"
SCENARIO_YEAR = 2026
SCENARIO_AS_OF_DATE = "2026-12-31"

# Monthly targets for SO and PO
MONTHLY_TARGETS = {
    1:  {'so': 60, 'po': 18, 'phase': 'Baseline'},
    2:  {'so': 58, 'po': 18, 'phase': 'Baseline'},
    3:  {'so': 48, 'po': 15, 'phase': 'Disruption'},
    4:  {'so': 55, 'po': 32, 'phase': 'Procurement Response'},
    5:  {'so': 60, 'po': 28, 'phase': 'Accumulation'},
    6:  {'so': 62, 'po': 20, 'phase': 'Correction'},
    7:  {'so': 63, 'po': 18, 'phase': 'Correction'},
    8:  {'so': 64, 'po': 17, 'phase': 'Correction'},
    9:  {'so': 61, 'po': 18, 'phase': 'Correction'},
    10: {'so': 62, 'po': 18, 'phase': 'Stabilization'},
    11: {'so': 63, 'po': 18, 'phase': 'Stabilization'},
    12: {'so': 64, 'po': 20, 'phase': 'Stabilization'},
}

TOTAL_SO_TARGET = 720
TOTAL_PO_TARGET = 240
TOTAL_TRANSFERS_TARGET = 24
TOTAL_SCRAP_TARGET = 12

# Customer segment rules (48 total customers)
CUSTOMER_SEGMENTS = {
    'Strategic':  {'count': 8,  'min_orders': 36, 'max_orders': 54},
    'Regular':    {'count': 16, 'min_orders': 12, 'max_orders': 24},
    'Occasional': {'count': 14, 'min_orders': 3,  'max_orders': 8},
    'One-time':   {'count': 10, 'min_orders': 1,  'max_orders': 1},
}

# Supplier segment rules (24 total suppliers)
SUPPLIER_SEGMENTS = {
    'Strategic':  {'count': 5,  'min_pos': 24, 'max_pos': 36},
    'Regular':    {'count': 10, 'min_pos': 6,  'max_pos': 14},
    'Backup':     {'count': 6,  'min_pos': 2,  'max_pos': 6},
    'Occasional': {'count': 3,  'min_pos': 1,  'max_pos': 3},
}

# Quantity bounds per category for SO line items
SO_CATEGORY_QTY_BOUNDS = {
    'Heavy Equipment': (1, 2),
    'Engine and Hydraulic Parts': (1, 5),
    'Undercarriage Parts': (1, 8),
    'Filters and Maintenance Parts': (2, 30),
    'Consumables': (5, 80),
}

# Quantity bounds per category for PO line items
PO_CATEGORY_QTY_BOUNDS = {
    'Heavy Equipment': (1, 2),
    'Engine and Hydraulic Parts': (2, 12),
    'Undercarriage Parts': (4, 20),
    'Filters and Maintenance Parts': (20, 120),
    'Consumables': (50, 300),
}

# Reference patterns
REF_PATTERNS = {
    'sale.order': f"{BATCH_PREFIX}-SO-{{:04d}}",
    'purchase.order': f"{BATCH_PREFIX}-PO-{{:04d}}",
    'account.move.invoice': f"{BATCH_PREFIX}-INV-{{:04d}}",
    'account.move.bill': f"{BATCH_PREFIX}-BILL-{{:04d}}",
    'stock.picking.internal': f"{BATCH_PREFIX}-INT-{{:02d}}",
    'stock.scrap': f"{BATCH_PREFIX}-SCRAP-{{:02d}}",
}
