import random
from .connection import get_connection

def setup_products():
    uid, models, db, password = get_connection()
    print("\n--- Setup Products and Categories ---")
    
    random.seed(26072026)

    # 1. Setup Categories
    categories = [
        "Heavy Equipment",
        "Engine and Hydraulic Parts",
        "Undercarriage Parts",
        "Filters and Maintenance Parts",
        "Consumables"
    ]
    
    # Check parent category
    parent_cat_id = None
    existing_parent = models.execute_kw(db, uid, password, 'product.category', 'search_read', [[('name', '=', 'Portfolio 2026')]], {'fields': ['id']})
    if existing_parent:
        parent_cat_id = existing_parent[0]['id']
    else:
        parent_cat_id = models.execute_kw(db, uid, password, 'product.category', 'create', [{'name': 'Portfolio 2026'}])
        print("Created parent category: Portfolio 2026")

    cat_ids = {}
    for cat in categories:
        existing_cat = models.execute_kw(db, uid, password, 'product.category', 'search_read', [[('name', '=', cat), ('parent_id', '=', parent_cat_id)]], {'fields': ['id']})
        if existing_cat:
            cat_ids[cat] = existing_cat[0]['id']
        else:
            cat_ids[cat] = models.execute_kw(db, uid, password, 'product.category', 'create', [{
                'name': cat,
                'parent_id': parent_cat_id
            }])
            print(f"Created category: {cat}")

    # 2. Setup Products (240 total)
    existing_prods = models.execute_kw(db, uid, password, 'product.template', 'search_count', [[('default_code', '=like', 'PORTFOLIO_2026_V1-PROD-%')]])
    product_ids = []
    
    if existing_prods == 240:
        print("Found 240 existing products. Skipping creation.")
        # Fetch them for mappings
        prods = models.execute_kw(db, uid, password, 'product.template', 'search_read', [[('default_code', '=like', 'PORTFOLIO_2026_V1-PROD-%')]], {'fields': ['id']})
        product_ids = [p['id'] for p in prods]
    else:
        print("Generating 240 products...")
        product_records = []
        for i in range(1, 241):
            # distribute evenly among 5 categories
            cat_name = categories[(i-1) % 5]
            cat_id = cat_ids[cat_name]
            
            cost = random.randint(10, 1000) * 1000
            price = cost * random.uniform(1.1, 1.5)
            
            product_records.append({
                'name': f"{cat_name} Item {i:03d}",
                'default_code': f"PORTFOLIO_2026_V1-PROD-{i:03d}",
                'list_price': price,
                'standard_price': cost,
                'type': 'consu',
                'is_storable': True,
                'categ_id': cat_id,
            })
            
        for p in product_records:
            pid = models.execute_kw(db, uid, password, 'product.template', 'create', [p])
            product_ids.append(pid)

    # 3. Setup Supplier Mappings (456 total)
    print("\n--- Setup Supplier Mappings ---")
    suppliers = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[('ref', '=like', 'PORTFOLIO_2026_V1-VEND-%')]], {'fields': ['id']})
    supplier_ids = [s['id'] for s in suppliers]
    
    if not supplier_ids:
        print("ERROR: No portfolio suppliers found.")
        return

    existing_mappings = models.execute_kw(db, uid, password, 'product.supplierinfo', 'search_count', [[('product_tmpl_id', 'in', product_ids)]])
    if existing_mappings == 456:
        print("Found 456 existing supplier mappings. Skipping creation.")
    else:
        print("Generating 456 supplier mappings...")
        # 48 products with 1 supplier
        # 168 products with 2 suppliers
        # 24 products with 3 suppliers
        distribution = [1] * 48 + [2] * 168 + [3] * 24
        random.shuffle(distribution) # shuffle so it's not the same categories getting same counts
        
        mapping_records = []
        for prod_id, num_suppliers in zip(product_ids, distribution):
            selected_suppliers = random.sample(supplier_ids, num_suppliers)
            for i, supp_id in enumerate(selected_suppliers):
                mapping_records.append({
                    'product_tmpl_id': prod_id,
                    'partner_id': supp_id,
                    'sequence': i + 1,
                    'delay': random.randint(1, 14),
                    'min_qty': 1,
                    'price': random.randint(10, 1000) * 1000 # generic price
                })
        
        # Batch create if possible, but Odoo create sometimes doesn't like huge batches of supplierinfo, we'll do it one by one
        for m in mapping_records:
            models.execute_kw(db, uid, password, 'product.supplierinfo', 'create', [m])

    print("Product setup finished.")
