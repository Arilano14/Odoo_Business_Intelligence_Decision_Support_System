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

    print("\n--- Executing Phase 9 ORM Cleanup ---")

    # Clean Invoices/Bills
    for inv in inv_list:
        try:
            if inv['state'] != 'draft':
                models.execute_kw(db, uid, password, 'account.move', 'button_draft', [[inv['id']]])
            models.execute_kw(db, uid, password, 'account.move', 'unlink', [[inv['id']]])
        except Exception as e:
            print(f"  Warning: Could not unlink move {inv['ref']}: {e}")

    # Clean Internal Transfers
    for pick in int_list:
        try:
            if pick['state'] not in ('draft', 'cancel'):
                models.execute_kw(db, uid, password, 'stock.picking', 'action_cancel', [[pick['id']]])
            models.execute_kw(db, uid, password, 'stock.picking', 'unlink', [[pick['id']]])
        except Exception as e:
            print(f"  Warning: Could not unlink picking {pick['origin']}: {e}")

    # Clean Purchase Orders
    for po in po_list:
        try:
            if po['state'] not in ('draft', 'cancel'):
                models.execute_kw(db, uid, password, 'purchase.order', 'button_cancel', [[po['id']]])
            models.execute_kw(db, uid, password, 'purchase.order', 'unlink', [[po['id']]])
        except Exception as e:
            print(f"  Warning: Could not unlink PO {po['partner_ref']}: {e}")

    # Clean Sales Orders
    for so in so_list:
        try:
            if so['state'] not in ('draft', 'cancel'):
                models.execute_kw(db, uid, password, 'sale.order', 'action_cancel', [[so['id']]])
            models.execute_kw(db, uid, password, 'sale.order', 'unlink', [[so['id']]])
        except Exception as e:
            print(f"  Warning: Could not unlink SO {so['client_order_ref']}: {e}")

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
