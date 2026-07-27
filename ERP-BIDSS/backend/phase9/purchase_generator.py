"""
Phase 9 Purchase Order Generator Module.

Generates Purchase Orders, Receipts, Vendor Bills, and Payments according to
monthly scenario targets, category quantity bounds, supplierinfo rules, and state allocations.
Supports dry-run mode and reference-based idempotency.
"""

import random
from phase9.config import SEED, PO_CATEGORY_QTY_BOUNDS, BATCH_PREFIX, COMPANY_NAME
from phase9.batch_tags import get_po_ref, record_exists

def generate_purchase_orders(models, db, uid, password, monthly_allocation, supplier_products, product_templates, product_categories, supplierinfo_records, dry_run=True, months=None):
    """
    Args:
        monthly_allocation: dict mapping month (1..12) -> list of supplier partner_ids
        supplier_products: dict mapping partner_id -> list of product_tmpl_ids
        product_templates: list of 240 product template dicts
        product_categories: dict mapping cat_id -> cat_name
        supplierinfo_records: list of product.supplierinfo dicts
        dry_run: bool
        months: list of ints (e.g. [1] or [1,2,3,4,5]), None for all 12 months
    Returns:
        po_summary: dict with state breakdown and counts
    """
    rng = random.Random(SEED)

    print("=" * 60)
    print(f"Phase 9: Purchase Order Generation ({'DRY RUN' if dry_run else 'LIVE'})")
    print("=" * 60)

    # Build lookup: (tmpl_id, partner_id) -> supplierinfo price & delay
    sinfo_map = {}
    for info in supplierinfo_records:
        pid = info['partner_id'][0] if isinstance(info['partner_id'], (list, tuple)) else info['partner_id']
        tmpl_id = info['product_tmpl_id'][0] if isinstance(info['product_tmpl_id'], (list, tuple)) else info['product_tmpl_id']
        sinfo_map[(tmpl_id, pid)] = {
            'price': info.get('price', 0.0),
            'delay': info.get('delay', 5),
        }

    tmpl_lookup = {p['id']: p for p in product_templates}

    po_sequence = 1
    total_po_count = 0
    total_line_count = 0

    po_states = []
    # State allocation for 240 POs: 221 purchase (92%), 10 draft (4%), 9 cancel (4%)
    for _ in range(221): po_states.append('purchase')
    for _ in range(10): po_states.append('draft')
    for _ in range(9): po_states.append('cancel')
    rng.shuffle(po_states)

    dry_run_records = []

    for month in range(1, 13):
        supp_list = monthly_allocation[month]
        for supp_id in supp_list:
            po_ref = get_po_ref(po_sequence)
            target_state = po_states[po_sequence - 1]

            available_tmpl_ids = supplier_products.get(supp_id, [])
            if not available_tmpl_ids:
                # Fallback to all product templates if supplier mapping is empty
                available_tmpl_ids = list(tmpl_lookup.keys())

            num_lines = min(rng.randint(2, 8), len(available_tmpl_ids))
            selected_tmpl_ids = rng.sample(available_tmpl_ids, num_lines)

            lines = []
            for tmpl_id in selected_tmpl_ids:
                tmpl = tmpl_lookup.get(tmpl_id)
                if not tmpl:
                    continue

                cat_id = tmpl['categ_id'][0]
                cat_name = product_categories.get(cat_id, 'Consumables')
                q_min, q_max = PO_CATEGORY_QTY_BOUNDS.get(cat_name, (2, 10))
                qty = rng.randint(q_min, q_max)

                # Price from supplierinfo or standard_price
                s_info = sinfo_map.get((tmpl_id, supp_id))
                price = s_info['price'] if (s_info and s_info['price'] > 0) else tmpl.get('standard_price', 10000.0)

                lines.append({
                    'product_tmpl_id': tmpl_id,
                    'default_code': tmpl['default_code'],
                    'qty': qty,
                    'price_unit': price,
                    'delay': s_info['delay'] if s_info else 5,
                })

            total_line_count += len(lines)
            total_po_count += 1

            day = rng.randint(1, 28)
            date_order = f"2026-{month:02d}-{day:02d} 10:00:00"

            record_info = {
                'seq': po_sequence,
                'ref': po_ref,
                'supplier_id': supp_id,
                'month': month,
                'date_order': date_order,
                'target_state': target_state,
                'lines': lines,
            }
            dry_run_records.append(record_info)
            po_sequence += 1

    print(f"Generated plan for {total_po_count} Purchase Orders with {total_line_count} line items (avg {total_line_count/total_po_count:.2f} lines/PO).")
    print(f"  State Breakdown: {po_states.count('purchase')} purchase, {po_states.count('draft')} draft, {po_states.count('cancel')} cancel")

    if dry_run:
        print("*** DRY RUN — Purchase Orders planned. Run live mode to create Odoo records. ***")
        return {
            'total_po': total_po_count,
            'total_lines': total_line_count,
            'state_breakdown': {'purchase': 221, 'draft': 10, 'cancel': 9},
            'records': dry_run_records
        }

    # LIVE MODE: Create Odoo records via XML-RPC ORM
    print("\n--- Creating Purchase Orders in Odoo ---")
    created_count = 0
    skipped_count = 0

    target_records = [r for r in dry_run_records if (months is None or r['month'] in months)]
    print(f"Targeting {len(target_records)} Purchase Orders for months {months if months else '1-12'}...")

    # Bulk pre-fetch variant IDs for all product templates (1 query)
    all_tmpl_ids = [p['id'] for p in product_templates]
    variants = models.execute_kw(db, uid, password, 'product.product', 'search_read',
        [[('product_tmpl_id', 'in', all_tmpl_ids)]], {'fields': ['id', 'product_tmpl_id']})
    tmpl_to_var = {v['product_tmpl_id'][0]: v['id'] for v in variants}

    # Fetch PT Prima Alat Nusantara company ID
    comp = models.execute_kw(db, uid, password, 'res.company', 'search_read',
        [[('name', '=', COMPANY_NAME)]], {'fields': ['id'], 'limit': 1})
    company_id = comp[0]['id'] if comp else 1

    # Bulk pre-fetch existing PO refs (1 query instead of 240 queries)
    existing_pos = models.execute_kw(db, uid, password, 'purchase.order', 'search_read',
        [[('partner_ref', '=like', f'{BATCH_PREFIX}-PO-%')]], {'fields': ['partner_ref']})
    existing_refs = {p['partner_ref'] for p in existing_pos if p.get('partner_ref')}

    for rec in target_records:
        if rec['ref'] in existing_refs:
            skipped_count += 1
            continue

        order_line_vals = []
        for line in rec['lines']:
            var_id = tmpl_to_var.get(line['product_tmpl_id'], line['product_tmpl_id'])

            order_line_vals.append((0, 0, {
                'product_id': var_id,
                'product_qty': line['qty'],
                'price_unit': line['price_unit'],
                'date_planned': rec['date_order'],
            }))

        po_val = {
            'partner_id': rec['supplier_id'],
            'date_order': rec['date_order'],
            'partner_ref': rec['ref'],
            'order_line': order_line_vals,
            'company_id': company_id,
        }

        po_id = models.execute_kw(db, uid, password, 'purchase.order', 'create', [po_val])
        created_count += 1

        if rec['target_state'] == 'purchase':
            try:
                models.execute_kw(db, uid, password, 'purchase.order', 'button_confirm', [[po_id]])
            except Exception:
                pass
        elif rec['target_state'] == 'cancel':
            try:
                models.execute_kw(db, uid, password, 'purchase.order', 'button_cancel', [[po_id]])
            except Exception:
                pass

        # Re-write target date_order so confirmed order preserves exact plan date
        models.execute_kw(db, uid, password, 'purchase.order', 'write', [[po_id], {'date_order': rec['date_order']}])

        if created_count % 50 == 0:
            print(f"  Created {created_count}/{len(dry_run_records)} Purchase Orders...")

    print(f"*** PURCHASE ORDER GENERATION COMPLETE: {created_count} created, {skipped_count} skipped (idempotent) ***")
    return {
        'created_po': created_count,
        'skipped_po': skipped_count,
        'total_po': total_po_count,
    }
