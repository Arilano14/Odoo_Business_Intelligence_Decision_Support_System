import csv
import os

# ============================================================
# AUTHORITATIVE PRODUCT SCOPE GATE
# Exclusive variant-level partition: every active variant
# must appear in exactly ONE classification bucket.
# Total must equal exactly 283 (total active variants).
# ============================================================

# Step 1: Get ALL active product variants
all_active = env['product.product'].search([('active', '=', True)])
print(f"Total active variants: {len(all_active)}")
assert len(all_active) == 283, f"GATE FAILED: Expected 283 active variants, got {len(all_active)}"

# Step 2: Determine transacted variants
# Include ALL confirmed SO lines for company 2 (state = 'sale' or 'done')
so_lines = env['sale.order.line'].search([
    ('order_id.company_id', '=', 2),
    ('order_id.state', 'in', ['sale', 'done'])
])
po_lines = env['purchase.order.line'].search([
    ('order_id.company_id', '=', 2),
    ('order_id.state', 'in', ['purchase', 'done'])
])

# Also check draft/cancel SO/PO to see if any variants show up there
so_lines_all = env['sale.order.line'].search([
    ('order_id.company_id', '=', 2),
])
po_lines_all = env['purchase.order.line'].search([
    ('order_id.company_id', '=', 2),
])

confirmed_so_product_ids = set(so_lines.mapped('product_id.id'))
confirmed_po_product_ids = set(po_lines.mapped('product_id.id'))
all_so_product_ids = set(so_lines_all.mapped('product_id.id'))
all_po_product_ids = set(po_lines_all.mapped('product_id.id'))

confirmed_transacted = confirmed_so_product_ids | confirmed_po_product_ids
all_transacted = all_so_product_ids | all_po_product_ids

print(f"Confirmed SO product IDs: {len(confirmed_so_product_ids)}")
print(f"Confirmed PO product IDs: {len(confirmed_po_product_ids)}")
print(f"Confirmed transacted (union): {len(confirmed_transacted)}")
print(f"All SO product IDs (any state): {len(all_so_product_ids)}")
print(f"All PO product IDs (any state): {len(all_po_product_ids)}")
print(f"All transacted (any state, union): {len(all_transacted)}")

# Also check stock.move for transacted products
stock_moves = env['stock.move'].search([
    ('company_id', '=', 2),
    ('state', '=', 'done')
])
stock_transacted = set(stock_moves.mapped('product_id.id'))
print(f"Stock move transacted: {len(stock_transacted)}")

# Full transacted = any confirmed SO/PO line OR completed stock move
full_transacted = confirmed_transacted | stock_transacted
print(f"Full transacted (confirmed SO/PO + done stock.move): {len(full_transacted)}")

# Step 3: Portfolio classification
# Rules from Phase 8 generator and product master:
# - Products with default_code containing underscore (FURN_xxx, DESK_xxx, etc.)
#   EXCEPT those starting with 'E-' (Odoo expense products)
# - Products in categories that are saleable/furniture-related
#   created by the Phase 8 generator
#
# Standard Odoo products:
# - Products with names matching known Odoo defaults
# - Products in expense/internal categories
# - Products with E- or CONS_ prefix codes

# Get all category names for reference
all_categs = set()
for p in all_active:
    full_categ = p.categ_id.complete_name or p.categ_id.name or ''
    all_categs.add(full_categ)

print(f"\nAll product categories present:")
for c in sorted(all_categs):
    count = len([p for p in all_active if (p.categ_id.complete_name or p.categ_id.name or '') == c])
    print(f"  {c}: {count}")

# Portfolio detection: reproducible rules
PORTFOLIO_CATEGORIES = set()
NON_PORTFOLIO_CATEGORIES = set()
STANDARD_ODOO_CATEGORIES = set()

# Let me inspect every category and decide
for c in sorted(all_categs):
    c_lower = c.lower()
    if any(kw in c_lower for kw in ['expense', 'internal']):
        STANDARD_ODOO_CATEGORIES.add(c)
    elif any(kw in c_lower for kw in ['service']):
        NON_PORTFOLIO_CATEGORIES.add(c)
    else:
        # Assume generated portfolio category
        PORTFOLIO_CATEGORIES.add(c)

print(f"\nPortfolio categories: {sorted(PORTFOLIO_CATEGORIES)}")
print(f"Non-portfolio categories: {sorted(NON_PORTFOLIO_CATEGORIES)}")
print(f"Standard Odoo categories: {sorted(STANDARD_ODOO_CATEGORIES)}")

# Standard Odoo product names (known defaults)
STANDARD_ODOO_NAMES = {
    'Deposit', 'Discount', 'Down payment', 'Down Payment',
    'Expenses', 'Hotel Accommodation', 'Restaurant Expenses'
}

# Now classify each variant exclusively
rows = []  # For CSV output
partition = {
    'portfolio_transacted': [],
    'portfolio_non_transacted': [],
    'non_portfolio_transacted': [],
    'standard_default_non_transacted': [],
    'unknown_transacted': [],
    'unknown_non_transacted': [],
}

for p in all_active:
    pid = p.id
    tmpl_id = p.product_tmpl_id.id
    name = p.name or ''
    code = p.default_code or ''
    categ = p.categ_id.complete_name or p.categ_id.name or ''
    is_confirmed_transacted = pid in confirmed_transacted
    is_full_transacted = pid in full_transacted
    
    # Use full_transacted as "transacted" definition
    is_transacted = is_full_transacted

    # Classification: determine if portfolio, standard, or unknown
    classification = None
    
    # Rule 1: Check if it's a known standard Odoo product
    is_standard = False
    if name in STANDARD_ODOO_NAMES:
        is_standard = True
    elif code and code.startswith('E-'):
        is_standard = True
    elif code and code.startswith('CONS_'):
        is_standard = True
    elif categ in STANDARD_ODOO_CATEGORIES:
        is_standard = True
    
    # Rule 2: Check if it's a non-portfolio service
    is_non_portfolio_service = False
    if categ in NON_PORTFOLIO_CATEGORIES:
        is_non_portfolio_service = True
    
    # Rule 3: Check if it's a portfolio product
    is_portfolio = False
    if not is_standard and not is_non_portfolio_service:
        if categ in PORTFOLIO_CATEGORIES:
            is_portfolio = True
    
    # Assign to exactly one bucket
    if is_portfolio:
        if is_transacted:
            classification = 'portfolio_transacted'
        else:
            classification = 'portfolio_non_transacted'
    elif is_standard:
        if is_transacted:
            classification = 'non_portfolio_transacted'  # standard but transacted
        else:
            classification = 'standard_default_non_transacted'
    elif is_non_portfolio_service:
        if is_transacted:
            classification = 'non_portfolio_transacted'
        else:
            classification = 'standard_default_non_transacted'  # non-transacted service
    else:
        # Should not reach here if categories are exhaustive
        if is_transacted:
            classification = 'unknown_transacted'
        else:
            classification = 'unknown_non_transacted'
    
    partition[classification].append(pid)
    rows.append({
        'variant_id': pid,
        'template_id': tmpl_id,
        'name': name,
        'default_code': code,
        'category': categ,
        'is_confirmed_transacted': is_confirmed_transacted,
        'is_full_transacted': is_transacted,
        'classification': classification,
    })

# Print exclusive partition
print(f"\n{'='*60}")
print(f"EXCLUSIVE VARIANT-LEVEL PARTITION")
print(f"{'='*60}")
total = 0
for cls_name in ['portfolio_transacted', 'portfolio_non_transacted', 
                  'non_portfolio_transacted', 'standard_default_non_transacted',
                  'unknown_transacted', 'unknown_non_transacted']:
    count = len(partition[cls_name])
    total += count
    print(f"| {cls_name:40s} | {count:4d} |")
print(f"| {'TOTAL':40s} | {total:4d} |")

# Verify total
if total != 283:
    print(f"\n*** GATE FAILED: Total {total} != 283 ***")
    # Debug: find which variants are missing
    classified_ids = set()
    for v in partition.values():
        classified_ids.update(v)
    all_ids = set(all_active.ids)
    missing = all_ids - classified_ids
    dupes = [pid for pid in classified_ids if sum(1 for v in partition.values() if pid in v) > 1]
    print(f"Missing from partition: {missing}")
    print(f"Duplicated in partition: {dupes}")
else:
    print(f"\n*** GATE CHECK: Total matches 283 ***")

# Verify no duplicates
all_classified = []
for v in partition.values():
    all_classified.extend(v)
if len(all_classified) != len(set(all_classified)):
    print("*** GATE FAILED: Duplicate variants found ***")
else:
    print("*** GATE CHECK: No duplicates ***")

# Transacted reconciliation
transacted_in_partition = len(partition['portfolio_transacted']) + len(partition['non_portfolio_transacted']) + len(partition['unknown_transacted'])
print(f"\nTransacted in partition: {transacted_in_partition}")
print(f"Full transacted set: {len(full_transacted)}")

# Check if all full_transacted are covered
transacted_partition_ids = set(partition['portfolio_transacted']) | set(partition['non_portfolio_transacted']) | set(partition['unknown_transacted'])
# Some transacted products might be inactive (not in our 283)
active_transacted = full_transacted & set(all_active.ids)
missing_transacted = active_transacted - transacted_partition_ids
if missing_transacted:
    print(f"*** WARNING: {len(missing_transacted)} active transacted variants not in transacted partition ***")
    for pid in missing_transacted:
        p = env['product.product'].browse(pid)
        print(f"  ID: {pid}, Name: {p.name}, Code: {p.default_code}, Categ: {p.categ_id.complete_name}")
else:
    print("*** GATE CHECK: All active transacted variants accounted for ***")

# Save CSV
docs_dir = 'c:/Users/Arilano/Downloads/Project ARICE/Project Odoo/docs/phase11_2_programmatic'
os.makedirs(docs_dir, exist_ok=True)

csv_path = os.path.join(docs_dir, 'product_scope_partition.csv')
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['variant_id', 'template_id', 'name', 'default_code', 'category', 'is_confirmed_transacted', 'is_full_transacted', 'classification'])
    writer.writeheader()
    for row in sorted(rows, key=lambda r: (r['classification'], r['variant_id'])):
        writer.writerow(row)

print(f"\nSaved partition CSV to: {csv_path}")

# Print details of non-portfolio transacted and unknown
print(f"\n{'='*60}")
print("NON-PORTFOLIO TRANSACTED DETAILS:")
print(f"{'='*60}")
for pid in partition['non_portfolio_transacted']:
    p = env['product.product'].browse(pid)
    print(f"  ID: {pid}, Name: {p.name}, Code: {p.default_code}, Categ: {p.categ_id.complete_name}")

print(f"\n{'='*60}")
print("UNKNOWN TRANSACTED DETAILS:")
print(f"{'='*60}")
for pid in partition['unknown_transacted']:
    p = env['product.product'].browse(pid)
    print(f"  ID: {pid}, Name: {p.name}, Code: {p.default_code}, Categ: {p.categ_id.complete_name}")

print(f"\n{'='*60}")
print("UNKNOWN NON-TRANSACTED DETAILS:")
print(f"{'='*60}")
for pid in partition['unknown_non_transacted']:
    p = env['product.product'].browse(pid)
    print(f"  ID: {pid}, Name: {p.name}, Code: {p.default_code}, Categ: {p.categ_id.complete_name}")

# Save verified portfolio product IDs
verified_ids = sorted(set(partition['portfolio_transacted']) | set(partition['portfolio_non_transacted']))
with open(os.path.join(docs_dir, 'verified_portfolio_product_ids.txt'), 'w') as f:
    f.write(','.join(map(str, verified_ids)))
print(f"\nSaved {len(verified_ids)} verified portfolio product IDs")
