import psycopg2
conn = psycopg2.connect(host='localhost', port=5432, user='openpg', password='openpgpwd', dbname='Business_Intelegent_Project_v2')
cur = conn.cursor()

print('=== PT PRIMA ALAT NUSANTARA - CURRENT DATA TRUTH ===')

queries = [
    ('SO (all)', "SELECT COUNT(*) FROM sale_order"),
    ('SO (confirmed/sale)', "SELECT COUNT(*) FROM sale_order WHERE state = 'sale'"),
    ('PO (all)', "SELECT COUNT(*) FROM purchase_order"),
    ('PO (confirmed/purchase)', "SELECT COUNT(*) FROM purchase_order WHERE state = 'purchase'"),
    ('product.product (active)', "SELECT COUNT(*) FROM product_product WHERE active = true"),
    ('product.template (active)', "SELECT COUNT(*) FROM product_template WHERE active = true"),
    ('account.move (customer invoices)', "SELECT COUNT(*) FROM account_move WHERE move_type = 'out_invoice'"),
    ('account.move (vendor bills)', "SELECT COUNT(*) FROM account_move WHERE move_type = 'in_invoice'"),
    ('stock.picking (done)', "SELECT COUNT(*) FROM stock_picking WHERE state = 'done'"),
    ('stock.quant', "SELECT COUNT(*) FROM stock_quant"),
    ('Confirmed Sales Revenue', "SELECT SUM(amount_total) FROM sale_order WHERE state = 'sale'"),
    ('Confirmed Purchase Value', "SELECT SUM(amount_total) FROM purchase_order WHERE state = 'purchase'"),
]

for label, q in queries:
    try:
        cur.execute(q)
        val = cur.fetchone()[0]
        if isinstance(val, float):
            print(f'  {label}: {val:,.2f}')
        else:
            print(f'  {label}: {val}')
    except Exception as e:
        print(f'  {label}: ERROR - {e}')
        conn.rollback()

print()
print('=== COMPANIES ===')
cur.execute("SELECT id, name FROM res_company ORDER BY id")
for row in cur.fetchall():
    print(f'  Company {row[0]}: {row[1]}')

print()
print('=== OBIDSS MODULE STATUS ===')
cur.execute("SELECT name, state, latest_version FROM ir_module_module WHERE name = 'obidss_operational_bi'")
row = cur.fetchone()
if row:
    print(f'  Module: {row[0]} | State: {row[1]} | Version: {row[2]}')
else:
    print('  Module NOT found in ir_module_module!')

print()
print('=== DASHBOARD RECORDS ===')
cur.execute("""
    SELECT d.id, d.name->>'en_US', d.is_published, d.sequence,
           g.name->>'en_US' as group_name, d.sample_dashboard_file_path
    FROM spreadsheet_dashboard d
    LEFT JOIN spreadsheet_dashboard_group g ON d.dashboard_group_id = g.id
    ORDER BY d.id
""")
for row in cur.fetchall():
    print(f'  Dash {row[0]:2d}: {row[1]:40s} | published={row[2]} | seq={row[3]} | group={row[4]} | sample_path={row[5]}')

print()
print('=== ALL MENUS WITH OBIDSS OR DASHBOARDS ===')
cur.execute("""
    SELECT m.id, m.name->>'en_US' as name, m.parent_id, m.sequence, m.action
    FROM ir_ui_menu m
    WHERE m.name::text ILIKE '%%obidss%%' 
       OR m.name::text ILIKE '%%dashboard%%'
       OR m.name::text ILIKE '%%executive%%'
    ORDER BY m.id
""")
for row in cur.fetchall():
    print(f'  Menu {row[0]:4d}: {str(row[1]):35s} | parent_id={row[2]} | seq={row[3]} | action={row[4]}')

cur.close()
conn.close()
