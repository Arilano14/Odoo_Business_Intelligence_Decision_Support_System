# GATE 2E.1 — Final Data Truth
## PT Prima Alat Nusantara (Company ID 2, FY 2026)

All queries filtered by `company_id = 2 AND date >= '2026-01-01' AND date < '2027-01-01'`.

## Summary Table

| Entity | All-company total | Company 2 FY2026 | Portfolio valid | Excluded |
|--------|:-:|:-:|:-:|:-:|
| Sale Orders | 740 | 740 | 740 | 0 |
| Purchase Orders | 253 | 251 | 251 | 2 (Company 1) |
| Product Variants (active) | 283 | N/A | 257 (transacted) | 26 (not in any SO/PO) |
| Product Templates (active) | 277 | N/A | N/A | N/A |
| Customer Invoices | — | 0 | 0 | — |
| Vendor Bills | — | 0 | 0 | — |
| Stock Quants | — | 491 | 491 | — |
| Done Pickings | — | 20 | 20 | — |

## Sales Orders by State

| State | Count | Amount (IDR) |
|-------|------:|-------------:|
| sale (confirmed) | 677 | 17,552,025,691.43 |
| draft | 33 | 755,771,465.12 |
| cancel | 29 | 604,307,965.87 |
| sent | 1 | 1,740.00 |

## Purchase Orders by State (Company 2 FY2026)

| State | Count | Amount (IDR) |
|-------|------:|-------------:|
| purchase (confirmed) | 225 | 30,088,422,406.50 |
| draft | 16 | 1,111,549,592.00 |
| cancel | 9 | 1,348,766,000.00 |
| sent | 1 | 14,563.00 |

## PO Discrepancy (251 vs 253)

**Explanation:** 253 total POs exist in the database. 2 belong to Company 1:

| PO ID | Name | Company | State | Date | Amount |
|-------|------|---------|-------|------|--------|
| 529 | P00529 | 1 (My Company SF) | draft | 2026-07-28 | 24,138.50 |
| 530 | P00530 | 1 (My Company SF) | draft | 2026-07-23 | 316.25 |

**Classification: OTHER_COMPANY** — These are not PT Prima Alat Nusantara data.

Remaining 251 POs are all Company 2, all within FY2026. No unknown records.

## Finance Decision

```
Customer Invoices (Company 2 FY2026) = 0
Vendor Bills (Company 2 FY2026) = 0

FINANCE & INVOICING DASHBOARD: NOT AVAILABLE — NO VALID INVOICE OR BILL DATA
```

## Products

- 257 product variants are actively transacted in Company 2 FY2026 (SO or PO lines)
- 250 products appear in Sales Order lines
- 241 products appear in Purchase Order lines
- 26 active variants have no transactions (may be test/setup products)
