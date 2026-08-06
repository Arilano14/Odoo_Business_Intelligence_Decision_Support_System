import json
import glob
import os

print("=" * 80)
print("INSPECTING ODOO 18 SPREADSHEET DASHBOARD JSON SCHEMAS FROM CORE ADDONS")
print("=" * 80)

base_dir = r"C:\Program Files\Odoo 18.0.20241229\server\odoo\addons"
json_files = glob.glob(os.path.join(base_dir, "spreadsheet_dashboard*", "data", "files", "*.json"))

print(f"Found {len(json_files)} official dashboard JSON files:")
for jf in json_files:
    fname = os.path.basename(jf)
    modname = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(jf))))
    with open(jf, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    ver = data.get("version")
    pivots = data.get("pivots", {})
    lists = data.get("lists", {})
    gfilters = data.get("globalFilters", [])
    sheets = data.get("sheets", [])
    
    fig_count = sum(len(s.get("figures", [])) for s in sheets)
    cell_count = sum(len(s.get("cells", {})) for s in sheets)
    
    print(f"\nFile: [{modname}] {fname}")
    print(f"  Version: {ver} | Sheets: {len(sheets)} | Cells: {cell_count} | Figures: {fig_count}")
    print(f"  Pivots ({len(pivots)}): {list(pivots.keys())}")
    for pid, pinfo in pivots.items():
        print(f"    Pivot {pid}: name='{pinfo.get('name')}' model='{pinfo.get('model')}' measures={pinfo.get('measures')}")
        print(f"      domain={pinfo.get('domain')} rowGroupBys={pinfo.get('rowGroupBys')} colGroupBys={pinfo.get('colGroupBys')}")
    print(f"  Lists ({len(lists)}): {list(lists.keys())}")
    for lid, linfo in lists.items():
        print(f"    List {lid}: name='{linfo.get('name')}' model='{linfo.get('model')}' columns={linfo.get('columns')}")
        print(f"      domain={linfo.get('domain')} orderBy={linfo.get('orderBy')}")
    print(f"  Global Filters ({len(gfilters)}):")
    for gf in gfilters:
        print(f"    Filter '{gf.get('label')}' id={gf.get('id')} type={gf.get('type')} model={gf.get('modelName')}")

