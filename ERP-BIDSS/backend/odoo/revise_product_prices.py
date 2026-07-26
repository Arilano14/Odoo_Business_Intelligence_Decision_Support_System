"""
Phase 9 Pre-Work: Revise Phase 8 product prices to realistic category ranges.

This script updates the 240 PORTFOLIO_2026_V1-PROD-* products with
category-appropriate cost and selling prices using deterministic seeding.

Uses XML-RPC ORM only. No direct SQL.
"""
import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from odoo.connection import get_connection

# Deterministic seed
SEED = 26072026

# Category price ranges: (min_sell, max_sell, margin_min, margin_max)
# margin = (sell - cost) / sell  =>  cost = sell * (1 - margin)
CATEGORY_PRICE_RANGES = {
    'Heavy Equipment': {
        'sell_min': 600_000_000,      # Rp 600M
        'sell_max': 2_500_000_000,    # Rp 2.5B
        'margin_min': 0.12,
        'margin_max': 0.18,
    },
    'Engine and Hydraulic Parts': {
        'sell_min': 15_000_000,       # Rp 15M
        'sell_max': 250_000_000,      # Rp 250M
        'margin_min': 0.20,
        'margin_max': 0.32,
    },
    'Undercarriage Parts': {
        'sell_min': 5_000_000,        # Rp 5M
        'sell_max': 80_000_000,       # Rp 80M
        'margin_min': 0.20,
        'margin_max': 0.35,
    },
    'Filters and Maintenance Parts': {
        'sell_min': 300_000,          # Rp 300K
        'sell_max': 12_000_000,       # Rp 12M
        'margin_min': 0.22,
        'margin_max': 0.38,
    },
    'Consumables': {
        'sell_min': 50_000,           # Rp 50K
        'sell_max': 3_000_000,        # Rp 3M
        'margin_min': 0.25,
        'margin_max': 0.40,
    },
}


def revise_product_prices(dry_run=True):
    uid, models, db, password = get_connection()
    rng = random.Random(SEED)

    print("=" * 60)
    print(f"Phase 9 Pre-Work: Product Price Revision ({'DRY RUN' if dry_run else 'LIVE'})")
    print("=" * 60)

    # Get all portfolio products with their categories
    products = models.execute_kw(db, uid, password, 'product.template', 'search_read',
        [[('default_code', '=like', 'PORTFOLIO_2026_V1-PROD-%')]],
        {'fields': ['id', 'name', 'default_code', 'categ_id', 'list_price', 'standard_price'],
         'order': 'default_code asc'})

    if len(products) != 240:
        print(f"ERROR: Expected 240 products, found {len(products)}. Aborting.")
        return False

    # Build category name lookup
    cat_ids = list(set(p['categ_id'][0] for p in products))
    categories = models.execute_kw(db, uid, password, 'product.category', 'search_read',
        [[('id', 'in', cat_ids)]], {'fields': ['id', 'name', 'complete_name']})
    cat_map = {}
    for c in categories:
        # Extract the leaf category name from complete_name like "Portfolio 2026 / Heavy Equipment"
        leaf_name = c['complete_name'].split(' / ')[-1] if ' / ' in c['complete_name'] else c['name']
        cat_map[c['id']] = leaf_name

    updated = 0
    errors = 0
    stats = {cat: {'count': 0, 'min_sell': float('inf'), 'max_sell': 0, 'min_margin': 1.0, 'max_margin': 0.0}
             for cat in CATEGORY_PRICE_RANGES}

    for p in products:
        cat_id = p['categ_id'][0]
        cat_name = cat_map.get(cat_id, 'Unknown')

        if cat_name not in CATEGORY_PRICE_RANGES:
            print(f"WARNING: Product {p['default_code']} has unknown category '{cat_name}'. Skipping.")
            errors += 1
            continue

        cfg = CATEGORY_PRICE_RANGES[cat_name]

        # Generate selling price within range
        sell_price = rng.randint(cfg['sell_min'], cfg['sell_max'])

        # Round to nice numbers
        if sell_price >= 1_000_000_000:
            sell_price = round(sell_price, -7)  # Round to nearest 10M for big items
        elif sell_price >= 100_000_000:
            sell_price = round(sell_price, -6)  # Round to nearest 1M
        elif sell_price >= 10_000_000:
            sell_price = round(sell_price, -5)  # Round to nearest 100K
        elif sell_price >= 1_000_000:
            sell_price = round(sell_price, -4)  # Round to nearest 10K
        else:
            sell_price = round(sell_price, -3)  # Round to nearest 1K

        # Generate margin within range
        margin = rng.uniform(cfg['margin_min'], cfg['margin_max'])

        # Calculate cost from margin: margin = (sell - cost) / sell => cost = sell * (1 - margin)
        cost_price = int(sell_price * (1.0 - margin))

        # Round cost to nice numbers
        if cost_price >= 1_000_000_000:
            cost_price = round(cost_price, -6)
        elif cost_price >= 100_000_000:
            cost_price = round(cost_price, -5)
        elif cost_price >= 10_000_000:
            cost_price = round(cost_price, -4)
        elif cost_price >= 1_000_000:
            cost_price = round(cost_price, -3)
        else:
            cost_price = round(cost_price, -2)

        actual_margin = (sell_price - cost_price) / sell_price if sell_price > 0 else 0

        # Validate
        if sell_price <= 0 or cost_price <= 0:
            print(f"ERROR: Product {p['default_code']} would get zero/negative price. Aborting.")
            return False
        if cost_price >= sell_price:
            print(f"ERROR: Product {p['default_code']} cost ({cost_price}) >= sell ({sell_price}). Aborting.")
            return False

        # Track stats
        s = stats[cat_name]
        s['count'] += 1
        s['min_sell'] = min(s['min_sell'], sell_price)
        s['max_sell'] = max(s['max_sell'], sell_price)
        s['min_margin'] = min(s['min_margin'], actual_margin)
        s['max_margin'] = max(s['max_margin'], actual_margin)

        if not dry_run:
            models.execute_kw(db, uid, password, 'product.template', 'write',
                [[p['id']], {'list_price': float(sell_price), 'standard_price': float(cost_price)}])

        updated += 1
        if updated % 50 == 0:
            print(f"  Processed {updated}/240 products...")

    print(f"\nProcessed: {updated}, Errors: {errors}")
    print("\n--- Category Summary ---")
    for cat_name, s in stats.items():
        if s['count'] > 0:
            print(f"  {cat_name}: {s['count']} products")
            print(f"    Sell range: Rp {s['min_sell']:,.0f} – Rp {s['max_sell']:,.0f}")
            print(f"    Margin range: {s['min_margin']:.1%} – {s['max_margin']:.1%}")

    # Also update supplierinfo prices to match cost prices
    if not dry_run:
        print("\n--- Updating Supplier Info Prices ---")
        tmpl_ids = [p['id'] for p in products]
        for tmpl_id in tmpl_ids:
            tmpl = models.execute_kw(db, uid, password, 'product.template', 'read',
                [tmpl_id], {'fields': ['standard_price']})
            cost = tmpl[0]['standard_price'] if tmpl else 0

            # Supplier price = cost * (0.95 to 1.03) — slight variation
            sinfos = models.execute_kw(db, uid, password, 'product.supplierinfo', 'search_read',
                [[('product_tmpl_id', '=', tmpl_id)]], {'fields': ['id', 'sequence']})
            for si in sinfos:
                # Primary supplier gets best price, secondary pays slightly more
                price_factor = 1.0 + (si['sequence'] - 1) * 0.02  # +2% per rank
                si_price = int(cost * price_factor * rng.uniform(0.97, 1.03))
                si_price = max(si_price, 1000)  # floor at Rp 1000
                models.execute_kw(db, uid, password, 'product.supplierinfo', 'write',
                    [[si['id']], {'price': float(si_price)}])

        print("  Supplier info prices updated.")

    if dry_run:
        print("\n*** DRY RUN — No changes written. Run with --apply to commit. ***")
    else:
        print("\n*** PRICES UPDATED SUCCESSFULLY ***")

    return errors == 0


if __name__ == '__main__':
    import sys
    dry_run = '--apply' not in sys.argv
    success = revise_product_prices(dry_run=dry_run)
    if not success:
        sys.exit(1)
