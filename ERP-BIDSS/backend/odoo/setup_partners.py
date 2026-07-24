import random
from .connection import get_connection

def setup_partners():
    uid, models, db, password = get_connection()
    print("\n--- Setup Partners ---")
    
    random.seed(26072026)

    # Base names for generation
    prefixes = ['PT', 'CV', 'UD']
    customer_keywords = ['Tambang', 'Konstruksi', 'Bina', 'Infrastruktur', 'Energi', 'Logistik', 'Agro', 'Karya', 'Makmur', 'Jaya', 'Nusantara', 'Persada', 'Abadi', 'Sejahtera', 'Mandiri']
    supplier_keywords = ['Teknik', 'Mesin', 'Sparepart', 'Global', 'Oto', 'Diesel', 'Hydraulic', 'Filtrasi', 'Tractor', 'Motor', 'Part', 'Industri']

    def generate_names(count, keywords, prefix='BIDSS'):
        names = set()
        while len(names) < count:
            pref = random.choice(prefixes)
            kw1 = random.choice(keywords)
            kw2 = random.choice(keywords)
            if kw1 != kw2:
                name = f"{pref} {kw1} {kw2}"
                names.add(name)
        return list(names)

    customers = generate_names(48, customer_keywords)
    suppliers = generate_names(24, supplier_keywords)

    customer_records = []
    for i, name in enumerate(customers, 1):
        customer_records.append({
            'name': name,
            'ref': f'PORTFOLIO_2026_V1-CUST-{i:03d}',
            'customer_rank': 1,
            'supplier_rank': 0,
            'is_company': True
        })

    supplier_records = []
    for i, name in enumerate(suppliers, 1):
        supplier_records.append({
            'name': name,
            'ref': f'PORTFOLIO_2026_V1-VEND-{i:03d}',
            'customer_rank': 0,
            'supplier_rank': 1,
            'is_company': True
        })

    # Check existing to ensure idempotency
    existing_custs = models.execute_kw(db, uid, password, 'res.partner', 'search_count', [[('ref', '=like', 'PORTFOLIO_2026_V1-CUST-%')]])
    if existing_custs == 0:
        print(f"Creating {len(customer_records)} customers...")
        for c in customer_records:
            models.execute_kw(db, uid, password, 'res.partner', 'create', [c])
    else:
        print(f"Found {existing_custs} existing customers. Skipping creation.")

    existing_vends = models.execute_kw(db, uid, password, 'res.partner', 'search_count', [[('ref', '=like', 'PORTFOLIO_2026_V1-VEND-%')]])
    if existing_vends == 0:
        print(f"Creating {len(supplier_records)} suppliers...")
        for s in supplier_records:
            models.execute_kw(db, uid, password, 'res.partner', 'create', [s])
    else:
        print(f"Found {existing_vends} existing suppliers. Skipping creation.")

