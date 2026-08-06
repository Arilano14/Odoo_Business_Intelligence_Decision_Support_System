# Audit Untaxed Baselines, Purchase Report Fields, Dashboard Fields, PO States

print("=" * 60)
print("1. UNTAXED BASELINE SQL AUDIT (sale_order & purchase_order)")
print("=" * 60)

# Sales untaxed sum
so_domain = [('company_id', '=', 2), ('state', '=', 'sale'), ('date_order', '>=', '2026-01-01'), ('date_order', '<', '2027-01-01')]
so_records = env['sale.order'].search(so_domain)
so_untaxed_sum = sum(so_records.mapped('amount_untaxed'))
so_taxed_sum = sum(so_records.mapped('amount_total'))
so_count = len(so_records)
print(f"Sale Orders (state='sale', company=2, FY2026):")
print(f"  Count: {so_count}")
print(f"  SUM(amount_untaxed): {so_untaxed_sum:,.2f}")
print(f"  SUM(amount_total):   {so_taxed_sum:,.2f}")

# Purchase untaxed sum
po_domain = [('company_id', '=', 2), ('state', 'in', ['purchase', 'done']), ('date_order', '>=', '2026-01-01'), ('date_order', '<', '2027-01-01')]
po_records = env['purchase.order'].search(po_domain)
po_untaxed_sum = sum(po_records.mapped('amount_untaxed'))
po_taxed_sum = sum(po_records.mapped('amount_total'))
po_count = len(po_records)
print(f"\nPurchase Orders (state in ['purchase', 'done'], company=2, FY2026):")
print(f"  Count: {po_count}")
print(f"  SUM(amount_untaxed): {po_untaxed_sum:,.2f}")
print(f"  SUM(amount_total):   {po_taxed_sum:,.2f}")

# Check purchase orders by state
print(f"\nPurchase Orders by State Distribution:")
po_all = env['purchase.order'].search([('company_id', '=', 2), ('date_order', '>=', '2026-01-01'), ('date_order', '<', '2027-01-01')])
for state in ['draft', 'sent', 'to approve', 'purchase', 'done', 'cancel']:
    recs = po_all.filtered(lambda p: p.state == state)
    if recs:
        u_sum = sum(recs.mapped('amount_untaxed'))
        t_sum = sum(recs.mapped('amount_total'))
        print(f"  state='{state}': {len(recs)} orders | untaxed={u_sum:,.2f} | total={t_sum:,.2f}")

print("\n" + "=" * 60)
print("2. RECONCILE WITH REPORT MODELS")
print("=" * 60)

# sale.report reconciliation
sr_domain = [('company_id', '=', 2), ('state', '=', 'sale'), ('date', '>=', '2026-01-01'), ('date', '<', '2027-01-01')]
sr_recs = env['sale.report'].search(sr_domain)
sr_subtotal_sum = sum(sr_recs.mapped('price_subtotal'))
print(f"sale.report price_subtotal: {sr_subtotal_sum:,.2f}")
print(f"sale.order amount_untaxed:   {so_untaxed_sum:,.2f}")
print(f"Difference:                   {sr_subtotal_sum - so_untaxed_sum:,.2f}")

# purchase.report reconciliation
pr_domain = [('company_id', '=', 2), ('state', 'in', ['purchase', 'done']), ('date_order', '>=', '2026-01-01'), ('date_order', '<', '2027-01-01')]
pr_recs = env['purchase.report'].search(pr_domain)

print("\npurchase.report available measure fields:")
pr_fields = env['purchase.report']._fields
for fn in ['untaxed_total', 'price_total', 'price_subtotal', 'price_average']:
    if fn in pr_fields:
        val = sum(pr_recs.mapped(fn))
        print(f"  {fn}: {val:,.2f}")
    else:
        print(f"  {fn}: NOT IN MODEL")

print("\n" + "=" * 60)
print("3. SPREADSHEET.DASHBOARD FIELDS AUDIT (Group Visibility)")
print("=" * 60)
sd_fields = env['spreadsheet.dashboard']._fields
print(f"Available fields on spreadsheet.dashboard:")
for fn, fobj in sorted(sd_fields.items()):
    print(f"  {fn}: {fobj.type} (string='{fobj.string}')")

print("\n" + "=" * 60)
print("4. STOCK QUANT DISTINCT PORTFOLIO SKUS WITH POSITIVE STOCK")
print("=" * 60)
quants = env['stock.quant'].search([
    ('company_id', '=', 2),
    ('location_id.usage', '=', 'internal'),
    ('quantity', '>', 0)
])
distinct_products = set(quants.mapped('product_id.id'))
print(f"Total positive stock quant records: {len(quants)}")
print(f"Distinct products with positive stock: {len(distinct_products)}")
