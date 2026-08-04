import json

fpath = r'C:\Program Files\Odoo 18.0.20241229\sessions\filestore\Business_Intelegent_Project_v2\11\1143df9801d944616c76d9f0ee884f3cb9b2ef1f'
with open(fpath, 'r') as f:
    obj = json.load(f)

# Examine chart definitions  
sheets = obj.get('sheets', [])
for i, s in enumerate(sheets):
    figures = s.get('figures', [])
    if figures:
        print(f'Sheet {i} ("{s.get("name")}"): {len(figures)} figures')
        for fi, fig in enumerate(figures):
            print(f'\n  Figure {fi}: id={fig.get("id")} tag={fig.get("tag")}')
            data = fig.get("data", {})
            print(f'    data keys: {sorted(data.keys())}')
            print(f'    type: {data.get("type")}')
            print(f'    title: {data.get("title")}')
            ds = data.get("dataSets", [])
            print(f'    dataSets count: {len(ds)}')
            for di, d in enumerate(ds[:2]):
                print(f'      dataSet {di}: {json.dumps(d)[:200]}')
            ld = data.get("labelRange")
            print(f'    labelRange: {ld}')

# Now look at the cell formulas more deeply - the Data sheet
data_sheet = sheets[1] if len(sheets) > 1 else None
if data_sheet:
    cells = data_sheet.get("cells", {})
    print(f'\n=== DATA SHEET CELLS ({len(cells)} total) ===')
    for k in sorted(cells.keys()):
        v = cells[k]
        content = v.get("content", "")
        print(f'  {k:6s}: {content}')

# Also check if there are Odoo chart formulas referencing data
dash_sheet = sheets[0]
cells0 = dash_sheet.get("cells", {})
print(f'\n=== DASHBOARD SHEET CELLS ({len(cells0)} total) ===')
for k in sorted(cells0.keys()):
    v = cells0[k]
    content = v.get("content", "")
    print(f'  {k:6s}: {content[:200]}')
