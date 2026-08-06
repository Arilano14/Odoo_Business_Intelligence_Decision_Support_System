import xmlrpc.client

url = "http://localhost:8070"
db = "Business_Intelegent_Project_v2_fresh_clone"
user = "admin"
password = "admin"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, user, password, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# Check all customers
cust_ids = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['customer_rank', '>', 0]]])
print(f"Total Customer Partners: {len(cust_ids)}")

# Check product variants starting with PORTFOLIO_2026_
prod_ids = models.execute_kw(db, uid, password, 'product.product', 'search', [[['default_code', '=like', 'PORTFOLIO_2026_%']]])
print(f"Total Portfolio Product Variants (product.product): {len(prod_ids)}")

# Fetch sample product mapping
prods = models.execute_kw(db, uid, password, 'product.product', 'read', [prod_ids[:5]], {'fields': ['id', 'default_code', 'name', 'uom_id', 'list_price']})
print("Sample product variants:")
for p in prods:
    print(p)
