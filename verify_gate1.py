# Verify Gate 1 Sales Operations pilot evaluation
import json

d = env.ref('obidss_operational_bi.dashboard_sales')
print(f"Reading evaluated payload for {d.name} (ID: {d.id})...")

data = json.loads(d.spreadsheet_data)
sheets = data.get('sheets', [])
data_sheet = [s for s in sheets if s['id'] == 'sales_data'][0]

print("\nEvaluated Data Sheet Cells (H2:I13 - Monthly Trend):")
print(f"{'Cell H (Label)':<20} | {'Cell I (Value)':<25}")
print("-" * 50)

for i in range(2, 14):
    h_content = data_sheet['cells'].get(f"H{i}", {}).get('content', '')
    i_content = data_sheet['cells'].get(f"I{i}", {}).get('content', '')
    print(f"H{i}: {h_content:<16} | I{i}: {i_content:<22}")

print("\nEvaluated Data Sheet Cells (A2:B6 - Categories):")
for i in range(2, 7):
    a_content = data_sheet['cells'].get(f"A{i}", {}).get('content', '')
    b_content = data_sheet['cells'].get(f"B{i}", {}).get('content', '')
    print(f"A{i}: {a_content:<30} | B{i}: {b_content:<22}")

print("\nEvaluated Data Sheet Cells (E2:F6 - Salespeople):")
for i in range(2, 7):
    e_content = data_sheet['cells'].get(f"E{i}", {}).get('content', '')
    f_content = data_sheet['cells'].get(f"F{i}", {}).get('content', '')
    print(f"E{i}: {e_content:<20} | F{i}: {f_content:<22}")
