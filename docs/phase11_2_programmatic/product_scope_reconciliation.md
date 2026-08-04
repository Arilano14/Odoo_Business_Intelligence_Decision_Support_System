# Product Scope Reconciliation Report

## Exclusive Variant-Level Partition (Total = 283)

| Exclusive Classification | Variant Count |
|---|---:|
| Portfolio transacted | 250 |
| Portfolio non-transacted | 19 |
| Non-portfolio transacted | 4 |
| Standard/default non-transacted | 10 |
| Unknown transacted | 0 |
| Unknown non-transacted | 0 |
| **Total** | **283** |

## Reconciliation: 257 vs 254 Transacted

- **257** = all variants appearing in ANY SO/PO line for Company 2 (including draft, sent, cancel states)
- **254** = variants appearing in CONFIRMED SO/PO lines only (state = sale/done for SO, purchase/done for PO)
- **Difference = 3 variants** that appear ONLY in draft/sent PO lines (never confirmed):

| ID | Name | Code | Category | PO State |
|---|---|---|---|---|
| 17 | Large Cabinet | E-COM07 | All / Saleable / Office Furniture | sent |
| 29 | Desk Stand with Screen | FURN_7888 | All / Saleable / Office Furniture | draft |
| 30 | Individual Workplace | FURN_0789 | All / Saleable / Office Furniture | draft |

Note: IDs 29 and 30 (FURN_ prefix) are portfolio products that appear only in draft POs. They are classified as **portfolio_non_transacted** in the partition because only confirmed transactions count. ID 17 (E-COM07) is a standard Odoo product also in a draft/sent PO only.

## Non-Portfolio Transacted Impact

| Product | Code | Category | SO Value | PO Value |
|---|---|---|---:|---:|
| Corner Desk Right Sit | E-COM06 | Office Furniture | 0.00 | 2,500.00 |
| Large Desk | E-COM09 | Office Furniture | 0.00 | 10,000.00 |
| Virtual Home Staging | — | Services | 1,147.50 | 0.00 |
| Virtual Interior Design | — | Services | 3,000.00 | 0.00 |

**Total non-portfolio SO impact: Rp 4,147.50 / Rp 17,552,025,691.43 = 0.0000%**
**Total non-portfolio PO impact: Rp 12,500.00 / Rp 30,088,422,406.50 = 0.0000%**

**Conclusion: Non-portfolio transactions are not material.**

## Portfolio Classifier Rules

The portfolio classification is based on the following reproducible rules:

1. **Category-based**: Any product in `Portfolio 2026/*` categories (Consumables, Engine and Hydraulic Parts, Filters and Maintenance Parts, Heavy Equipment, Undercarriage Parts) → PORTFOLIO
2. **Category-based**: Products in `All / Saleable / Office Furniture`, `All / Saleable / Outdoor furniture`, `All / Saleable / Software`, `All / Home Construction` → PORTFOLIO (Odoo demo products that are saleable)
3. **Standard exclusion**: Products with `E-` or `CONS_` code prefix → STANDARD/DEFAULT
4. **Standard exclusion**: Products with names in {Deposit, Discount, Down payment, Expenses, Hotel Accommodation, Restaurant Expenses} → STANDARD/DEFAULT
5. **Standard exclusion**: Products in `All / Expenses` category → STANDARD/DEFAULT
6. **Service exclusion**: Products in `All / Saleable / Services` → NON-PORTFOLIO

## Product Categories Distribution

| Category | Count |
|---|---:|
| Portfolio 2026 / Consumables | 48 |
| Portfolio 2026 / Engine and Hydraulic Parts | 48 |
| Portfolio 2026 / Filters and Maintenance Parts | 48 |
| Portfolio 2026 / Heavy Equipment | 48 |
| Portfolio 2026 / Undercarriage Parts | 48 |
| All / Saleable / Office Furniture | 34 |
| All / Saleable / Services | 4 |
| All / Expenses | 2 |
| All / Home Construction | 1 |
| All / Saleable / Outdoor furniture | 1 |
| All / Saleable / Software | 1 |

## Scope Gate Verdict

```
PRODUCT SCOPE GATE: PASSED

Total active variants:           283 (matches)
Exclusive partition total:       283 (matches)
No duplicate classifications:    VERIFIED
No unknown transacted products:  VERIFIED (0)
Transacted reconciliation:       257 any-state → 254 confirmed (3 draft-only explained)
Non-portfolio impact:            0.0000% (not material)
Verified portfolio product IDs:  269 variants exported
```
