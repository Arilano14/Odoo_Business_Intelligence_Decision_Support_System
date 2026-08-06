# Investigate unknown and non-portfolio transacted products
# And check their impact on dashboard metrics

# Re-gather transacted product IDs
so_lines = env['sale.order.line'].search([
    ('order_id.company_id', '=', 2),
    ('order_id.state', 'in', ['sale', 'done'])
])
po_lines = env['purchase.order.line'].search([
    ('order_id.company_id', '=', 2),
    ('order_id.state', 'in', ['purchase', 'done'])
])
transacted_product_ids = set(so_lines.mapped('product_id.id')) | set(po_lines.mapped('product_id.id'))

# Classify again to identify specific unknown/non-portfolio products
STANDARD_ODOO_NAMES = ['Deposit', 'Discount', 'Down payment', 'Expenses', 'Hotel Accommodation', 'Restaurant Expenses']
STANDARD_ODOO_PREFIXES = ['E-', 'CONS_']

non_portfolio_transacted = []
unknown_products = []

for p in env['product.product'].search([]):
    code = p.default_code or ''
    name = p.name or ''
    categ = p.categ_id.name or ''
    is_transacted = p.id in transacted_product_ids

    is_portfolio = False
    if code and ('_' in code or code.startswith('FURN') or code.startswith('E-COM')):
        if not code.startswith('E-'):
            is_portfolio = True
    if categ in ['All / Saleable', 'All / Saleable / Furniture', 'All / Saleable / Office Furniture']:
        is_portfolio = True

    is_standard = False
    if not is_portfolio:
        if name in STANDARD_ODOO_NAMES or (code and any(code.startswith(pre) for pre in STANDARD_ODOO_PREFIXES)):
            is_standard = True
        elif categ in ['All / Expenses', 'All / Internal']:
            is_standard = True

    if not is_portfolio and not is_standard:
        if is_transacted:
            # Calculate SO and PO amounts for this product
            so_amount = sum(so_lines.filtered(lambda l: l.product_id.id == p.id).mapped('price_subtotal'))
            po_amount = sum(po_lines.filtered(lambda l: l.product_id.id == p.id).mapped('price_subtotal'))
            non_portfolio_transacted.append({
                'id': p.id, 'name': name, 'code': code, 'categ': categ,
                'so_amount': so_amount, 'po_amount': po_amount
            })
        elif not is_transacted:
            unknown_products.append({
                'id': p.id, 'name': name, 'code': code, 'categ': categ,
                'active': p.active
            })

print("=" * 60)
print("NON-PORTFOLIO TRANSACTED PRODUCTS")
print("=" * 60)
for item in non_portfolio_transacted:
    print(f"  ID: {item['id']}, Name: {item['name']}, Code: {item['code']}, Categ: {item['categ']}")
    print(f"    SO Amount: {item['so_amount']}, PO Amount: {item['po_amount']}")

print()
print("=" * 60)
print("UNKNOWN PRODUCTS (NOT TRANSACTED, NOT STANDARD, NOT PORTFOLIO)")
print("=" * 60)
for item in unknown_products:
    print(f"  ID: {item['id']}, Name: {item['name']}, Code: {item['code']}, Categ: {item['categ']}, Active: {item['active']}")

# Total transaction values for context
total_so = sum(so_lines.mapped('price_subtotal'))
total_po = sum(po_lines.mapped('price_subtotal'))
npt_so = sum(item['so_amount'] for item in non_portfolio_transacted)
npt_po = sum(item['po_amount'] for item in non_portfolio_transacted)
print()
print(f"Total SO Value: {total_so}")
print(f"Total PO Value: {total_po}")
print(f"Non-Portfolio Transacted SO Value: {npt_so} ({npt_so/total_so*100 if total_so else 0:.2f}%)")
print(f"Non-Portfolio Transacted PO Value: {npt_po} ({npt_po/total_po*100 if total_po else 0:.2f}%)")

# Check spreadsheet_edition module availability
mod = env['ir.module.module'].search([('name', '=', 'spreadsheet_edition')])
if mod:
    print(f"\nspreadsheet_edition module: state={mod.state}")
else:
    print("\nspreadsheet_edition module: NOT FOUND IN DATABASE")

mod2 = env['ir.module.module'].search([('name', '=', 'spreadsheet_dashboard')])
if mod2:
    print(f"spreadsheet_dashboard module: state={mod2.state}")

mod3 = env['ir.module.module'].search([('name', '=', 'spreadsheet_dashboard_edition')])
if mod3:
    print(f"spreadsheet_dashboard_edition module: state={mod3.state}")
else:
    print("spreadsheet_dashboard_edition module: NOT FOUND IN DATABASE")

# Check if spreadsheet.mixin has any create method available
try:
    dm = env['spreadsheet.dashboard']
    fields = dm._fields.keys()
    print(f"\nspreadsheet.dashboard fields: {list(fields)}")
except Exception as e:
    print(f"\nError inspecting spreadsheet.dashboard: {e}")
