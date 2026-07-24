from odoo.connection import get_connection

def validate():
    uid, models, db, password = get_connection()
    print("\n--- Running Phase 8 Validation ---")
    
    passed = True

    def check(name, actual, expected):
        nonlocal passed
        if actual == expected:
            print(f"[PASS] {name}: {actual}")
        else:
            print(f"[FAIL] {name}: Expected {expected}, got {actual}")
            passed = False

    # 1. Company
    companies = models.execute_kw(db, uid, password, 'res.company', 'search_count', [[('name', '=', 'PT Prima Alat Nusantara')]])
    check("Company 'PT Prima Alat Nusantara'", companies, 1)

    # 2. Warehouse
    warehouses = models.execute_kw(db, uid, password, 'stock.warehouse', 'search_count', [[('code', '=', 'PAN')]])
    check("Warehouse 'PAN'", warehouses, 1)

    # 3. Partners
    custs = models.execute_kw(db, uid, password, 'res.partner', 'search_count', [[('ref', '=like', 'PORTFOLIO_2026_V1-CUST-%')]])
    check("Portfolio Customers", custs, 48)

    supps = models.execute_kw(db, uid, password, 'res.partner', 'search_count', [[('ref', '=like', 'PORTFOLIO_2026_V1-VEND-%')]])
    check("Portfolio Suppliers", supps, 24)

    # 4. Products and Categories
    parent_cat = models.execute_kw(db, uid, password, 'product.category', 'search_count', [[('name', '=', 'Portfolio 2026')]])
    check("Parent Category 'Portfolio 2026'", parent_cat, 1)

    if parent_cat == 1:
        parent_id = models.execute_kw(db, uid, password, 'product.category', 'search_read', [[('name', '=', 'Portfolio 2026')]], {'fields': ['id']})[0]['id']
        child_cats = models.execute_kw(db, uid, password, 'product.category', 'search_count', [[('parent_id', '=', parent_id)]])
        check("Child Categories", child_cats, 5)

    prod_tmpls = models.execute_kw(db, uid, password, 'product.template', 'search_count', [[('default_code', '=like', 'PORTFOLIO_2026_V1-PROD-%')]])
    check("Product Templates", prod_tmpls, 240)

    prod_vars = models.execute_kw(db, uid, password, 'product.product', 'search_count', [[('default_code', '=like', 'PORTFOLIO_2026_V1-PROD-%')]])
    check("Product Variants", prod_vars, 240)

    mappings = models.execute_kw(db, uid, password, 'product.supplierinfo', 'search_read', [[]], {'fields': ['id', 'product_tmpl_id']})
    # Count mappings that belong to our templates
    templates = models.execute_kw(db, uid, password, 'product.template', 'search_read', [[('default_code', '=like', 'PORTFOLIO_2026_V1-PROD-%')]], {'fields': ['id']})
    template_ids = [t['id'] for t in templates]
    portfolio_mappings = len([m for m in mappings if m.get('product_tmpl_id') and m['product_tmpl_id'][0] in template_ids])
    check("Product Supplier Mappings", portfolio_mappings, 456)

    # 5. Zero transactions
    sales = models.execute_kw(db, uid, password, 'sale.order', 'search_count', [['|', ('date_order', '=like', '2024%'), ('date_order', '=like', '2026%')]])
    check("Zero 2024/2026 Sales Orders", sales, 0)

    purchases = models.execute_kw(db, uid, password, 'purchase.order', 'search_count', [['|', ('date_order', '=like', '2024%'), ('date_order', '=like', '2026%')]])
    check("Zero 2024/2026 Purchase Orders", purchases, 0)

    moves = models.execute_kw(db, uid, password, 'account.move', 'search_count', [['|', ('date', '=like', '2024%'), ('date', '=like', '2026%')]])
    check("Zero 2024/2026 Account Moves", moves, 0)

    pickings = models.execute_kw(db, uid, password, 'stock.picking', 'search_count', [['|', ('date', '=like', '2024%'), ('date', '=like', '2026%')]])
    check("Zero 2024/2026 Stock Pickings", pickings, 0)
    
    if passed:
        print("\n[VALIDATION SUCCESS] All conditions met!")
    else:
        print("\n[VALIDATION FAILED] Some conditions were not met.")
