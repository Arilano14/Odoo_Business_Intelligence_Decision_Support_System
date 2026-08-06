# Sales Operations Pilot Payload Anatomy & Audit
## GATE 2E.5 — Payload Inspection and Classification

### Summary
- **Dashboard ID:** 6 (`Sales Operations`)
- **Attachment ID:** `1132`
- **`res_field`:** `spreadsheet_binary_data`
- **Published State:** `True`
- **Payload File Size:** `13175` bytes
- **Classification:** **`LIVE`**

---

### Audit Criteria & Evidence Matrix

| Criterion | Requirement | Verified Value | Result |
|-----------|-------------|----------------|--------|
| Attachment `res_field` | Must be `spreadsheet_binary_data` | `spreadsheet_binary_data` | **PASS** |
| Attachment `name` | Must be `spreadsheet_binary_data` | `spreadsheet_binary_data` | **PASS** |
| Published State | Must be `True` | `True` | **PASS** |
| Live Data Sources | At least 1 live Odoo pivot / list | `3` Pivots (`sale.report`), `1` List (`sale.order`) | **PASS** |
| Pivot Formulas | `=PIVOT.VALUE(...)` in cells | Yes (`Data!B2`, `Data!B3`, `Data!B5`, `A18-C22`) | **PASS** |
| Scorecard Charts | Scorecard figures referencing formulas | 4 Scorecards (Confirmed Rev, SO Count, AOV, Cancelled SO) | **PASS** |
| Dynamic Charts | Odoo line/bar chart referencing model | 1 Odoo Line Chart (`sale.report`, monthly trend) | **PASS** |
| Global Filters | Mapped filter objects | 3 Filters (Period, Product Category, Customer) | **PASS** |
| Drill-Down Navigation | `odoo://view/` links for user click-through | 3 Navigation Links (SO List, Sales Pivot, Product Catalog) | **PASS** |

---

### Detailed Anatomy

```json
{
  "version": 21,
  "pivots": {
    "1": "Confirmed Sales Summary (model: sale.report, domain: company_id=2, state in [sale, done])",
    "2": "Cancelled Sales Summary (model: sale.report, domain: company_id=2, state=cancel)",
    "3": "Top Product Categories Sales (model: sale.report, rowGroupBys: categ_id)"
  },
  "lists": {
    "1": "Recent Confirmed Sales Orders (model: sale.order, domain: company_id=2)"
  },
  "globalFilters": [
    "Date Period (relative this_year)",
    "Product Category (model: product.category)",
    "Customer (model: res.partner)"
  ],
  "figures": [
    "Scorecard: Confirmed Sales Value (Data!B2)",
    "Scorecard: Confirmed Orders (SOs) (Data!B3)",
    "Scorecard: Average Order Value (AOV) (Data!B4)",
    "Scorecard: Cancelled Orders (Data!B5)",
    "Odoo Line Chart: Monthly Sales Revenue Trend (FY 2026)"
  ]
}
```
