# Inspect all models needed for dashboards
# Purchase, Inventory, and Data Quality

print("=" * 60)
print("1. PURCHASE REPORT MODEL")
print("=" * 60)
try:
    pr = env['purchase.report']
    fields = sorted(pr._fields.keys())
    print(f"Fields ({len(fields)}):")
    for f in fields:
        fd = pr._fields[f]
        print(f"  {f}: {fd.type}, string='{fd.string}'")
except Exception as e:
    print(f"ERROR: {e}")

print()
print("=" * 60)
print("2. PURCHASE ORDER - CONFIRMED STATES")
print("=" * 60)
states = env['purchase.order'].search([('company_id', '=', 2)]).mapped('state')
from collections import Counter
state_counts = Counter(states)
for state, count in sorted(state_counts.items()):
    total_val = sum(env['purchase.order'].search([('company_id', '=', 2), ('state', '=', state)]).mapped('amount_untaxed'))
    print(f"  state='{state}': {count} orders, amount_untaxed={total_val:,.2f}")

print()
print("=" * 60)
print("3. STOCK.MOVE MODEL (key fields)")
print("=" * 60)
try:
    sm = env['stock.move']
    key_fields = ['date', 'product_id', 'product_uom_qty', 'quantity', 'state',
                  'company_id', 'location_id', 'location_dest_id', 'picking_type_id',
                  'reference', 'origin', 'product_uom']
    for f in key_fields:
        if f in sm._fields:
            fd = sm._fields[f]
            print(f"  {f}: {fd.type}, string='{fd.string}'")
        else:
            print(f"  {f}: NOT FOUND")
except Exception as e:
    print(f"ERROR: {e}")

print()
print("=" * 60)
print("4. STOCK.MOVE LOCATION ANALYSIS (Company 2, state=done)")
print("=" * 60)
moves = env['stock.move'].search([('company_id', '=', 2), ('state', '=', 'done')])
print(f"Total done moves: {len(moves)}")

loc_combos = Counter()
for m in moves:
    src = m.location_id.usage
    dst = m.location_dest_id.usage
    loc_combos[(src, dst)] += 1

for (src, dst), count in sorted(loc_combos.items(), key=lambda x: -x[1]):
    print(f"  {src} → {dst}: {count} moves")

print()
print("=" * 60)
print("5. STOCK.QUANT MODEL (key fields)")
print("=" * 60)
try:
    sq = env['stock.quant']
    key_fields = ['product_id', 'location_id', 'quantity', 'reserved_quantity',
                  'value', 'company_id', 'lot_id', 'package_id']
    for f in key_fields:
        if f in sq._fields:
            fd = sq._fields[f]
            print(f"  {f}: {fd.type}, string='{fd.string}'")
        else:
            print(f"  {f}: NOT FOUND")
except Exception as e:
    print(f"ERROR: {e}")

print()
quants = env['stock.quant'].search([('company_id', '=', 2), ('location_id.usage', '=', 'internal')])
print(f"Total internal quants (company 2): {len(quants)}")
total_qty = sum(quants.mapped('quantity'))
zero_stock = len([q for q in quants if q.quantity == 0])
negative = len([q for q in quants if q.quantity < 0])
print(f"  Total on-hand quantity: {total_qty}")
print(f"  Zero-stock quants: {zero_stock}")
print(f"  Negative-stock quants: {negative}")

print()
print("=" * 60)
print("6. STOCK.SCRAP MODEL")
print("=" * 60)
try:
    ss = env['stock.scrap']
    scraps = ss.search([('company_id', '=', 2)])
    print(f"Total scraps: {len(scraps)}")
    for s in scraps[:5]:
        print(f"  ID: {s.id}, Product: {s.product_id.name}, Qty: {s.scrap_qty}, State: {s.state}")
except Exception as e:
    print(f"ERROR: {e}")

print()
print("=" * 60)
print("7. OBIDSS.DATA.QUALITY MODEL")
print("=" * 60)
try:
    dq = env['obidss.data.quality']
    print(f"Model exists. Records: {dq.search_count([])}")
    fields = sorted(dq._fields.keys())
    for f in fields:
        fd = dq._fields[f]
        print(f"  {f}: {fd.type}, string='{fd.string}'")
except Exception as e:
    print(f"Model not found or error: {e}")
