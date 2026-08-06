# Reconcile: why "all transacted (any state)" = 257 but "confirmed transacted" = 254
# The difference of 3 variants must be products that exist in draft/cancel SO/PO only

so_lines_all = env['sale.order.line'].search([('order_id.company_id', '=', 2)])
po_lines_all = env['purchase.order.line'].search([('order_id.company_id', '=', 2)])
all_so_pids = set(so_lines_all.mapped('product_id.id'))
all_po_pids = set(po_lines_all.mapped('product_id.id'))
all_transacted = all_so_pids | all_po_pids

so_lines_confirmed = env['sale.order.line'].search([
    ('order_id.company_id', '=', 2),
    ('order_id.state', 'in', ['sale', 'done'])
])
po_lines_confirmed = env['purchase.order.line'].search([
    ('order_id.company_id', '=', 2),
    ('order_id.state', 'in', ['purchase', 'done'])
])
confirmed_so_pids = set(so_lines_confirmed.mapped('product_id.id'))
confirmed_po_pids = set(po_lines_confirmed.mapped('product_id.id'))
confirmed_transacted = confirmed_so_pids | confirmed_po_pids

print(f"All transacted (any state): {len(all_transacted)}")
print(f"Confirmed transacted: {len(confirmed_transacted)}")

# Find the 3 that are in draft/cancel only
draft_only = all_transacted - confirmed_transacted
print(f"\nProducts in draft/cancel orders ONLY (not confirmed): {len(draft_only)}")
for pid in draft_only:
    p = env['product.product'].browse(pid)
    # Find what orders they appear in
    so_states = set()
    po_states = set()
    for line in so_lines_all.filtered(lambda l: l.product_id.id == pid):
        so_states.add(line.order_id.state)
    for line in po_lines_all.filtered(lambda l: l.product_id.id == pid):
        po_states.add(line.order_id.state)
    print(f"  ID: {pid}, Name: {p.name}, Code: {p.default_code}")
    print(f"    Category: {p.categ_id.complete_name}")
    print(f"    SO states: {so_states}, PO states: {po_states}")

# Also check: are the 4 non-portfolio transacted in the E-COM category?
print(f"\n{'='*60}")
print("NON-PORTFOLIO TRANSACTED IMPACT ANALYSIS")
print(f"{'='*60}")
non_portfolio_ids = [16, 19, 4, 3]
total_so_val = sum(so_lines_confirmed.mapped('price_subtotal'))
total_po_val = sum(po_lines_confirmed.mapped('price_subtotal'))

for pid in non_portfolio_ids:
    p = env['product.product'].browse(pid)
    so_val = sum(so_lines_confirmed.filtered(lambda l: l.product_id.id == pid).mapped('price_subtotal'))
    po_val = sum(po_lines_confirmed.filtered(lambda l: l.product_id.id == pid).mapped('price_subtotal'))
    so_pct = (so_val / total_so_val * 100) if total_so_val else 0
    po_pct = (po_val / total_po_val * 100) if total_po_val else 0
    print(f"  {p.name} (ID={pid}, Code={p.default_code})")
    print(f"    SO: {so_val:,.2f} ({so_pct:.4f}%), PO: {po_val:,.2f} ({po_pct:.4f}%)")

print(f"\nTotal confirmed SO value: {total_so_val:,.2f}")
print(f"Total confirmed PO value: {total_po_val:,.2f}")
