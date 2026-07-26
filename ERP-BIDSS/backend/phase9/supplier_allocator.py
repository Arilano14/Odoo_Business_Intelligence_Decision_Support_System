"""
Phase 9 Supplier Allocation Module.

Allocates exactly 240 Purchase Orders across 24 portfolio suppliers in 4 segments
and distributes them deterministically across 12 months, respecting product.supplierinfo mappings.
"""

import random
from phase9.config import SEED, SUPPLIER_SEGMENTS, MONTHLY_TARGETS, TOTAL_PO_TARGET

def allocate_suppliers(supplier_records, supplierinfo_records):
    """
    Args:
        supplier_records: list of 24 supplier dicts [{'id': 1, 'name': '...', 'ref': 'PORTFOLIO_2026_V1-VEND-001'}, ...]
        supplierinfo_records: list of supplierinfo dicts [{'partner_id': [id, name], 'product_tmpl_id': [id, name], 'delay': int, 'price': float}, ...]
    Returns:
        allocation_plan: dict with keys:
            'supplier_segments': dict mapping partner_id -> segment_name
            'annual_pos': dict mapping partner_id -> po_count
            'monthly_allocation': dict mapping month (1..12) -> list of partner_ids for each PO
            'supplier_products': dict mapping partner_id -> list of product_tmpl_ids
    """
    rng = random.Random(SEED)

    # Sort suppliers deterministically by ref
    supps = sorted(supplier_records, key=lambda x: x['ref'])
    if len(supps) != 24:
        raise ValueError(f"Expected 24 suppliers, got {len(supps)}")

    # Map supplier to product templates they can provide
    supplier_products = {s['id']: set() for s in supps}
    for info in supplierinfo_records:
        pid = info['partner_id'][0] if isinstance(info['partner_id'], (list, tuple)) else info['partner_id']
        tmpl_id = info['product_tmpl_id'][0] if isinstance(info['product_tmpl_id'], (list, tuple)) else info['product_tmpl_id']
        if pid in supplier_products:
            supplier_products[pid].add(tmpl_id)

    # Assign segments deterministically
    # 5 Strategic, 10 Regular, 6 Backup, 3 Occasional
    segment_assignment = {}
    idx = 0
    for seg_name, cfg in SUPPLIER_SEGMENTS.items():
        count = cfg['count']
        for s in supps[idx:idx+count]:
            segment_assignment[s['id']] = seg_name
        idx += count

    # Step 1: Assign annual PO counts
    annual_pos = {}
    current_total = 0

    for s in supps:
        sid = s['id']
        seg = segment_assignment[sid]
        min_p = SUPPLIER_SEGMENTS[seg]['min_pos']
        annual_pos[sid] = min_p
        current_total += min_p

    # Distribute remaining POs to reach exactly 240
    remaining = TOTAL_PO_TARGET - current_total
    all_sids = [s['id'] for s in supps]

    while remaining > 0:
        candidate = rng.choice(all_sids)
        seg = segment_assignment[candidate]
        max_p = SUPPLIER_SEGMENTS[seg]['max_pos']
        if annual_pos[candidate] < max_p:
            annual_pos[candidate] += 1
            remaining -= 1

    assert sum(annual_pos.values()) == TOTAL_PO_TARGET, "Annual PO total mismatch"

    # Step 2: Distribute across 12 months matching MONTHLY_TARGETS
    monthly_allocation = {m: [] for m in range(1, 13)}
    remaining_supp_pos = {sid: annual_pos[sid] for sid in all_sids}

    # Backup suppliers get higher weight in April (Month 4)
    backup_sids = [sid for sid in all_sids if segment_assignment[sid] == 'Backup']
    strategic_sids = [sid for sid in all_sids if segment_assignment[sid] == 'Strategic']

    for m in range(1, 13):
        slots_needed = MONTHLY_TARGETS[m]['po']
        selected_for_month = []

        for _ in range(slots_needed):
            candidates = [sid for sid in all_sids if remaining_supp_pos[sid] > 0]
            if not candidates:
                break

            # Adjust weights for Month 4 (Procurement response - backup suppliers boosted)
            weights = []
            for sid in candidates:
                w = float(remaining_supp_pos[sid])
                if m == 4 and sid in backup_sids:
                    w *= 3.0
                elif sid in strategic_sids:
                    w *= 1.5
                weights.append(w)

            chosen = rng.choices(candidates, weights=weights, k=1)[0]
            selected_for_month.append(chosen)
            remaining_supp_pos[chosen] -= 1

        monthly_allocation[m].extend(selected_for_month)

    # Verify monthly totals
    for m in range(1, 13):
        expected = MONTHLY_TARGETS[m]['po']
        actual = len(monthly_allocation[m])
        assert actual == expected, f"Month {m} PO allocation mismatch: expected {expected}, got {actual}"

    return {
        'supplier_segments': segment_assignment,
        'annual_pos': annual_pos,
        'monthly_allocation': monthly_allocation,
        'supplier_products': {sid: list(prods) for sid, prods in supplier_products.items()},
    }
