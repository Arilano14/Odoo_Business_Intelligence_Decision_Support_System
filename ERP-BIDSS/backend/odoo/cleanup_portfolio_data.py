import os
import sys
from .connection import get_connection

def perform_cleanup(dry_run=True, confirm=None):
    print(f"\n[PHASE 8] Running Cleanup (Dry Run: {dry_run})")
    
    if not dry_run and confirm != "PHASE8-WIPE-APPROVED":
        print("ERROR: Application of cleanup requires the confirmation token 'PHASE8-WIPE-APPROVED'")
        sys.exit(1)

    try:
        uid, models, db, password = get_connection()
    except Exception as e:
        print(f"Failed to connect to Odoo: {e}")
        return

    # 1. Clean Sales Orders
    print("\n--- Cleaning Sales Orders ---")
    sales = models.execute_kw(db, uid, password, 'sale.order', 'search_read',
        [[ '|', ('date_order', '=like', '2024%'), ('date_order', '=like', '2026%') ]],
        {'fields': ['id', 'name', 'state']})
    
    sales_to_cancel = [s['id'] for s in sales if s['state'] != 'cancel']
    if sales_to_cancel and not dry_run:
        print(f"Cancelling {len(sales_to_cancel)} sales orders...")
        models.execute_kw(db, uid, password, 'sale.order', 'action_cancel', [sales_to_cancel])
    
    if sales and not dry_run:
        print(f"Deleting {len(sales)} sales orders...")
        models.execute_kw(db, uid, password, 'sale.order', 'unlink', [[s['id'] for s in sales]])
    elif dry_run:
        print(f"[DRY-RUN] Would cancel {len(sales_to_cancel)} and delete {len(sales)} sales orders.")

    # 2. Clean Purchase Orders
    print("\n--- Cleaning Purchase Orders ---")
    purchases = models.execute_kw(db, uid, password, 'purchase.order', 'search_read',
        [[ '|', ('date_order', '=like', '2024%'), ('date_order', '=like', '2026%') ]],
        {'fields': ['id', 'name', 'state']})
    
    purchases_to_cancel = [p['id'] for p in purchases if p['state'] != 'cancel']
    if purchases_to_cancel and not dry_run:
        print(f"Cancelling {len(purchases_to_cancel)} purchase orders...")
        models.execute_kw(db, uid, password, 'purchase.order', 'button_cancel', [purchases_to_cancel])
        
    if purchases and not dry_run:
        print(f"Deleting {len(purchases)} purchase orders...")
        models.execute_kw(db, uid, password, 'purchase.order', 'unlink', [[p['id'] for p in purchases]])
    elif dry_run:
        print(f"[DRY-RUN] Would cancel {len(purchases_to_cancel)} and delete {len(purchases)} purchase orders.")

    # 3. Clean Account Moves (Invoices/Bills)
    print("\n--- Cleaning Account Moves ---")
    moves = models.execute_kw(db, uid, password, 'account.move', 'search_read',
        [[ '&', ('move_type', 'in', ['out_invoice', 'in_invoice']), '|', ('date', '=like', '2024%'), ('date', '=like', '2026%') ]],
        {'fields': ['id', 'name', 'state']})
    
    moves_to_cancel = [m['id'] for m in moves if m['state'] == 'posted']
    if moves_to_cancel and not dry_run:
        print(f"Cancelling {len(moves_to_cancel)} account moves (resetting to draft)...")
        # In Odoo, to cancel a posted invoice you usually need to reset to draft first
        try:
            models.execute_kw(db, uid, password, 'account.move', 'button_draft', [moves_to_cancel])
        except Exception as e:
            print(f"WARNING: Failed to reset to draft: {e}")
            print("Stopping cleanup to prevent forced SQL unlink on posted records.")
            sys.exit(1)
            
        print("Cancelling drafts...")
        models.execute_kw(db, uid, password, 'account.move', 'button_cancel', [moves_to_cancel])
        
    if moves and not dry_run:
        print(f"Deleting {len(moves)} account moves...")
        models.execute_kw(db, uid, password, 'account.move', 'unlink', [[m['id'] for m in moves]])
    elif dry_run:
        print(f"[DRY-RUN] Would cancel {len(moves_to_cancel)} and delete {len(moves)} account moves.")

    # 4. Clean Stock Pickings
    print("\n--- Cleaning Stock Pickings ---")
    pickings = models.execute_kw(db, uid, password, 'stock.picking', 'search_read',
        [[ '|', ('date', '=like', '2024%'), ('date', '=like', '2026%') ]],
        {'fields': ['id', 'name', 'state']})
    
    pickings_to_cancel = [p['id'] for p in pickings if p['state'] not in ('cancel', 'done')]
    done_pickings = [p['id'] for p in pickings if p['state'] == 'done']
    
    if pickings_to_cancel and not dry_run:
        print(f"Cancelling {len(pickings_to_cancel)} stock pickings...")
        models.execute_kw(db, uid, password, 'stock.picking', 'action_cancel', [pickings_to_cancel])

    if done_pickings:
        print(f"WARNING: There are {len(done_pickings)} DONE pickings. Odoo ORM prevents deleting done stock moves.")
        if not dry_run:
            print("Skipping deletion of DONE pickings to adhere to safety rules.")
            # Only unlink non-done pickings
            pickings_to_delete = [p['id'] for p in pickings if p['state'] != 'done']
            if pickings_to_delete:
                print(f"Deleting {len(pickings_to_delete)} cancelled pickings...")
                models.execute_kw(db, uid, password, 'stock.picking', 'unlink', [pickings_to_delete])
    elif pickings and not dry_run:
        print(f"Deleting {len(pickings)} stock pickings...")
        models.execute_kw(db, uid, password, 'stock.picking', 'unlink', [[p['id'] for p in pickings]])
        
    if dry_run:
        print(f"[DRY-RUN] Would cancel {len(pickings_to_cancel)} and attempt to delete {len(pickings) - len(done_pickings)} pickings (skipping {len(done_pickings)} DONE pickings).")

    # 5. Clean Portfolio Partners (Customers & Suppliers)
    print("\n--- Cleaning Portfolio Partners ---")
    partners = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
        [[ '|', ('ref', '=like', 'BIDSS-CUST-%'), ('ref', '=like', 'BIDSS-VEND-%') ]],
        {'fields': ['id', 'name', 'ref']})
    
    if partners and not dry_run:
        print(f"Deleting {len(partners)} portfolio partners...")
        models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[p['id'] for p in partners]])
    elif dry_run:
        print(f"[DRY-RUN] Would delete {len(partners)} partners.")

    # 6. Clean Portfolio Products
    print("\n--- Cleaning Portfolio Products ---")
    products = models.execute_kw(db, uid, password, 'product.product', 'search_read',
        [[('default_code', '=like', 'BIDSS-HE-%')]], 
        {'fields': ['id', 'name', 'default_code']})
    
    # Also we should find other products generated by the old script.
    # We can rely on the newly setup product category later to keep things organized, 
    # but for now we'll clean the ones with BIDSS-HE
    
    if products and not dry_run:
        print(f"Deleting {len(products)} portfolio products...")
        models.execute_kw(db, uid, password, 'product.product', 'unlink', [[p['id'] for p in products]])
    elif dry_run:
        print(f"[DRY-RUN] Would delete {len(products)} products.")

    print("\n[PHASE 8] Cleanup phase finished.")
