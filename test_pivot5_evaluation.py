# Test exact spreadsheet evaluation for Pivot 5 date_order:month formulas
import json
import base64

dashboard = env.ref("obidss_operational_bi.dashboard_sales")
data = json.loads(dashboard.spreadsheet_data)

# Print pivot 5 structure
print("Pivot 5 definition:")
print(json.dumps(data['pivots']['5'], indent=2))

# Test formulas on Data sheet
data_sheet = [s for s in data['sheets'] if s['id'] == 'sales_data'][0]

print("\nCurrent Data sheet H and I formulas:")
for i in range(2, 14):
    h = data_sheet['cells'].get(f"H{i}", {}).get('content')
    val = data_sheet['cells'].get(f"I{i}", {}).get('content')
    print(f"  H{i}: {h} | I{i}: {val}")

# Let's test setting explicit month headers in H (e.g. "01/2026", "02/2026")
# and using PIVOT.VALUE(5, "amount_untaxed", "date_order:month", "01/2026")
print("\nUpdating H cells to literal month strings '01/2026'...'12/2026'")
print("and I cells to =PIVOT.VALUE(5, \"amount_untaxed\", \"date_order:month\", H<row>)")

months = [f"{m:02d}/2026" for m in range(1, 13)]
for i, m_str in enumerate(months, 2):
    data_sheet['cells'][f"H{i}"] = {"content": m_str}
    data_sheet['cells'][f"I{i}"] = {"content": f'=PIVOT.VALUE(5,"amount_untaxed","date_order:month","{m_str}")'}

dashboard.write({'spreadsheet_binary_data': base64.b64encode(json.dumps(data).encode('utf-8'))})
env.cr.commit()

print("Updated Sales Operations dashboard with literal month keys and PIVOT.VALUE test!")
