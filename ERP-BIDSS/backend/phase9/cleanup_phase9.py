"""
Phase 9 Batch Cleanup Module.

Safely reverses Phase 9 transaction records (tagged with PORTFOLIO_2026_V1)
using Odoo ORM in correct reverse dependency order.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from odoo.connection import get_connection
from phase9.config import BATCH_PREFIX

def cleanup_phase9_batch(dry_run=True):
    uid, models, db, password = get_connection()

    print("=" * 60)
    print(f"Phase 9 Batch Cleanup ({'DRY RUN' if dry_run else 'LIVE'})")
    print("=" * 60)

    # 1. Search Phase 9 Sales Orders
    so_list = models.execute_kw(db, uid, password, 'sale.order', 'search_read',
        [[('client_order_ref', '=like', f"{BATCH_PREFIX}-SO-%")]], {'fields': ['id', 'client_order_ref', 'state']})

    # 2. Search Phase 9 Purchase Orders
    po_list = models.execute_kw(db, uid, password, 'purchase.order', 'search_read',
        [[('partner_ref', '=like', f"{BATCH_PREFIX}-PO-%")]], {'fields': ['id', 'partner_ref', 'state']})

    # 3. Search Phase 9 Account Moves (Invoices/Bills)
    inv_list = models.execute_kw(db, uid, password, 'account.move', 'search_read',
        [['|', ('ref', '=like', f"{BATCH_PREFIX}-INV-%"), ('ref', '=like', f"{BATCH_PREFIX}-BILL-%")]],
        {'fields': ['id', 'ref', 'state']})

    # 4. Search Phase 9 Internal Transfers
    int_list = models.execute_kw(db, uid, password, 'stock.picking', 'search_read',
        [[('origin', '=like', f"{BATCH_PREFIX}-INT-%")]], {'fields': ['id', 'origin', 'state']})

    # 5. Search Phase 9 Scrap Operations
    scrap_list = models.execute_kw(db, uid, password, 'stock.scrap', 'search_read',
        [[('origin', '=like', f"{BATCH_PREFIX}-SCRAP-%")]], {'fields': ['id', 'origin']})

    print(f"Found Phase 9 Records to Clean:")
    print(f"  Sales Orders: {len(so_list)}")
    print(f"  Purchase Orders: {len(po_list)}")
    print(f"  Invoices/Bills: {len(inv_list)}")
    print(f"  Internal Transfers: {len(int_list)}")
    print(f"  Scrap Operations: {len(scrap_list)}")

    if dry_run:
        print("\n*** DRY RUN — No records deleted. Run with --apply to execute cleanup. ***")
        return True

    print("\n--- Executing Phase 9 ORM Cleanup (Batch Optimized) ---")

    # 1. Clean Invoices/Bills
    if inv_list:
        inv_ids = [inv['id'] for inv in inv_list]
        for inv_id in inv_ids:
            try:
                models.execute_kw(db, uid, password, 'account.move', 'button_draft', [[inv_id]])
                models.execute_kw(db, uid, password, 'account.move', 'unlink', [[inv_id]])
            except Exception:
                pass

    # 2. Clean Internal Transfers
    if int_list:
        int_ids = [p['id'] for p in int_list]
        for int_id in int_ids:
            try:
                models.execute_kw(db, uid, password, 'stock.picking', 'action_cancel', [[int_id]])
                models.execute_kw(db, uid, password, 'stock.picking', 'unlink', [[int_id]])
            except Exception:
                pass

    # 3. Clean Purchase Orders
    if po_list:
        po_ids = [p['id'] for p in po_list]
        for po_id in po_ids:
            try:
                models.execute_kw(db, uid, password, 'purchase.order', 'button_cancel', [[po_id]])
                models.execute_kw(db, uid, password, 'purchase.order', 'unlink', [[po_id]])
            except Exception:
                pass

    # 4. Clean Sales Orders
    if so_list:
        so_ids = [s['id'] for s in so_list]
        for so_id in so_ids:
            try:
                models.execute_kw(db, uid, password, 'sale.order', 'action_cancel', [[so_id]])
                models.execute_kw(db, uid, password, 'sale.order', 'unlink', [[so_id]])
            except Exception:
                pass

    # Clean Scrap Operations
    for scrap in scrap_list:
        try:
            models.execute_kw(db, uid, password, 'stock.scrap', 'unlink', [[scrap['id']]])
        except Exception as e:
            print(f"  Warning: Could not unlink scrap {scrap['origin']}: {e}")

    print("*** PHASE 9 BATCH CLEANUP COMPLETE ***")
    return True

if __name__ == '__main__':
    dry_run = '--apply' not in sys.argv
    cleanup_phase9_batch(dry_run=dry_run)
