# Verify XML IDs of standard dashboards
std_xml_ids = [
    'spreadsheet_dashboard_sale.spreadsheet_dashboard_sales',
    'spreadsheet_dashboard_sale.spreadsheet_dashboard_product',
    'spreadsheet_dashboard_account.spreadsheet_dashboard_invoicing',
    'spreadsheet_dashboard_stock_account.spreadsheet_dashboard_warehouse_metrics'
]

for xml_id in std_xml_ids:
    rec = env.ref(xml_id, raise_if_not_found=False)
    if rec:
        print(f"FOUND: {xml_id} -> ID={rec.id}, Name='{rec.name}', Group='{rec.dashboard_group_id.name}', Published={rec.is_published}")
    else:
        print(f"NOT FOUND: {xml_id}")
