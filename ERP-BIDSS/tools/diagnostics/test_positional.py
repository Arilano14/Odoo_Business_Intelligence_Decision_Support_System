# Test script to test positional formulas #date:month and #categ_id

import json
import base64

# Let's inspect what Odoo's spreadsheet engine returns for positional header #date:month
# by updating Dashboard 29 (Executive Operations) with #date:month in Data sheet
d = env.ref('obidss_operational_bi.dashboard_executive')

payload = json.loads(d.spreadsheet_data)
print(f"Loaded payload for {d.name}")

# Check pivot 5 (Monthly Sales Trend)
p5 = payload['pivots']['5']
print(f"Pivot 5: {p5}")

# Update Data sheet cells to use #date:month and #date_order:month
sheets = payload['sheets']
data_sheet = [s for s in sheets if s['id'] == 'exec_data'][0]

print("Original cell A2:", data_sheet['cells'].get('A2'))
print("Updating to positional #date:month ...")

for i in range(1, 13):
    r = i + 1
    data_sheet['cells'][f"A{r}"] = {"content": f"=PIVOT.HEADER(5,\"#date:month\",{i})"}
    data_sheet['cells'][f"B{r}"] = {"content": f"=PIVOT.VALUE(5,\"price_subtotal\",\"#date:month\",{i})"}
    data_sheet['cells'][f"C{r}"] = {"content": f"=PIVOT.VALUE(6,\"untaxed_total\",\"#date_order:month\",{i})"}

# Write back to DB and test
b64_bytes = base64.b64encode(json.dumps(payload).encode('utf-8'))
d.write({'spreadsheet_binary_data': b64_bytes})
env.cr.commit()

print("Successfully updated Executive Operations with #date:month positional formulas!")
