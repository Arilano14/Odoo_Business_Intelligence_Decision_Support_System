"""
Phase 9 Demand Planner Module.

Calculates projected annual demand, movement profiles (fast, normal, slow, no-demand),
and daily demand statistics for all 240 portfolio products.
"""

import random
from phase9.config import SEED

ANNUAL_DEMAND_RANGES = {
    'Heavy Equipment': (2, 8),
    'Engine and Hydraulic Parts': (10, 60),
    'Undercarriage Parts': (15, 80),
    'Filters and Maintenance Parts': (50, 400),
    'Consumables': (100, 800),
}

def plan_product_demand(products_by_category):
    """
    Args:
        products_by_category: dict mapping category_name -> list of product dicts
                              e.g. {'Heavy Equipment': [{'id': 1, 'default_code': '...'}, ...]}
    Returns:
        demand_plan: dict mapping product_id -> {
            'annual_demand': int,
            'avg_daily_demand': float,
            'movement_profile': str ('fast', 'normal', 'slow', 'no-demand'),
            'category': str
        }
    """
    rng = random.Random(SEED)
    demand_plan = {}

    all_products = []
    for cat_name, prod_list in products_by_category.items():
        for p in prod_list:
            all_products.append((p, cat_name))

    # Sort deterministically by default_code
    all_products.sort(key=lambda x: x[0]['default_code'])

    # Select 20 products for 'no-demand' (within 15-25 range)
    no_demand_indices = set(rng.sample(range(len(all_products)), 20))

    temp_demand = []
    for idx, (p, cat_name) in enumerate(all_products):
        pid = p['id']
        if idx in no_demand_indices:
            annual = 0
        else:
            cat_range = ANNUAL_DEMAND_RANGES.get(cat_name, (10, 100))
            annual = rng.randint(cat_range[0], cat_range[1])

        temp_demand.append({
            'product_id': pid,
            'default_code': p['default_code'],
            'category': cat_name,
            'annual_demand': annual,
        })

    # Classify movement profile based on positive demand percentile
    demanded_items = [item for item in temp_demand if item['annual_demand'] > 0]
    demanded_items.sort(key=lambda x: x['annual_demand'], reverse=True)

    total_active = len(demanded_items)
    fast_count = int(total_active * 0.20)
    slow_count = int(total_active * 0.20)

    fast_ids = set(x['product_id'] for x in demanded_items[:fast_count])
    slow_ids = set(x['product_id'] for x in demanded_items[-slow_count:])

    for item in temp_demand:
        pid = item['product_id']
        annual = item['annual_demand']
        daily = annual / 365.0

        if annual == 0:
            profile = 'no-demand'
        elif pid in fast_ids:
            profile = 'fast'
        elif pid in slow_ids:
            profile = 'slow'
        else:
            profile = 'normal'

        demand_plan[pid] = {
            'product_id': pid,
            'default_code': item['default_code'],
            'category': item['category'],
            'annual_demand': annual,
            'avg_daily_demand': daily,
            'movement_profile': profile,
        }

    return demand_plan
