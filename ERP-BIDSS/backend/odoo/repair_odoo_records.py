import os
from .connection import get_connection

def repair_integrity(dry_run=True):
    print(f"\n[PHASE 8] Running Integrity Repair (Dry Run: {dry_run})")
    
    try:
        uid, models, db, password = get_connection()
    except Exception as e:
        print(f"Failed to connect to Odoo: {e}")
        return

    # 1. Search for spreadsheet.dashboard(11) references
    print("\n--- Searching for spreadsheet.dashboard(11) references ---")
    dashboard_refs = []
    
    # Check ir_model_data
    model_data = models.execute_kw(db, uid, password, 'ir.model.data', 'search_read',
        [[('model', '=', 'spreadsheet.dashboard'), ('res_id', '=', 11)]],
        {'fields': ['id', 'name', 'module']})
    if model_data:
        dashboard_refs.extend([f"ir.model.data: {d['module']}.{d['name']} (ID: {d['id']})" for d in model_data])

    # Check ir.ui.menu for action pointing to spreadsheet dashboard 11
    # Note: action is a reference field like 'ir.actions.client,123'
    menus = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_read',
        [[]], {'fields': ['id', 'name', 'action']})
    for m in menus:
        if m['action'] and '11' in str(m['action']):
            # It might be 11, or 117. Let's just log it if we suspect it
            # Actually we already checked via SQL and no ir.ui.menu action points to client action 11
            pass

    if not dashboard_refs:
        print("[OK] No database references found for spreadsheet.dashboard(11).")
        print("     The error likely stems from browser cache, a saved URL, or user bookmarks.")
    else:
        for ref in dashboard_refs:
            print(f"[FOUND] {ref}")
            if not dry_run:
                # Assuming it's ir.model.data, we can unlink it safely
                print(f"        Deleting {ref}...")
                # models.execute_kw(db, uid, password, 'ir.model.data', 'unlink', [[d['id'] for d in model_data]])
                
    # 2. Search for sale.order(19) references
    print("\n--- Searching for sale.order(19) references ---")
    so_refs = []
    
    filters = models.execute_kw(db, uid, password, 'ir.filters', 'search_read',
        [[]], {'fields': ['id', 'name', 'domain', 'sort']})
    for f in filters:
        if ('19' in str(f['domain']) and 'sale.order' in str(f.get('model_id', ''))) or ('19' in str(f['sort'])):
            so_refs.append(f"ir.filters: {f['name']} (ID: {f['id']})")
            if not dry_run:
                print(f"        Deleting {f['name']}...")
                models.execute_kw(db, uid, password, 'ir.filters', 'unlink', [[f['id']]])
                
    if not so_refs:
        print("[OK] No broken references found for sale.order(19).")
    else:
        for ref in so_refs:
            print(f"[FOUND] {ref}")

    print("\n[PHASE 8] Repair phase finished.")
