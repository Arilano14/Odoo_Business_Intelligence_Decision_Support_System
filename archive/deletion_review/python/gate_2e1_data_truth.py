"""
GATE 2E.1 — FINAL DATA TRUTH
All queries filtered by company_id=2 AND FY2026 date range.
"""
import psycopg2
import csv
import os

conn = psycopg2.connect(host='localhost', port=5432, user='openpg', password='openpgpwd', dbname='Business_Intelegent_Project_v2')
cur = conn.cursor()

print("=" * 80)
print("GATE 2E.1 — FINAL DATA TRUTH (company_id=2, FY2026)")
print("=" * 80)

# ──────────────────────────────────────────────────────
# 1. SALE ORDERS
# ──────────────────────────────────────────────────────
print("\n=== SALE ORDERS ===")

# All-company total (for context)
cur.execute("SELECT COUNT(*) FROM sale_order")
so_all = cur.fetchone()[0]
print(f"  All-company total: {so_all}")

# Company 2 FY2026
cur.execute("""
    SELECT COUNT(*), COALESCE(SUM(amount_total), 0)
    FROM sale_order
    WHERE company_id = 2
      AND date_order >= DATE '2026-01-01'
      AND date_order < DATE '2027-01-01'
""")
so_c2, so_c2_sum = cur.fetchone()
print(f"  Company 2 FY2026 total: {so_c2} | Revenue: {so_c2_sum:,.2f}")

# By state
cur.execute("""
    SELECT state, COUNT(*), COALESCE(SUM(amount_total), 0)
    FROM sale_order
    WHERE company_id = 2
      AND date_order >= DATE '2026-01-01'
      AND date_order < DATE '2027-01-01'
    GROUP BY state
    ORDER BY COUNT(*) DESC
""")
print("  By state:")
for row in cur.fetchall():
    print(f"    {row[0]:15s}: {row[1]:5d} orders | {row[2]:>20,.2f}")

# Records outside company_id=2 or FY2026
cur.execute("""
    SELECT COUNT(*) FROM sale_order
    WHERE company_id != 2 OR date_order < DATE '2026-01-01' OR date_order >= DATE '2027-01-01'
""")
so_excluded = cur.fetchone()[0]
print(f"  Records excluded (other company/year): {so_excluded}")

# ──────────────────────────────────────────────────────
# 2. PURCHASE ORDERS — WITH DISCREPANCY INVESTIGATION
# ──────────────────────────────────────────────────────
print("\n=== PURCHASE ORDERS ===")

# All-company total
cur.execute("SELECT COUNT(*) FROM purchase_order")
po_all = cur.fetchone()[0]
print(f"  All-company total: {po_all}")

# Company 2 FY2026
cur.execute("""
    SELECT COUNT(*), COALESCE(SUM(amount_total), 0)
    FROM purchase_order
    WHERE company_id = 2
      AND date_order >= DATE '2026-01-01'
      AND date_order < DATE '2027-01-01'
""")
po_c2, po_c2_sum = cur.fetchone()
print(f"  Company 2 FY2026 total: {po_c2} | Value: {po_c2_sum:,.2f}")

# By state
cur.execute("""
    SELECT state, COUNT(*), COALESCE(SUM(amount_total), 0)
    FROM purchase_order
    WHERE company_id = 2
      AND date_order >= DATE '2026-01-01'
      AND date_order < DATE '2027-01-01'
    GROUP BY state
    ORDER BY COUNT(*) DESC
""")
print("  By state:")
for row in cur.fetchall():
    print(f"    {row[0]:15s}: {row[1]:5d} orders | {row[2]:>20,.2f}")

# Records outside company_id=2 or FY2026
cur.execute("""
    SELECT COUNT(*) FROM purchase_order
    WHERE company_id != 2 OR date_order < DATE '2026-01-01' OR date_order >= DATE '2027-01-01'
""")
po_excluded = cur.fetchone()[0]
print(f"  Records excluded (other company/year): {po_excluded}")

# DISCREPANCY INVESTIGATION: Previous reports said 251, then 253
# Find ALL POs sorted by id to find the 2 newest ones
print("\n  --- PO DISCREPANCY INVESTIGATION (251 vs 253) ---")
cur.execute("""
    SELECT id, name, state, company_id, date_order, amount_total, partner_id,
           create_date, create_uid
    FROM purchase_order
    ORDER BY id DESC
    LIMIT 10
""")
print("  Last 10 Purchase Orders (by ID desc):")
for row in cur.fetchall():
    print(f"    PO id={row[0]} name={row[1]} state={row[2]} company={row[3]} "
          f"date={row[4]} amount={row[5]:,.2f} partner={row[6]} "
          f"created={row[7]} by_uid={row[8]}")

# Check for POs outside company 2 or FY2026
cur.execute("""
    SELECT id, name, state, company_id, date_order, amount_total
    FROM purchase_order
    WHERE company_id != 2
    ORDER BY id
""")
other_company_pos = cur.fetchall()
print(f"\n  POs from other companies: {len(other_company_pos)}")
for row in other_company_pos:
    print(f"    PO id={row[0]} name={row[1]} state={row[2]} company={row[3]} date={row[4]} amount={row[5]}")

cur.execute("""
    SELECT id, name, state, company_id, date_order, amount_total
    FROM purchase_order
    WHERE date_order < DATE '2026-01-01' OR date_order >= DATE '2027-01-01'
    ORDER BY id
""")
other_date_pos = cur.fetchall()
print(f"\n  POs outside FY2026: {len(other_date_pos)}")
for row in other_date_pos:
    print(f"    PO id={row[0]} name={row[1]} state={row[2]} company={row[3]} date={row[4]} amount={row[5]}")

# ──────────────────────────────────────────────────────
# 3. PRODUCTS  
# ──────────────────────────────────────────────────────
print("\n=== PRODUCTS ===")

# Company-scoped products (products referenced in company 2 FY2026 SOs/POs)
cur.execute("""
    SELECT COUNT(DISTINCT sol.product_id)
    FROM sale_order_line sol
    JOIN sale_order so ON sol.order_id = so.id
    WHERE so.company_id = 2
      AND so.date_order >= DATE '2026-01-01'
      AND so.date_order < DATE '2027-01-01'
""")
products_in_so = cur.fetchone()[0]
print(f"  Products referenced in Company 2 FY2026 SOs: {products_in_so}")

cur.execute("""
    SELECT COUNT(DISTINCT pol.product_id)
    FROM purchase_order_line pol
    JOIN purchase_order po ON pol.order_id = po.id
    WHERE po.company_id = 2
      AND po.date_order >= DATE '2026-01-01'
      AND po.date_order < DATE '2027-01-01'
""")
products_in_po = cur.fetchone()[0]
print(f"  Products referenced in Company 2 FY2026 POs: {products_in_po}")

# Total active products (all companies)
cur.execute("SELECT COUNT(*) FROM product_product WHERE active = true")
all_active = cur.fetchone()[0]
print(f"  All active product variants (all companies): {all_active}")

cur.execute("SELECT COUNT(*) FROM product_template WHERE active = true")
all_templates = cur.fetchone()[0]
print(f"  All active product templates (all companies): {all_templates}")

# Portfolio products (union of SO and PO products)
cur.execute("""
    SELECT COUNT(DISTINCT product_id) FROM (
        SELECT DISTINCT sol.product_id
        FROM sale_order_line sol
        JOIN sale_order so ON sol.order_id = so.id
        WHERE so.company_id = 2
          AND so.date_order >= DATE '2026-01-01'
          AND so.date_order < DATE '2027-01-01'
        UNION
        SELECT DISTINCT pol.product_id
        FROM purchase_order_line pol
        JOIN purchase_order po ON pol.order_id = po.id
        WHERE po.company_id = 2
          AND po.date_order >= DATE '2026-01-01'
          AND po.date_order < DATE '2027-01-01'
    ) portfolio
""")
portfolio_valid = cur.fetchone()[0]
print(f"  Valid portfolio products (Company 2 FY2026): {portfolio_valid}")

# ──────────────────────────────────────────────────────
# 4. ACCOUNTING
# ──────────────────────────────────────────────────────
print("\n=== ACCOUNTING ===")

cur.execute("""
    SELECT move_type, COUNT(*)
    FROM account_move
    WHERE company_id = 2
    GROUP BY move_type
    ORDER BY COUNT(*) DESC
""")
print("  Account moves by type (Company 2):")
for row in cur.fetchall():
    print(f"    {row[0]:20s}: {row[1]}")

cur.execute("""
    SELECT COUNT(*) FROM account_move
    WHERE company_id = 2 AND move_type = 'out_invoice'
      AND date >= DATE '2026-01-01' AND date < DATE '2027-01-01'
""")
cust_inv = cur.fetchone()[0]
print(f"  Customer Invoices (Company 2 FY2026): {cust_inv}")

cur.execute("""
    SELECT COUNT(*) FROM account_move
    WHERE company_id = 2 AND move_type = 'in_invoice'
      AND date >= DATE '2026-01-01' AND date < DATE '2027-01-01'
""")
vend_bills = cur.fetchone()[0]
print(f"  Vendor Bills (Company 2 FY2026): {vend_bills}")

# ──────────────────────────────────────────────────────
# 5. INVENTORY
# ──────────────────────────────────────────────────────
print("\n=== INVENTORY ===")

cur.execute("""
    SELECT COUNT(*) FROM stock_quant WHERE company_id = 2
""")
quants_c2 = cur.fetchone()[0]
print(f"  Stock quants (Company 2): {quants_c2}")

cur.execute("""
    SELECT COUNT(*) FROM stock_picking
    WHERE company_id = 2
      AND state = 'done'
      AND date_done >= '2026-01-01' AND date_done < '2027-01-01'
""")
pickings_c2 = cur.fetchone()[0]
print(f"  Done pickings (Company 2 FY2026): {pickings_c2}")

cur.execute("""
    SELECT picking_type_id, COUNT(*)
    FROM stock_picking
    WHERE company_id = 2
      AND state = 'done'
    GROUP BY picking_type_id
    ORDER BY COUNT(*) DESC
""")
print("  Done pickings by type (Company 2 all dates):")
for row in cur.fetchall():
    print(f"    type_id={row[0]}: {row[1]}")

# ──────────────────────────────────────────────────────
# 6. EXPORT PO DISCREPANCY CSV
# ──────────────────────────────────────────────────────
docs_dir = r"c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\docs\phase11_2_live"
os.makedirs(docs_dir, exist_ok=True)

cur.execute("""
    SELECT id, name, state, company_id, date_order, amount_total, partner_id,
           create_date, create_uid
    FROM purchase_order
    ORDER BY id
""")
all_pos = cur.fetchall()

csv_path = os.path.join(docs_dir, "purchase_order_discrepancy.csv")
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['id', 'name', 'state', 'company_id', 'date_order', 'amount_total',
                'partner_id', 'create_date', 'create_uid', 'classification'])
    for row in all_pos:
        # Classify
        co = row[3]
        dt = row[4]
        if co != 2:
            classification = "OTHER_COMPANY"
        elif dt and (dt.year < 2026 or dt.year >= 2027):
            classification = "OTHER_YEAR"
        else:
            classification = "VALID_PORTFOLIO"
        w.writerow(list(row) + [classification])

print(f"\n  PO discrepancy CSV written to: {csv_path}")
print(f"  Total POs: {len(all_pos)}")

# Summary
print("\n" + "=" * 80)
print("GATE 2E.1 — SUMMARY TABLE")
print("=" * 80)
print(f"{'Entity':<35s} | {'All-co total':>12s} | {'Co2 FY2026':>12s} | {'Valid':>8s} | {'Excluded':>8s}")
print("-" * 80)
print(f"{'Sale Orders':<35s} | {so_all:>12d} | {so_c2:>12d} | {so_c2:>8d} | {so_excluded:>8d}")
print(f"{'Purchase Orders':<35s} | {po_all:>12d} | {po_c2:>12d} | {po_c2:>8d} | {po_excluded:>8d}")
print(f"{'Product Variants (active)':<35s} | {all_active:>12d} | {'N/A':>12s} | {portfolio_valid:>8d} | {'N/A':>8s}")
print(f"{'Product Templates (active)':<35s} | {all_templates:>12d} | {'N/A':>12s} | {'N/A':>8s} | {'N/A':>8s}")
print(f"{'Customer Invoices':<35s} | {'':>12s} | {cust_inv:>12d} | {cust_inv:>8d} | {'':>8s}")
print(f"{'Vendor Bills':<35s} | {'':>12s} | {vend_bills:>12d} | {vend_bills:>8d} | {'':>8s}")
print(f"{'Stock Quants':<35s} | {'':>12s} | {quants_c2:>12d} | {quants_c2:>8d} | {'':>8s}")
print(f"{'Done Pickings':<35s} | {'':>12s} | {pickings_c2:>12d} | {pickings_c2:>8d} | {'':>8s}")

cur.close()
conn.close()
