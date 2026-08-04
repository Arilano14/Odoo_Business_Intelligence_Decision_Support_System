# RPC-level verification: check all dashboards can be loaded without errors
import json
import base64

dashboards = env['spreadsheet.dashboard'].search([])
print(f"Total dashboards: {len(dashboards)}")
print()

for d in dashboards:
    print(f"ID: {d.id}, Name: {d.name}")
    print(f"  Group: {d.dashboard_group_id.name}")
    print(f"  Published: {d.is_published}")
    
    # Try to read spreadsheet_data (this is what the RPC call does)
    try:
        data_str = d.spreadsheet_data
        if data_str:
            data = json.loads(data_str)
            pivots = data.get("pivots", {})
            lists = data.get("lists", {})
            sheets = data.get("sheets", [])
            
            # Count live formulas
            live_formulas = 0
            for sheet in sheets:
                for cell_ref, cell in sheet.get("cells", {}).items():
                    content = cell.get("content", "")
                    if content.startswith("="):
                        live_formulas += 1
            
            # Count figures (charts)
            total_figures = sum(len(sheet.get("figures", [])) for sheet in sheets)
            
            print(f"  Version: {data.get('version')}")
            print(f"  Pivots: {len(pivots)}")
            print(f"  Lists: {len(lists)}")
            print(f"  Sheets: {len(sheets)}")
            print(f"  Live Formulas: {live_formulas}")
            print(f"  Charts/Figures: {total_figures}")
            print(f"  RPC Load: PASS")
        else:
            print(f"  Data: EMPTY")
            print(f"  RPC Load: FAIL (no data)")
    except json.JSONDecodeError as e:
        print(f"  RPC Load: FAIL (JSONDecodeError: {e})")
    except Exception as e:
        print(f"  RPC Load: FAIL ({e})")
    print()
