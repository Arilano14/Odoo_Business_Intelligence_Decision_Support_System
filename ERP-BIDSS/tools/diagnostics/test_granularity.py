# Test granularity vs fieldName in Odoo Spreadsheet pivot
import json
import base64

dashboard = env.ref('obidss_operational_bi.dashboard_sales')
print(f"Testing pivot granularity on {dashboard.name}...")

# Test defining pivot 5 with granularity: "month"
p5_def = {
    "type": "ODOO", "id": "5", "formulaId": "5",
    "name": "Monthly Sales Trend",
    "model": "sale.order",
    "domain": [["company_id", "=", 2], ["state", "=", "sale"], ["date_order", ">=", "2026-01-01"], ["date_order", "<", "2027-01-01"]],
    "measures": [{"id": "amount_untaxed", "fieldName": "amount_untaxed"}],
    "rows": [{"fieldName": "date_order", "granularity": "month"}],
    "columns": [],
    "fieldMatching": {}
}

# Test how Odoo evaluates PIVOT.HEADER and PIVOT.VALUE with granularity
# Write to dashboard and check evaluated cells
payload = json.loads(dashboard.spreadsheet_data)
payload['pivots']['5'] = p5_def

# Update Data sheet
data_sheet = [s for s in payload['sheets'] if s['id'] == 'sales_data'][0]
for i in range(1, 13):
    r = i + 1
    # Try different formula combinations
    data_sheet['cells'][f"H{r}"] = {"content": f"=PIVOT.HEADER(5,\"#date_order\",{i})"}
    data_sheet['cells'][f"I{r}"] = {"content": f"=PIVOT.VALUE(5,\"amount_untaxed\",\"#date_order\",{i})"}

dashboard.write({'spreadsheet_binary_data': base64.b64encode(json.dumps(payload).encode('utf-8'))})
env.cr.commit()

print("Wrote granularity pivot definition test!")
