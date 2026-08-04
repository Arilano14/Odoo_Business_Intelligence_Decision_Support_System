# Sales Operations UI Build Log
## GATE 2E.4 & 2E.5 — Pilot Build Provenance

1. **Source Model:** `sale.report` (Sales Analysis) & `sale.order` (Sales Orders)
2. **Filters Applied:** `company_id = 2`, `date_order >= 2026-01-01`, `state in ('sale', 'done')`
3. **Data Source Integration:** 3 Odoo Pivots, 1 Odoo List, 3 Global Filters
4. **Formulas Embedded:** `=PIVOT.VALUE(1, "price_subtotal")`, `=PIVOT.VALUE(1, "order_reference")`, `=IFERROR(B2/B3, 0)`, `=PIVOT.VALUE(2, "order_reference")`
5. **Scorecards & Visuals:** 4 Scorecard Figures, 1 Odoo Line Chart
6. **Provenance Hash:** Verified JSON Version 21 deployment to Attachment ID `1132` on Dashboard ID 6.
