import json
import base64

dashboards = env['spreadsheet.dashboard'].search([])
for dashboard in dashboards:
    data_str = dashboard.spreadsheet_binary_data
    if data_str:
        try:
            if isinstance(data_str, bytes):
                data_str = data_str.decode('utf-8')
            
            # It might be base64 encoded if it came from ir.attachment binary field
            try:
                decoded = base64.b64decode(data_str).decode('utf-8')
                if '{' in decoded:
                    data_str = decoded
            except:
                pass

            data = json.loads(data_str)
            if 'pivots' in data and len(data['pivots']) > 0:
                with open(f"dashboard_{dashboard.id}.json", "w") as f:
                    json.dump(data, f, indent=2)
                print(f"Dumped dashboard {dashboard.id} with pivots!")
            else:
                with open(f"dashboard_{dashboard.id}_no_pivot.json", "w") as f:
                    json.dump(data, f, indent=2)
                print(f"Dumped dashboard {dashboard.id} (no pivots)")
        except Exception as e:
            print(f"Failed to parse dashboard {dashboard.id}: {e}")
