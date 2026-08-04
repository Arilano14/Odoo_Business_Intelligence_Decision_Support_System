# Generated Artifact Provenance Report
## GATE 2E.8 — Dashboard Artifact Provenance

### Exported & Versioned Artifacts inside Custom Addon
All JSON dashboard payloads were generated using Odoo 18 Spreadsheet Version 21 specification with live Odoo data sources (`sale.report`, `purchase.report`, `stock.quant`, `obidss.data.quality`).

- **Base Addon Path:** `custom_addons/obidss_operational_bi/data/files/`

| Artifact Filename | Target Dashboard ID | Live Model Sources | File Size | Version | Provenance Status |
|-------------------|---------------------|--------------------|-----------|---------|-------------------|
| `executive_operations_dashboard.json` | ID 5 | `sale.report`, `purchase.report`, `stock.quant` | 6,190 bytes | 21 | **VERIFIED ODOO PAYLOAD** |
| `sales_operations_dashboard.json` | ID 6 | `sale.report`, `sale.order` | 13,175 bytes | 21 | **VERIFIED ODOO PAYLOAD** |
| `purchase_suppliers_dashboard.json` | ID 7 | `purchase.report`, `purchase.order` | 5,528 bytes | 21 | **VERIFIED ODOO PAYLOAD** |
| `inventory_operations_dashboard.json` | ID 8 | `stock.quant`, `stock.picking` | 4,526 bytes | 21 | **VERIFIED ODOO PAYLOAD** |
| `data_quality_dashboard.json` | ID 10 | `obidss.data.quality` | 1,689 bytes | 21 | **VERIFIED ODOO PAYLOAD** |

### XML Manifest Integration
In `custom_addons/obidss_operational_bi/data/dashboard_groups.xml`, records are defined using native base64 XML file loading:

```xml
<record id="dashboard_sales" model="spreadsheet.dashboard">
    <field name="name">Sales Operations</field>
    <field name="dashboard_group_id" ref="dashboard_group_obidss"/>
    <field name="sequence">20</field>
    <field name="is_published" eval="True"/>
    <field name="group_ids" eval="[(4, ref('group_obidss_user'))]"/>
    <field name="spreadsheet_binary_data" type="base64" file="obidss_operational_bi/data/files/sales_operations_dashboard.json"/>
</record>
```
