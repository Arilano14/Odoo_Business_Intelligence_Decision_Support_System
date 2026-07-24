from .connection import get_connection

def setup_company():
    uid, models, db, password = get_connection()
    print("\n--- Setup Company ---")

    # Reuse existing active internal company
    companies = models.execute_kw(db, uid, password, 'res.company', 'search_read', [[]], {'fields': ['id', 'name']})
    if not companies:
        print("ERROR: No company found to reuse.")
        return
    
    # We use the first one (usually ID 1, My Company)
    main_company_id = companies[0]['id']
    
    # Get IDR currency
    currencies = models.execute_kw(db, uid, password, 'res.currency', 'search_read', [[('name', '=', 'IDR')]], {'fields': ['id']})
    if not currencies:
        print("ERROR: IDR currency not found.")
        return
    idr_id = currencies[0]['id']

    # Update company
    models.execute_kw(db, uid, password, 'res.company', 'write', [[main_company_id], {
        'name': 'PT Prima Alat Nusantara',
        'currency_id': idr_id
    }])
    print(f"Updated company {main_company_id} to PT Prima Alat Nusantara (IDR).")

    # Rename the main warehouse
    warehouses = models.execute_kw(db, uid, password, 'stock.warehouse', 'search_read', [[('company_id', '=', main_company_id)]], {'fields': ['id']})
    if warehouses:
        main_wh_id = warehouses[0]['id']
        models.execute_kw(db, uid, password, 'stock.warehouse', 'write', [[main_wh_id], {
            'name': 'PAN Main Warehouse',
            'code': 'PAN'
        }])
        print(f"Updated warehouse {main_wh_id} to PAN Main Warehouse.")
