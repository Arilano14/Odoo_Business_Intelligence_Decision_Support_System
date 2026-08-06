import json

fpath = r"C:\Program Files\Odoo 18.0.20241229\server\odoo\addons\spreadsheet_dashboard_website_sale\data\files\ecommerce_dashboard.json"
with open(fpath, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=== ECOMMERCE DASHBOARD JSON ANATOMY ===")
print("Top-level keys:", list(data.keys()))
print("Pivots detail:")
print(json.dumps(data.get("pivots"), indent=2)[:2000])

print("\nGlobal Filters detail:")
print(json.dumps(data.get("globalFilters"), indent=2)[:2000])

sheets = data.get("sheets", [])
for s in sheets:
    print(f"\nSheet '{s.get('name')}': cells={len(s.get('cells', {}))}, figures={len(s.get('figures', []))}")
    for cid, cval in list(s.get("cells", {}).items())[:15]:
        print(f"  Cell {cid}: {cval}")
    for fig in s.get("figures", []):
        print(f"  Figure id={fig.get('id')} tag={fig.get('tag')} data={fig.get('data')}")

