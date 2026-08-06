# Clean up duplicate dashboard records
# Keep only the new ones (IDs 29-34), remove old duplicates (IDs 5-10)

old_ids = [5, 6, 7, 8, 9, 10]
for old_id in old_ids:
    d = env['spreadsheet.dashboard'].browse(old_id)
    if d.exists():
        print(f"Deleting duplicate: ID={old_id}, Name={d.name}, Group={d.dashboard_group_id.name}")
        d.unlink()

env.cr.commit()
print("Cleaned up duplicate dashboards!")

# Verify remaining
remaining = env['spreadsheet.dashboard'].search([('dashboard_group_id.name', '=', 'OBIDSS Operational BI')])
print(f"\nRemaining OBIDSS dashboards: {len(remaining)}")
for d in remaining:
    print(f"  ID: {d.id}, Name: {d.name}, Published: {d.is_published}")
