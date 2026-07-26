"""
Phase 9 Customer Allocation Module.

Allocates exactly 720 Sales Orders across 48 portfolio customers in 4 segments
and distributes them deterministically across 12 months.
"""

import random
from phase9.config import SEED, CUSTOMER_SEGMENTS, MONTHLY_TARGETS, TOTAL_SO_TARGET

def allocate_customers(customer_records):
    """
    Args:
        customer_records: list of 48 customer dicts [{'id': 1, 'name': '...', 'ref': 'PORTFOLIO_2026_V1-CUST-001'}, ...]
    Returns:
        allocation_plan: dict with keys:
            'customer_segments': dict mapping partner_id -> segment_name
            'annual_orders': dict mapping partner_id -> order_count
            'monthly_allocation': dict mapping month (1..12) -> list of partner_ids for each SO
    """
    rng = random.Random(SEED)

    # Sort customers deterministically by ref
    custs = sorted(customer_records, key=lambda x: x['ref'])
    if len(custs) != 48:
        raise ValueError(f"Expected 48 customers, got {len(custs)}")

    # Assign segments deterministically
    # 8 Strategic, 16 Regular, 14 Occasional, 10 One-time
    segment_assignment = {}
    idx = 0
    for seg_name, cfg in CUSTOMER_SEGMENTS.items():
        count = cfg['count']
        for c in custs[idx:idx+count]:
            segment_assignment[c['id']] = seg_name
        idx += count

    # Step 1: Assign annual order counts
    annual_orders = {}

    # One-time customers get exactly 1 order
    one_time_ids = [c['id'] for c in custs if segment_assignment[c['id']] == 'One-time']
    for cid in one_time_ids:
        annual_orders[cid] = 1

    # Base allocation for remaining segments
    other_custs = [c['id'] for c in custs if segment_assignment[c['id']] != 'One-time']
    
    # Set min bounds
    current_total = len(one_time_ids)
    for cid in other_custs:
        seg = segment_assignment[cid]
        min_o = CUSTOMER_SEGMENTS[seg]['min_orders']
        annual_orders[cid] = min_o
        current_total += min_o

    # Distribute remaining orders to reach exactly 720
    remaining = TOTAL_SO_TARGET - current_total

    while remaining > 0:
        # Pick a customer eligible for more orders
        candidate = rng.choice(other_custs)
        seg = segment_assignment[candidate]
        max_o = CUSTOMER_SEGMENTS[seg]['max_orders']
        if annual_orders[candidate] < max_o:
            annual_orders[candidate] += 1
            remaining -= 1

    assert sum(annual_orders.values()) == TOTAL_SO_TARGET, "Annual order total mismatch"
    for cid in one_time_ids:
        assert annual_orders[cid] == 1, "One-time customer violated"

    # Step 2: Distribute across 12 months matching MONTHLY_TARGETS
    # Create order pool for each month
    monthly_allocation = {m: [] for m in range(1, 13)}

    # Place one-time customers in random distinct months
    ot_months = rng.sample(range(1, 13), len(one_time_ids))
    for cid, m in zip(one_time_ids, ot_months):
        monthly_allocation[m].append(cid)

    # Remaining order counts to assign per customer
    remaining_cust_orders = {cid: annual_orders[cid] for cid in other_custs}

    # Month targets remaining
    remaining_month_slots = {m: MONTHLY_TARGETS[m]['so'] - len(monthly_allocation[m]) for m in range(1, 13)}

    # Distribute month by month
    for m in range(1, 13):
        slots_needed = remaining_month_slots[m]
        # Candidates are customers with remaining_cust_orders > 0
        candidates = [cid for cid in other_custs if remaining_cust_orders[cid] > 0]
        
        # Weighted by remaining orders
        weights = [remaining_cust_orders[cid] for cid in candidates]

        # Select candidates for this month without exceeding slots_needed
        selected_for_month = []
        for _ in range(slots_needed):
            if not candidates:
                break
            # We can pick customer if they haven't been picked too many times in this month
            # Prefer unique customers per month if possible
            available_candidates = [c for c in candidates if selected_for_month.count(c) < 3]
            if not available_candidates:
                available_candidates = candidates
            
            avail_weights = [remaining_cust_orders[c] for c in available_candidates]
            chosen = rng.choices(available_candidates, weights=avail_weights, k=1)[0]
            selected_for_month.append(chosen)
            remaining_cust_orders[chosen] -= 1
            if remaining_cust_orders[chosen] == 0:
                idx = candidates.index(chosen)
                candidates.pop(idx)

        monthly_allocation[m].extend(selected_for_month)

    # Verify monthly totals
    for m in range(1, 13):
        expected = MONTHLY_TARGETS[m]['so']
        actual = len(monthly_allocation[m])
        assert actual == expected, f"Month {m} allocation mismatch: expected {expected}, got {actual}"

    return {
        'customer_segments': segment_assignment,
        'annual_orders': annual_orders,
        'monthly_allocation': monthly_allocation,
    }
