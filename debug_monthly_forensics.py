# Forensics: Why does date_order:month fail in Odoo Spreadsheet?
# Let's test how Odoo's spreadsheet engine evaluates PIVOT.HEADER and PIVOT.VALUE
# for sale.order with date_order:month vs sale.report with date:month

import json

print("=" * 70)
print("FORENSICS GATE R1 — SALES MONTHLY TREND FORENSICS")
print("=" * 70)

# Check sale.order vs sale.report field definitions
so_date = env['sale.order']._fields['date_order']
sr_date = env['sale.report']._fields['date']

print(f"sale.order date_order type: {so_date.type}, string='{so_date.string}'")
print(f"sale.report date type:       {sr_date.type}, string='{sr_date.string}'")

# Let's inspect read_group on sale.order with date_order:month
so_group = env['sale.order'].read_group(
    domain=[('company_id', '=', 2), ('state', '=', 'sale'), ('date_order', '>=', '2026-01-01'), ('date_order', '<', '2027-01-01')],
    fields=['amount_untaxed'],
    groupby=['date_order:month']
)

print(f"\nsale.order read_group('date_order:month') result count: {len(so_group)}")
for g in so_group[:5]:
    print(f"  date_order:month = {g['date_order:month']!r} | amount_untaxed = {g.get('amount_untaxed'):,.2f} | count = {g.get('date_order_count')}")

# Now let's test sale.report read_group('date:month')
sr_group = env['sale.report'].read_group(
    domain=[('company_id', '=', 2), ('state', '=', 'sale'), ('date', '>=', '2026-01-01'), ('date', '<', '2027-01-01')],
    fields=['price_subtotal'],
    groupby=['date:month']
)

print(f"\nsale.report read_group('date:month') result count: {len(sr_group)}")
for g in sr_group[:5]:
    print(f"  date:month = {g['date:month']!r} | price_subtotal = {g.get('price_subtotal'):,.2f} | count = {g.get('date_count')}")

# Now let's check what format Odoo Spreadsheet expects for columns/rows in PIVOT definition!
# Does Odoo Spreadsheet pivot expect 'date_order:month' in columns?
# Let's inspect how Odoo spreadsheet pivot processes date fields!
