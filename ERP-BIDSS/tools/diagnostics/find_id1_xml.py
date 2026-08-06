# Find XML ID for spreadsheet.dashboard ID=1
im = env['ir.model.data'].search([('model', '=', 'spreadsheet.dashboard'), ('res_id', '=', 1)])
if im:
    print(f"ID 1 XML ID: {im.module}.{im.name}")
else:
    print("ID 1 has no ir.model.data entry")

d1 = env['spreadsheet.dashboard'].browse(1)
if d1.exists():
    print(f"ID 1 Name: '{d1.name}', Group: '{d1.dashboard_group_id.name}'")
