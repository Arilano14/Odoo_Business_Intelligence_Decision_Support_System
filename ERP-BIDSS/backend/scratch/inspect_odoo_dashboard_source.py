import json, os

# Check how Odoo loads dashboards - the sample_dashboard_file_path mechanism
# Let's look at the Odoo source code for spreadsheet_dashboard

source_base = r'C:\Program Files\Odoo 18.0.20241229\server\odoo\addons'

# Find all Python files in spreadsheet_dashboard module
import glob
dashboard_module = os.path.join(source_base, 'spreadsheet_dashboard')
dashboard_models = os.path.join(dashboard_module, 'models')

# Read the main model
model_files = glob.glob(os.path.join(dashboard_models, '*.py'))
for f in model_files:
    fname = os.path.basename(f)
    print(f'=== {fname} ===')
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    # Find relevant methods
    if 'sample_dashboard_file_path' in content or 'spreadsheet_data' in content or 'get_data' in content:
        print(content[:5000])
    else:
        print(f'  (no relevant methods, {len(content)} chars)')
    print()

# Also check the controller
controllers = glob.glob(os.path.join(dashboard_module, 'controllers', '*.py'))
for f in controllers:
    fname = os.path.basename(f)
    print(f'=== CONTROLLER: {fname} ===')
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    print(content[:5000])
