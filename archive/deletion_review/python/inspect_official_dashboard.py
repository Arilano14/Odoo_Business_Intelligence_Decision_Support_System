import json, os

fpath = r'C:\Program Files\Odoo 18.0.20241229\sessions\filestore\Business_Intelegent_Project_v2\11\1143df9801d944616c76d9f0ee884f3cb9b2ef1f'
with open(fpath, 'r') as f:
    obj = json.load(f)

print('=== OFFICIAL SALES DASHBOARD (ID 3) - FULL ANATOMY ===')
ver = obj["version"]
print(f'Version: {ver}')

sheets = obj.get('sheets', [])
print(f'Sheets: {len(sheets)}')
for i, s in enumerate(sheets):
    cells = s.get('cells', {})
    figures = s.get('figures', [])
    sname = s.get("name", "unnamed")
    colN = s.get("colNumber", 0)
    rowN = s.get("rowNumber", 0)
    print(f'  Sheet {i}: name={sname} cols={colN} rows={rowN} cells={len(cells)} figures={len(figures)}')
    for fig in figures:
        fid = fig.get("id","?")
        ftag = fig.get("tag","?")
        fw = fig.get("width", 0)
        fh = fig.get("height", 0)
        print(f'    Figure: id={fid} tag={ftag} width={fw} height={fh}')
    # Show cells with formulas
    formula_cells = {k: v for k, v in cells.items() if v.get('content','').startswith('=')}
    print(f'    Formula cells ({len(formula_cells)} total, showing first 10):')
    for k in sorted(formula_cells.keys())[:10]:
        content = formula_cells[k].get('content', '')[:150]
        print(f'      {k}: {content}')

pivot_keys = list(obj.get("pivots", {}).keys())
list_keys = list(obj.get("lists", {}).keys())
print(f'\nPivots: {pivot_keys}')
print(f'Lists: {list_keys}')

gf = obj.get('globalFilters', [])
print(f'GlobalFilters ({len(gf)}):')
for g in gf:
    print(f'  label={g.get("label")} type={g.get("type")} model={g.get("modelName")}')

# Check the sample file path to understand what Odoo generates for official dashboards  
print('\n=== CHECKING SAMPLE FILE PATHS ===')
# Find where odoo stores sample dashboard files
sample_dir = r'C:\Program Files\Odoo 18.0.20241229\server\odoo\addons'
for root, dirs, files in os.walk(sample_dir):
    for fn in files:
        if 'sales_sample_dashboard' in fn:
            fp = os.path.join(root, fn)
            with open(fp, 'r') as sf:
                sample = json.load(sf)
            print(f'Found sample file: {fp}')
            print(f'  Top keys: {sorted(sample.keys())}')
            sv = sample.get("version","?")
            print(f'  Version: {sv}')
            spivots = sample.get("pivots",{})
            slists = sample.get("lists",{})
            print(f'  Pivots: {len(spivots)}')
            for pid, pd in spivots.items():
                print(f'    Pivot {pid}: model={pd.get("model")} measures={pd.get("measures",[])}')
            print(f'  Lists: {len(slists)}')
            for lid, ld in slists.items():
                print(f'    List {lid}: model={ld.get("model")} columns={ld.get("columns",[])}')
