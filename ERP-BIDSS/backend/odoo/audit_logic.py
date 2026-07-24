import os
from .connection import get_connection

def run_audit():
    try:
        uid, models, db, password = get_connection()
    except Exception as e:
        print(f"Failed to connect to Odoo: {e}")
        return

    # Identify candidate records
    customers = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
        [[('ref', '=like', 'BIDSS-CUST-%')]],
        {'fields': ['id', 'name', 'ref']})
    
    suppliers = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
        [[('ref', '=like', 'BIDSS-VEND-%')]],
        {'fields': ['id', 'name', 'ref']})

    products = models.execute_kw(db, uid, password, 'product.product', 'search_read',
        [[('default_code', '=like', 'BIDSS-HE-%')]], # Using BIDSS-HE as an example, will also look for generic ones
        {'fields': ['id', 'name', 'default_code']})

    sales = models.execute_kw(db, uid, password, 'sale.order', 'search_read',
        [[]], # We will likely wipe ALL sales since it's a dummy DB, or just 2024/2026. Let's find 2024/2026.
        {'fields': ['id', 'name', 'date_order', 'state']})
    
    # Filter sales by 2024 and 2026
    portfolio_sales = [s for s in sales if s['date_order'] and (s['date_order'].startswith('2024') or s['date_order'].startswith('2026'))]

    purchases = models.execute_kw(db, uid, password, 'purchase.order', 'search_read',
        [[]],
        {'fields': ['id', 'name', 'date_order', 'state']})
    portfolio_purchases = [p for p in purchases if p['date_order'] and (p['date_order'].startswith('2024') or p['date_order'].startswith('2026'))]

    pickings = models.execute_kw(db, uid, password, 'stock.picking', 'search_read',
        [[]],
        {'fields': ['id', 'name', 'date', 'state']})
    portfolio_pickings = [p for p in pickings if p['date'] and (p['date'].startswith('2024') or p['date'].startswith('2026'))]
    
    invoices = models.execute_kw(db, uid, password, 'account.move', 'search_read',
        [[('move_type', 'in', ['out_invoice', 'in_invoice'])]],
        {'fields': ['id', 'name', 'date', 'state']})
    portfolio_invoices = [i for i in invoices if i['date'] and (i['date'].startswith('2024') or i['date'].startswith('2026'))]

    manifest_path = os.path.join("..", "..", "docs", "phase8", "cleanup_candidate_manifest.md")
    with open(manifest_path, "w") as f:
        f.write("# Phase 8 Cleanup Candidate Manifest\n\n")
        f.write("The following records are identified as synthetic portfolio data and are candidates for deletion.\n\n")
        
        f.write(f"## 1. Customers ({len(customers)})\n")
        for c in customers[:5]:
            f.write(f"- ID: {c['id']}, Name: {c['name']}, Ref: {c['ref']}\n")
        if len(customers) > 5: f.write(f"- ... and {len(customers)-5} more\n\n")

        f.write(f"## 2. Suppliers ({len(suppliers)})\n")
        for s in suppliers[:5]:
            f.write(f"- ID: {s['id']}, Name: {s['name']}, Ref: {s['ref']}\n")
        if len(suppliers) > 5: f.write(f"- ... and {len(suppliers)-5} more\n\n")
        
        f.write(f"## 3. Products ({len(products)})\n")
        for p in products[:5]:
            f.write(f"- ID: {p['id']}, Name: {p['name']}, SKU: {p['default_code']}\n")
        if len(products) > 5: f.write(f"- ... and {len(products)-5} more\n\n")
        
        f.write(f"## 4. Sales Orders ({len(portfolio_sales)})\n")
        for s in portfolio_sales[:5]:
            f.write(f"- ID: {s['id']}, Ref: {s['name']}, Date: {s['date_order']}, State: {s['state']}\n")
        if len(portfolio_sales) > 5: f.write(f"- ... and {len(portfolio_sales)-5} more\n\n")
        
        f.write(f"## 5. Purchase Orders ({len(portfolio_purchases)})\n")
        for p in portfolio_purchases[:5]:
            f.write(f"- ID: {p['id']}, Ref: {p['name']}, Date: {p['date_order']}, State: {p['state']}\n")
        if len(portfolio_purchases) > 5: f.write(f"- ... and {len(portfolio_purchases)-5} more\n\n")

        f.write(f"## 6. Stock Pickings ({len(portfolio_pickings)})\n")
        for p in portfolio_pickings[:5]:
            f.write(f"- ID: {p['id']}, Ref: {p['name']}, Date: {p['date']}, State: {p['state']}\n")
        if len(portfolio_pickings) > 5: f.write(f"- ... and {len(portfolio_pickings)-5} more\n\n")

        f.write(f"## 7. Account Moves (Invoices/Bills) ({len(portfolio_invoices)})\n")
        for i in portfolio_invoices[:5]:
            f.write(f"- ID: {i['id']}, Ref: {i['name']}, Date: {i['date']}, State: {i['state']}\n")
        if len(portfolio_invoices) > 5: f.write(f"- ... and {len(portfolio_invoices)-5} more\n\n")

        f.write("## 8. Dashboard Issues\n")
        f.write("- Found 1 dangling reference in `ir_act_client` (ID: 348, tag: action_spreadsheet_dashboard). Needs manual review if it explicitly opens dashboard 11.\n")
        f.write("- Sale order 19 missing references need to be cleaned up in `ir_filters` or UI if any exist.\n")

    print(f"[OK] Audit complete. Manifest written to {manifest_path}")
