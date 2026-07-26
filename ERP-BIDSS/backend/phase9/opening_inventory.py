"""
Phase 9 Opening Inventory Module.

Creates opening stock adjustment on 2026-01-01 for all 240 portfolio products
based on stock coverage rules (fast/normal/slow/no-demand).
Uses supported Odoo ORM (stock.quant action_apply_inventory). No direct SQL.
"""

import random
from phase9.config import SEED, WAREHOUSE_CODE

COVERAGE_DAYS = {
    'fast': (45, 75),
    'normal': (60, 100),
    'slow': (120, 210),
}

def generate_opening_inventory(models, db, uid, password, demand_plan, dry_run=True):
    """
    Args:
        demand_plan: dict mapping product_id -> {'annual_demand': int, 'avg_daily_demand': float, 'movement_profile': str, ...}
        dry_run: if True, prints calculation without modifying Odoo records.
    Returns:
        opening_quantities: dict mapping product_id -> opening_qty
    """
    rng = random.Random(SEED)
    opening_quantities = {}

    print("=" * 60)
    print(f"Phase 9: Opening Inventory Generation ({'DRY RUN' if dry_run else 'LIVE'})")
    print("=" * 60)

    # 1. Fetch PAN warehouse stock location
    wh = models.execute_kw(db, uid, password, 'stock.warehouse', 'search_read',
        [[('code', '=', WAREHOUSE_CODE)]], {'fields': ['id', 'lot_stock_id'], 'limit': 1})

    if not wh:
        raise ValueError(f"Main warehouse '{WAREHOUSE_CODE}' not found!")

    stock_loc_id = wh[0]['lot_stock_id'][0]

    # Sort product IDs for deterministic calculation
    sorted_pids = sorted(demand_plan.keys())

    total_value = 0.0
    products_with_stock = 0
    products_zero_stock = 0

    for pid in sorted_pids:
        info = demand_plan[pid]
        profile = info['movement_profile']
        daily = info['avg_daily_demand']

        if profile == 'no-demand':
            # 60% zero stock, 40% 1..5 units
            if rng.random() < 0.60:
                qty = 0
            else:
                qty = rng.randint(1, 5)
        else:
            days_range = COVERAGE_DAYS[profile]
            days = rng.randint(days_range[0], days_range[1])
            qty = int(round(daily * days))
            qty = max(1, qty)  # Ensure at least 1 unit if profile is fast/normal/slow

        opening_quantities[pid] = qty

        if qty > 0:
            products_with_stock += 1
        else:
            products_zero_stock += 1

    print(f"Opening Stock Plan: {products_with_stock} products with stock, {products_zero_stock} products with zero stock.")

    if dry_run:
        print("*** DRY RUN — Opening inventory calculated. Run live mode to apply. ***")
        return opening_quantities

    # Live Mode: Apply inventory via stock.quant ORM
    print("\n--- Applying Opening Inventory via Odoo ORM ---")
    quant_vals = []
    for pid, qty in opening_quantities.items():
        if qty > 0:
            # Check existing quant
            existing = models.execute_kw(db, uid, password, 'stock.quant', 'search_read',
                [[('product_id', '=', pid), ('location_id', '=', stock_loc_id)]], {'fields': ['id']})
            
            if existing:
                models.execute_kw(db, uid, password, 'stock.quant', 'write',
                    [[existing[0]['id']], {'inventory_quantity': qty}])
                qid = existing[0]['id']
            else:
                qid = models.execute_kw(db, uid, password, 'stock.quant', 'create', [{
                    'product_id': pid,
                    'location_id': stock_loc_id,
                    'inventory_quantity': qty,
                }])
            quant_vals.append(qid)

    if quant_vals:
        # Apply in batch chunks of 50
        for i in range(0, len(quant_vals), 50):
            chunk = quant_vals[i:i+50]
            models.execute_kw(db, uid, password, 'stock.quant', 'action_apply_inventory', [chunk])
            print(f"  Applied inventory batch {i+len(chunk)}/{len(quant_vals)}...")

    print("*** OPENING INVENTORY APPLIED SUCCESSFULLY ***")
    return opening_quantities
