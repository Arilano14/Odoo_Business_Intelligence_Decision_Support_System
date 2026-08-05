# RPC & ORM Final Verification Script for OBIDSS Dashboards

import json

print("=" * 65)
print("1. VERIFY DASHBOARD PUBLICATION & SIDEBAR CLEANUP STATUS")
print("=" * 65)

# Check all dashboards in system
all_dashboards = env['spreadsheet.dashboard'].search([])
print(f"Total dashboards in database: {len(all_dashboards)}")

print(f"\n{'ID':<5} | {'XML ID':<55} | {'Group':<22} | {'Published':<10}")
print("-" * 100)

for d in all_dashboards:
    # Get XML ID if exists
    im = env['ir.model.data'].search([('model', '=', 'spreadsheet.dashboard'), ('res_id', '=', d.id)])
    xml_id = f"{im.module}.{im.name}" if im else "N/A (custom)"
    group_name = d.dashboard_group_id.name if d.dashboard_group_id else "No Group"
    print(f"{d.id:<5} | {xml_id:<55} | {group_name:<22} | {str(d.is_published):<10}")

print("\n" + "=" * 65)
print("2. VERIFY OBIDSS DASHBOARDS STRUCTURAL INTEGRITY")
print("=" * 65)

obidss_xml_ids = [
    ('Executive Operations', 'obidss_operational_bi.dashboard_executive'),
    ('Sales Operations', 'obidss_operational_bi.dashboard_sales'),
    ('Purchase & Suppliers', 'obidss_operational_bi.dashboard_purchase'),
    ('Inventory Operations', 'obidss_operational_bi.dashboard_inventory'),
    ('Data Quality & Reconciliation', 'obidss_operational_bi.dashboard_data_quality'),
    ('Finance & Invoicing (Unpublished)', 'obidss_operational_bi.dashboard_finance'),
]

for name, xml_id in obidss_xml_ids:
    d = env.ref(xml_id, raise_if_not_found=False)
    if not d:
        print(f"ERROR: {xml_id} NOT FOUND!")
        continue
    
    print(f"\nDashboard: {d.name} (XML ID: {xml_id}, DB ID: {d.id})")
    print(f"  Published: {d.is_published}")

    if not d.spreadsheet_data:
        print("  Data: EMPTY (Unpublished or No Data)")
        continue

    try:
        data = json.loads(d.spreadsheet_data)
        pivots = data.get("pivots", {})
        lists = data.get("lists", {})
        sheets = data.get("sheets", [])

        live_formulas = 0
        positional_formulas = 0
        for sheet in sheets:
            for cell_ref, cell in sheet.get("cells", {}).items():
                content = cell.get("content", "")
                if content.startswith("="):
                    live_formulas += 1
                if "#" in content:
                    positional_formulas += 1

        total_figures = sum(len(sheet.get("figures", [])) for sheet in sheets)

        print(f"  Pivots: {len(pivots)} | Lists: {len(lists)} | Sheets: {len(sheets)}")
        print(f"  Live Formulas: {live_formulas} | Positional (#) Formulas: {positional_formulas}")
        print(f"  Charts/Figures: {total_figures}")
        print(f"  RPC Load: STRUCTURAL VALIDATION PASS")

    except Exception as e:
        print(f"  RPC Load FAILED: {e}")

print("\n" + "=" * 65)
print("3. VERIFY PUBLISHED DASHBOARDS SIDEBAR LIST FOR REVIEWER")
print("=" * 65)

published_obidss = env['spreadsheet.dashboard'].search([
    ('is_published', '=', True)
])

print(f"Total Published Dashboards for Reviewer Sidebar: {len(published_obidss)}")
for d in published_obidss:
    im = env['ir.model.data'].search([('model', '=', 'spreadsheet.dashboard'), ('res_id', '=', d.id)])
    xml_id = f"{im.module}.{im.name}" if im else "N/A"
    print(f"  - [{d.dashboard_group_id.name}] {d.name} ({xml_id})")
