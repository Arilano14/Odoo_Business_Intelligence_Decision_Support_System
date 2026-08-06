import json
import base64

dashboards = env['spreadsheet.dashboard'].search([])
invalid = []
for d in dashboards:
    data_str = d.spreadsheet_binary_data
    if not data_str:
        invalid.append((d.id, d.name, "Empty binary data"))
        continue
        
    try:
        if isinstance(data_str, bytes):
            data_str = data_str.decode('utf-8')
            
        try:
            decoded = base64.b64decode(data_str).decode('utf-8')
            if '{' in decoded:
                data_str = decoded
        except:
            pass
            
        json.loads(data_str)
    except Exception as e:
        invalid.append((d.id, d.name, f"JSON Error: {e}"))

print(f"Found {len(invalid)} invalid dashboards:")
for d_id, name, err in invalid:
    print(f" - ID: {d_id}, Name: {name}, Error: {err}")
    
print("Fixing them by applying an empty valid JSON...")
empty_data = json.dumps({
    "version": 21,
    "sheets": [{"id": "sheet1", "name": "Sheet1", "cells": {}}]
})
empty_b64 = base64.b64encode(empty_data.encode('utf-8'))

for d_id, name, err in invalid:
    d = env['spreadsheet.dashboard'].browse(d_id)
    d.write({'spreadsheet_binary_data': empty_b64})
    
env.cr.commit()
print("Fixed invalid dashboards!")
