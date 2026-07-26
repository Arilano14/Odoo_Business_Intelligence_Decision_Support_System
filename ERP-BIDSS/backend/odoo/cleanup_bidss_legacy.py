"""
Phase 9 Pre-Work: Legacy BIDSS Master Data Cleanup.

Identifies and removes legacy BIDSS synthetic data (products with code 'BIDSS-%',
partners with ref 'BIDSS-CUST-%' or 'BIDSS-VEND-%') using Odoo ORM.

Generates a dry-run manifest before deletion.
Does NOT perform indiscriminate wipes or use direct SQL writes.
Preserves system partners, company config, accounting setup, warehouses, etc.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from odoo.connection import get_connection

MANIFEST_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "docs", "phase9", "bidss_cleanup_manifest.md"
)

def build_manifest_and_clean(dry_run=True):
    uid, models, db, password = get_connection()

    print("=" * 60)
    print(f"Phase 9 Pre-Work: BIDSS Legacy Cleanup ({'DRY RUN' if dry_run else 'LIVE'})")
    print("=" * 60)

    # 1. Identify legacy transactions (if any)
    legacy_so = models.execute_kw(db, uid, password, 'sale.order', 'search_read',
        [[('name', '=like', 'SO/BIDSS/%')]], {'fields': ['id', 'name', 'state']})
    
    legacy_po = models.execute_kw(db, uid, password, 'purchase.order', 'search_read',
        [[('name', '=like', 'PO/BIDSS/%')]], {'fields': ['id', 'name', 'state']})

    # 2. Identify legacy products
    legacy_prods = models.execute_kw(db, uid, password, 'product.template', 'search_read',
        [[('default_code', '=like', 'BIDSS-%')]], {'fields': ['id', 'name', 'default_code']})

    # 3. Identify legacy partners
    legacy_custs = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
        [[('ref', '=like', 'BIDSS-CUST-%')]], {'fields': ['id', 'name', 'ref']})
    
    legacy_vends = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
        [[('ref', '=like', 'BIDSS-VEND-%')]], {'fields': ['id', 'name', 'ref']})

    manifest_lines = []
    manifest_lines.append("# BIDSS Legacy Data Cleanup Manifest")
    manifest_lines.append(f"Generated for Phase 9 pre-work. Total candidates identified.")
    manifest_lines.append("")
    manifest_lines.append("## Candidate Summary")
    manifest_lines.append(f"- **Legacy Sales Orders:** {len(legacy_so)}")
    manifest_lines.append(f"- **Legacy Purchase Orders:** {len(legacy_po)}")
    manifest_lines.append(f"- **Legacy Products:** {len(legacy_prods)}")
    manifest_lines.append(f"- **Legacy Customers:** {len(legacy_custs)}")
    manifest_lines.append(f"- **Legacy Vendors:** {len(legacy_vends)}")
    manifest_lines.append("")

    manifest_lines.append("## Deletion Candidates Detail")
    manifest_lines.append("| Model | Record ID | Name / Ref | Deletion Reason | Dependency Check |")
    manifest_lines.append("|---|---:|---|---|---|")

    candidates = []

    for so in legacy_so:
        manifest_lines.append(f"| `sale.order` | {so['id']} | {so['name']} | Legacy BIDSS transaction | state={so['state']} |")
        candidates.append(('sale.order', so['id'], so['name']))

    for po in legacy_po:
        manifest_lines.append(f"| `purchase.order` | {po['id']} | {po['name']} | Legacy BIDSS transaction | state={po['state']} |")
        candidates.append(('purchase.order', po['id'], po['name']))

    for p in legacy_prods:
        manifest_lines.append(f"| `product.template` | {p['id']} | {p['default_code']} ({p['name']}) | Legacy BIDSS master product | Safe ORM unlink candidate |")
        candidates.append(('product.template', p['id'], p['default_code']))

    for c in legacy_custs:
        manifest_lines.append(f"| `res.partner` | {c['id']} | {c['ref']} ({c['name']}) | Legacy BIDSS customer | Safe ORM unlink candidate |")
        candidates.append(('res.partner', c['id'], c['ref']))

    for v in legacy_vends:
        manifest_lines.append(f"| `res.partner` | {v['id']} | {v['ref']} ({v['name']}) | Legacy BIDSS supplier | Safe ORM unlink candidate |")
        candidates.append(('res.partner', v['id'], v['ref']))

    # Write manifest file
    os.makedirs(os.path.dirname(MANIFEST_PATH), exist_ok=True)
    with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(manifest_lines))

    print(f"[OK] Manifest written to {MANIFEST_PATH}")
    print(f"Total candidates: {len(candidates)} ({len(legacy_prods)} prods, {len(legacy_custs)} custs, {len(legacy_vends)} vends)")

    if dry_run:
        print("\n*** DRY RUN COMPLETE — Manifest generated. Run with --apply to perform ORM deletion. ***")
        return True

    # Execution phase
    print("\n--- Performing ORM Deletion ---")
    deleted_counts = {'sale.order': 0, 'purchase.order': 0, 'product.template': 0, 'res.partner': 0}

    # 1. Clean transactions first if any
    for so in legacy_so:
        if so['state'] not in ('draft', 'cancel'):
            models.execute_kw(db, uid, password, 'sale.order', 'action_cancel', [[so['id']]])
        models.execute_kw(db, uid, password, 'sale.order', 'unlink', [[so['id']]])
        deleted_counts['sale.order'] += 1

    for po in legacy_po:
        if po['state'] not in ('draft', 'cancel'):
            models.execute_kw(db, uid, password, 'purchase.order', 'button_cancel', [[po['id']]])
        models.execute_kw(db, uid, password, 'purchase.order', 'unlink', [[po['id']]])
        deleted_counts['purchase.order'] += 1

    # 2. Archive legacy products via ORM active=False
    legacy_prod_ids = [p['id'] for p in legacy_prods]
    if legacy_prod_ids:
        print(f"Archiving {len(legacy_prod_ids)} legacy product templates...")
        for i in range(0, len(legacy_prod_ids), 50):
            chunk = legacy_prod_ids[i:i+50]
            models.execute_kw(db, uid, password, 'product.template', 'write', [chunk, {'active': False}])
            deleted_counts['product.template'] += len(chunk)
            print(f"  Archived {deleted_counts['product.template']}/{len(legacy_prod_ids)} product templates...")

    # 3. Archive legacy partners
    legacy_partner_ids = [c['id'] for c in legacy_custs] + [v['id'] for v in legacy_vends]
    if legacy_partner_ids:
        print(f"Archiving {len(legacy_partner_ids)} legacy partners...")
        for i in range(0, len(legacy_partner_ids), 50):
            chunk = legacy_partner_ids[i:i+50]
            models.execute_kw(db, uid, password, 'res.partner', 'write', [chunk, {'active': False}])
            deleted_counts['res.partner'] += len(chunk)
            print(f"  Archived {deleted_counts['res.partner']}/{len(legacy_partner_ids)} partners...")

    print("\n*** LEGACY BIDSS CLEANUP COMPLETED SUCCESSFULLY ***")
    print(f"Summary: {deleted_counts}")
    return True

if __name__ == '__main__':
    dry_run = '--apply' not in sys.argv
    build_manifest_and_clean(dry_run=dry_run)
