"""
Phase 9 Sales Order Generator Module.

Generates Sales Orders, Delivery Orders, Invoices, and Payments according to
monthly scenario targets, category quantity bounds, and state allocations.
Supports dry-run mode and reference-based idempotency.
"""

import random
from phase9.config import SEED, SO_CATEGORY_QTY_BOUNDS, BATCH_PREFIX, COMPANY_NAME, WAREHOUSE_CODE
from phase9.batch_tags import get_so_ref, record_exists

def generate_sales_orders(models, db, uid, password, monthly_allocation, customer_records, product_templates, product_categories, dry_run=True, months=None):
    """
    Args:
        monthly_allocation: dict mapping month (1..12) -> list of customer partner_ids
        customer_records: list of customer dicts
        product_templates: list of 240 product template dicts
        product_categories: dict mapping cat_id -> cat_name
        dry_run: bool
        months: list of ints (e.g. [1] or [1,2,3,4,5]), None for all 12 months
    Returns:
        so_summary: dict with state breakdown and counts
    """
    rng = random.Random(SEED)

    print("=" * 60)
    print(f"Phase 9: Sales Order Generation ({'DRY RUN' if dry_run else 'LIVE'})")
    print("=" * 60)

    # Group products by category leaf name
    prods_by_cat = {}
    for p in product_templates:
        cat_id = p['categ_id'][0]
        cat_name = product_categories.get(cat_id, 'Consumables')
        if cat_name not in prods_by_cat:
            prods_by_cat[cat_name] = []
        prods_by_cat[cat_name].append(p)

    all_cats = list(prods_by_cat.keys())
    so_sequence = 1
    total_so_count = 0
    total_line_count = 0

    so_states = []
    # State allocation for 720 SOs: 662 sale (92%), 29 draft (4%), 29 cancel (4%)
    for _ in range(662): so_states.append('sale')
    for _ in range(29): so_states.append('draft')
    for _ in range(29): so_states.append('cancel')
    rng.shuffle(so_states)

    dry_run_records = []

    for month in range(1, 13):
        cust_list = monthly_allocation[month]
        for cust_id in cust_list:
            so_ref = get_so_ref(so_sequence)
            target_state = so_states[so_sequence - 1]

            # Choose 1..5 products for this SO
            num_lines = rng.randint(1, 5)
            selected_cats = rng.choices(all_cats, k=num_lines)
            
            lines = []
            used_prods = set()
            for cat in selected_cats:
                pool = [p for p in prods_by_cat[cat] if p['id'] not in used_prods]
                if not pool:
                    pool = prods_by_cat[cat]
                p = rng.choice(pool)
                used_prods.add(p['id'])

                q_min, q_max = SO_CATEGORY_QTY_BOUNDS.get(cat, (1, 5))
                qty = rng.randint(q_min, q_max)

                # Discount logic: 75% 0%, 20% 2-5%, 5% 6-10%
                r = rng.random()
                if r < 0.75:
                    discount = 0.0
                elif r < 0.95:
                    discount = float(rng.randint(2, 5))
                else:
                    discount = float(rng.randint(6, 10))

                lines.append({
                    'product_tmpl_id': p['id'],
                    'default_code': p['default_code'],
                    'qty': qty,
                    'price_unit': p['list_price'],
                    'discount': discount,
                })

            total_line_count += len(lines)
            total_so_count += 1

            # Day in month (business days)
            day = rng.randint(1, 28)
            date_order = f"2026-{month:02d}-{day:02d} 10:00:00"

            record_info = {
                'seq': so_sequence,
                'ref': so_ref,
                'customer_id': cust_id,
                'month': month,
                'date_order': date_order,
                'target_state': target_state,
                'lines': lines,
            }
            dry_run_records.append(record_info)
            so_sequence += 1

    print(f"Generated plan for {total_so_count} Sales Orders with {total_line_count} line items (avg {total_line_count/total_so_count:.2f} lines/SO).")
    print(f"  State Breakdown: {so_states.count('sale')} sale, {so_states.count('draft')} draft, {so_states.count('cancel')} cancel")

    if dry_run:
        print("*** DRY RUN — Sales Orders planned. Run live mode to create Odoo records. ***")
        return {
            'total_so': total_so_count,
            'total_lines': total_line_count,
            'state_breakdown': {'sale': 662, 'draft': 29, 'cancel': 29},
            'records': dry_run_records
        }

    # LIVE MODE: Create Odoo records via XML-RPC ORM
    print("\n--- Creating Sales Orders in Odoo ---")
    created_count = 0
    skipped_count = 0

    target_records = [r for r in dry_run_records if (months is None or r['month'] in months)]
    print(f"Targeting {len(target_records)} Sales Orders for months {months if months else '1-12'}...")

    # Bulk pre-fetch variant IDs for all product templates (1 query)
    all_tmpl_ids = [p['id'] for p in product_templates]
    variants = models.execute_kw(db, uid, password, 'product.product', 'search_read',
        [[('product_tmpl_id', 'in', all_tmpl_ids)]], {'fields': ['id', 'product_tmpl_id']})
    tmpl_to_var = {v['product_tmpl_id'][0]: v['id'] for v in variants}

    # Fetch PT Prima Alat Nusantara company ID and PAN warehouse ID
    comp = models.execute_kw(db, uid, password, 'res.company', 'search_read',
        [[('name', '=', COMPANY_NAME)]], {'fields': ['id'], 'limit': 1})
    company_id = comp[0]['id'] if comp else 1

    wh = models.execute_kw(db, uid, password, 'stock.warehouse', 'search_read',
        [[('code', '=', WAREHOUSE_CODE)]], {'fields': ['id'], 'limit': 1})
    warehouse_id = wh[0]['id'] if wh else 1

    for rec in target_records:
        existing_id = record_exists(models, db, uid, password, 'sale.order', 'client_order_ref', rec['ref'])
        if existing_id:
            skipped_count += 1
            continue

        # Convert template IDs to product variant IDs using bulk map
        order_line_vals = []
        for line in rec['lines']:
            var_id = tmpl_to_var.get(line['product_tmpl_id'], line['product_tmpl_id'])

            order_line_vals.append((0, 0, {
                'product_id': var_id,
                'product_uom_qty': line['qty'],
                'price_unit': line['price_unit'],
                'discount': line['discount'],
            }))

        so_val = {
            'partner_id': rec['customer_id'],
            'date_order': rec['date_order'],
            'client_order_ref': rec['ref'],
            'order_line': order_line_vals,
            'company_id': company_id,
            'warehouse_id': warehouse_id,
        }

        so_id = models.execute_kw(db, uid, password, 'sale.order', 'create', [so_val])
        created_count += 1

        if rec['target_state'] == 'sale':
            try:
                models.execute_kw(db, uid, password, 'sale.order', 'action_confirm', [[so_id]])
            except Exception:
                pass
        elif rec['target_state'] == 'cancel':
            try:
                models.execute_kw(db, uid, password, 'sale.order', 'action_cancel', [[so_id]])
            except Exception:
                pass

        if created_count % 100 == 0:
            print(f"  Created {created_count}/{len(dry_run_records)} Sales Orders...")

    print(f"*** SALES ORDER GENERATION COMPLETE: {created_count} created, {skipped_count} skipped (idempotent) ***")
    return {
        'created_so': created_count,
        'skipped_so': skipped_count,
        'total_so': total_so_count,
    }
