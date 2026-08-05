# Gate 1 Forensic Investigation Script for Sales Operations
# Target: env.ref("obidss_operational_bi.dashboard_sales")

import json

print("=" * 75)
print("GATE 1 — SALES MONTHLY TREND FORENSIC INVESTIGATION")
print("=" * 75)

dashboard = env.ref("obidss_operational_bi.dashboard_sales", raise_if_not_found=False)
if not dashboard:
    print("ERROR: XML ID 'obidss_operational_bi.dashboard_sales' not found!")
    import sys
    sys.exit(1)

print(f"Target Dashboard: {dashboard.name} (DB ID: {dashboard.id})")

# Read spreadsheet data
data = json.loads(dashboard.spreadsheet_data)

# Step 1 — Inspect Pivot Definition 5 (Monthly Sales Trend)
pivots = data.get("pivots", {})
print(f"\nTotal Pivots in Dashboard: {len(pivots)}")

for pid, pivot in pivots.items():
    print(f"\nPivot ID {pid}: '{pivot.get('name')}'")
    print(f"  Model:     {pivot.get('model')}")
    print(f"  Domain:    {pivot.get('domain')}")
    print(f"  Measures:  {pivot.get('measures')}")
    print(f"  Rows:      {pivot.get('rows')}")
    print(f"  Columns:   {pivot.get('columns')}")

# Let's inspect how Odoo ORM read_group behaves for sale.order with date_order
print("\n" + "=" * 75)
print("ORM READ_GROUP TEST — sale.order")
print("=" * 75)

rg_so_month = env['sale.order'].read_group(
    domain=[('company_id', '=', 2), ('state', '=', 'sale'), ('date_order', '>=', '2026-01-01'), ('date_order', '<', '2027-01-01')],
    fields=['amount_untaxed'],
    groupby=['date_order:month']
)

print(f"read_group('date_order:month') returned {len(rg_so_month)} months:")
for g in rg_so_month:
    print(f"  key={g['date_order:month']!r} | amount_untaxed={g['amount_untaxed']:,.2f}")

# Let's inspect how Odoo ORM read_group behaves for sale.report with date
print("\n" + "=" * 75)
print("ORM READ_GROUP TEST — sale.report")
print("=" * 75)

rg_sr_month = env['sale.report'].read_group(
    domain=[('company_id', '=', 2), ('state', '=', 'sale'), ('date', '>=', '2026-01-01'), ('date', '<', '2027-01-01')],
    fields=['price_subtotal'],
    groupby=['date:month']
)

print(f"read_group('date:month') returned {len(rg_sr_month)} months:")
for g in rg_sr_month:
    print(f"  key={g['date:month']!r} | price_subtotal={g['price_subtotal']:,.2f}")

print("\n" + "=" * 75)
print("241 vs 230 SKU RECONCILIATION AUDIT")
print("=" * 75)

# All positive quants in internal locations company 2
all_quants = env['stock.quant'].search([
    ('company_id', '=', 2),
    ('location_id.usage', '=', 'internal'),
    ('quantity', '>', 0)
])
all_pids = set(all_quants.mapped('product_id.id'))

# Excluded products
excluded_pids = set()
for pid in all_pids:
    p = env['product.product'].browse(pid)
    # Check if category is Portfolio 2026 or saleable portfolio
    cat_name = p.categ_id.complete_name
    if not (cat_name.startswith('Portfolio 2026') or cat_name.startswith('All / Saleable') or cat_name.startswith('All / Home Construction')):
        excluded_pids.add(pid)
    elif p.default_code and (p.default_code.startswith('E-COM') or p.default_code.startswith('CONS_')):
        excluded_pids.add(pid)
    elif p.name in ['Acoustic Bloc Screens', 'Virtual Home Staging', 'Virtual Interior Design']:
        excluded_pids.add(pid)

verified_portfolio_pids = all_pids - excluded_pids

print(f"All Positive Stock SKUs (Company 2, Internal):   {len(all_pids)} SKUs")
print(f"Excluded Non-Portfolio / Demo SKUs:               {len(excluded_pids)} SKUs")
print(f"Verified Portfolio SKUs with Positive Stock:       {len(verified_portfolio_pids)} SKUs")
print(f"Difference (241 - 230):                             {len(all_pids) - len(verified_portfolio_pids)} SKUs")

if excluded_pids:
    print("\nExcluded Product Details:")
    for pid in excluded_pids:
        p = env['product.product'].browse(pid)
        print(f"  ID: {pid}, Name: {p.name}, Code: {p.default_code}, Category: {p.categ_id.complete_name}")
