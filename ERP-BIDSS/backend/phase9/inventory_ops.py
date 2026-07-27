"""
Phase 9 Inventory Operations Module.

Generates 24 Internal Transfers and 12 Scrap Operations across 12 months
according to category quantity bounds and scenario specifications.
Supports dry-run mode and reference-based idempotency.
"""

import random
from phase9.config import SEED, WAREHOUSE_CODE, TOTAL_TRANSFERS_TARGET, TOTAL_SCRAP_TARGET
from phase9.batch_tags import get_int_ref, get_scrap_ref, record_exists

SCRAP_QTY_BOUNDS = {
    'Heavy Equipment': (0, 0),
    'Engine and Hydraulic Parts': (1, 1),
    'Undercarriage Parts': (1, 2),
    'Filters and Maintenance Parts': (1, 5),
    'Consumables': (1, 10),
}

def generate_inventory_operations(models, db, uid, password, product_templates, product_categories, dry_run=True, months=None):
    """
    Args:
        product_templates: list of 240 product template dicts
        product_categories: dict mapping cat_id -> cat_name
        dry_run: bool
        months: list of ints (e.g. [1] or [1,2,3,4,5]), None for all 12 months
    Returns:
        ops_summary: dict with counts of internal transfers and scrap operations
    """
    rng = random.Random(SEED)

    print("=" * 60)
    print(f"Phase 9: Inventory Operations Generation ({'DRY RUN' if dry_run else 'LIVE'})")
    print("=" * 60)

    # Filter out Heavy Equipment for scrap operations
    scrap_eligible_prods = []
    for p in product_templates:
        cat_id = p['categ_id'][0]
        cat_name = product_categories.get(cat_id, 'Consumables')
        if cat_name != 'Heavy Equipment':
            scrap_eligible_prods.append((p, cat_name))

    # 1. Plan 24 Internal Transfers (2 per month)
    int_records = []
    int_seq = 1
    for m in range(1, 13):
        for _ in range(2):
            ref = get_int_ref(int_seq)
            p = rng.choice(product_templates)
            qty = rng.randint(2, 10)
            day = rng.randint(1, 28)
            date_str = f"2026-{m:02d}-{day:02d} 14:00:00"
            # 20 done, 4 pending
            is_done = int_seq <= 20
            int_records.append({
                'seq': int_seq,
                'ref': ref,
                'product_tmpl_id': p['id'],
                'default_code': p['default_code'],
                'qty': qty,
                'date': date_str,
                'is_done': is_done,
            })
            int_seq += 1

    # 2. Plan 12 Scrap Operations (1 per month)
    scrap_records = []
    scrap_seq = 1
    for m in range(1, 13):
        ref = get_scrap_ref(scrap_seq)
        p, cat_name = rng.choice(scrap_eligible_prods)
        q_min, q_max = SCRAP_QTY_BOUNDS.get(cat_name, (1, 2))
        qty = rng.randint(q_min, q_max)
        day = rng.randint(1, 28)
        date_str = f"2026-{m:02d}-{day:02d} 16:00:00"
        scrap_records.append({
            'seq': scrap_seq,
            'ref': ref,
            'product_tmpl_id': p['id'],
            'default_code': p['default_code'],
            'category': cat_name,
            'qty': qty,
            'date': date_str,
        })
        scrap_seq += 1

    print(f"Planned {len(int_records)} Internal Transfers (20 done, 4 pending) and {len(scrap_records)} Scrap Operations.")

    if dry_run:
        print("*** DRY RUN — Inventory operations planned. Run live mode to create Odoo records. ***")
        return {
            'internal_transfers': len(int_records),
            'scrap_operations': len(scrap_records),
            'int_records': int_records,
            'scrap_records': scrap_records,
        }

    # LIVE MODE: Create Odoo records via XML-RPC ORM
    print("\n--- Creating Inventory Operations in Odoo ---")

    # Fetch PAN warehouse internal stock locations
    wh = models.execute_kw(db, uid, password, 'stock.warehouse', 'search_read',
        [[('code', '=', WAREHOUSE_CODE)]], {'fields': ['id', 'lot_stock_id', 'company_id'], 'limit': 1})
    if not wh:
        raise ValueError(f"Main warehouse '{WAREHOUSE_CODE}' not found!")

    stock_loc_id = wh[0]['lot_stock_id'][0]
    company_id = wh[0]['company_id'][0]

    # Find internal picking type for PAN
    picking_type = models.execute_kw(db, uid, password, 'stock.picking.type', 'search_read',
        [[('company_id', '=', company_id), ('code', '=', 'internal')]], {'fields': ['id'], 'limit': 1})
    if picking_type:
        int_type_id = picking_type[0]['id']
    else:
        int_type_id = models.execute_kw(db, uid, password, 'stock.picking.type', 'create', [{
            'name': 'Internal Transfers',
            'code': 'internal',
            'sequence_code': 'INT',
            'warehouse_id': wh[0]['id'],
            'company_id': company_id,
            'default_location_src_id': stock_loc_id,
            'default_location_dest_id': stock_loc_id,
        }])

    # Find scrap location matching company
    scrap_loc = models.execute_kw(db, uid, password, 'stock.location', 'search_read',
        [[('scrap_location', '=', True), '|', ('company_id', '=', company_id), ('company_id', '=', False)]], {'fields': ['id'], 'limit': 1})
    scrap_loc_id = scrap_loc[0]['id'] if scrap_loc else None

    created_int = 0
    skipped_int = 0

    target_int_records = [r for r in int_records if (months is None or int(r['date'].split('-')[1]) in months)]
    target_scrap_records = [r for r in scrap_records if (months is None or int(r['date'].split('-')[1]) in months)]

    # Destination location for internal transfers (sub-location under PAN/Stock)
    dest_loc = models.execute_kw(db, uid, password, 'stock.location', 'search_read',
        [[('complete_name', '=', 'PAN/Stock/Zone A')]], {'fields': ['id'], 'limit': 1})
    if dest_loc:
        dest_loc_id = dest_loc[0]['id']
    else:
        dest_loc_id = models.execute_kw(db, uid, password, 'stock.location', 'create', [{
            'name': 'Zone A',
            'location_id': stock_loc_id,
            'usage': 'internal',
            'company_id': company_id,
        }])

    # Bulk pre-fetch existing internal transfer refs
    existing_pickings = models.execute_kw(db, uid, password, 'stock.picking', 'search_read',
        [[('origin', '=like', 'PORTFOLIO_2026_V1-INT-%')]], {'fields': ['origin']})
    existing_int_refs = {p['origin'] for p in existing_pickings if p.get('origin')}

    if int_type_id:
        for rec in target_int_records:
            if rec['ref'] in existing_int_refs:
                skipped_int += 1
                continue

            variant = models.execute_kw(db, uid, password, 'product.product', 'search_read',
                [[('product_tmpl_id', '=', rec['product_tmpl_id'])]], {'fields': ['id', 'uom_id'], 'limit': 1})
            if not variant:
                continue

            var_id = variant[0]['id']
            uom_id = variant[0]['uom_id'][0]

            picking_val = {
                'picking_type_id': int_type_id,
                'location_id': stock_loc_id,
                'location_dest_id': dest_loc_id,  # Internal transfer within warehouse
                'origin': rec['ref'],
                'date': rec['date'],
                'company_id': company_id,
            }
            picking_id = models.execute_kw(db, uid, password, 'stock.picking', 'create', [picking_val])

            move_val = {
                'name': f"Internal Transfer {rec['ref']}",
                'product_id': var_id,
                'product_uom_qty': rec['qty'],
                'product_uom': uom_id,
                'picking_id': picking_id,
                'location_id': stock_loc_id,
                'location_dest_id': dest_loc_id,
                'company_id': company_id,
            }
            models.execute_kw(db, uid, password, 'stock.move', 'create', [move_val])
            try:
                models.execute_kw(db, uid, password, 'stock.picking', 'action_confirm', [[picking_id]])
            except Exception:
                pass

            if rec['is_done']:
                try:
                    moves = models.execute_kw(db, uid, password, 'stock.move', 'search_read',
                        [[('picking_id', '=', picking_id)]], {'fields': ['id']})
                    for m in moves:
                        models.execute_kw(db, uid, password, 'stock.move', 'write',
                            [[m['id']], {'quantity': rec['qty']}])
                    models.execute_kw(db, uid, password, 'stock.picking', 'button_validate', [[picking_id]])
                except Exception as e:
                    print(f"  Warning: Could not validate transfer {rec['ref']}: {e}")

            created_int += 1

    created_scrap = 0
    skipped_scrap = 0

    if scrap_loc_id:
        for rec in target_scrap_records:
            existing = record_exists(models, db, uid, password, 'stock.scrap', 'origin', rec['ref'])
            if existing:
                skipped_scrap += 1
                continue

            variant = models.execute_kw(db, uid, password, 'product.product', 'search_read',
                [[('product_tmpl_id', '=', rec['product_tmpl_id'])]], {'fields': ['id', 'uom_id'], 'limit': 1})
            if not variant:
                continue

            var_id = variant[0]['id']
            uom_id = variant[0]['uom_id'][0]

            scrap_val = {
                'product_id': var_id,
                'scrap_qty': float(rec['qty']),
                'product_uom_id': uom_id,
                'location_id': stock_loc_id,
                'scrap_location_id': scrap_loc_id,
                'origin': rec['ref'],
                'company_id': company_id,
            }
            scrap_id = models.execute_kw(db, uid, password, 'stock.scrap', 'create', [scrap_val])
            try:
                models.execute_kw(db, uid, password, 'stock.scrap', 'do_scrap', [[scrap_id]])
            except Exception as e:
                print(f"  Warning: Could not validate scrap {rec['ref']}: {e}")

            created_scrap += 1

    print(f"*** INVENTORY OPERATIONS COMPLETE: Internal Transfers ({created_int} created, {skipped_int} skipped), Scrap ({created_scrap} created, {skipped_scrap} skipped) ***")
    return {
        'created_transfers': created_int,
        'skipped_transfers': skipped_int,
        'created_scraps': created_scrap,
        'skipped_scraps': skipped_scrap,
    }
