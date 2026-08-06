# Sales Pilot Browser & RPC Validation Report
## GATE 2E.7 — Runtime Endpoint Verification

### Summary
- **Target Dashboard:** `Sales Operations` (ID 6)
- **Dashboard Group:** `OBIDSS Operational BI`
- **Published State:** `True`
- **Attachment ID:** `1132` (`res_field='spreadsheet_binary_data'`)
- **RPC Endpoint:** `spreadsheet.dashboard/get_readonly_dashboard`
- **Validation Status:** **`PASS`**

---

### Verification Matrix

| Check | Requirement | Actual Value | Status |
|-------|-------------|--------------|--------|
| **HTTP Access** | Endpoint returns 200 OK | `200 OK` (Odoo Web Client) | **PASS** |
| **RPC Method** | `get_readonly_dashboard` returns snapshot | Valid JSON Snapshot (Version 21) | **PASS** |
| **Live Pivots** | Non-empty pivot definitions | 3 Pivots (`sale.report` Company 2) | **PASS** |
| **Live Lists** | Non-empty list definitions | 1 List (`sale.order` Company 2) | **PASS** |
| **Global Filters** | Date & relation filters present | 3 Filters (Period, Category, Customer) | **PASS** |
| **Scorecards** | Visual scorecard figures | 4 Scorecards (Revenue, SOs, AOV, Cancelled) | **PASS** |
| **Charts** | Monthly trend line chart | 1 Odoo Line Chart (`sale.report`) | **PASS** |
| **Demo Data Audit** | No sample or demo company strings | 100% Clean (PT Prima Alat Nusantara) | **PASS** |
| **Console Errors** | No unbounded ranges or JSON parse errors | Clean (Version 21 compliant) | **PASS** |
