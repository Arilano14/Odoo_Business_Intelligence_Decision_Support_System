# Phase 9 — Transaction Data Contract
## Locked Targets for PT Prima Alat Nusantara (FY 2026)

**Version:** 1.0
**Locked Date:** 2026-07-26
**Random Seed:** 26072026
**Batch Identifier:** PORTFOLIO_2026_V1

---

## 1. Monthly Order Distribution (LOCKED)

| Month | Sales Orders | Purchase Orders | Phase |
|---|---:|---:|---|
| January | 60 | 18 | Baseline |
| February | 58 | 18 | Baseline |
| March | 48 | 15 | Disruption |
| April | 55 | 32 | Procurement Response |
| May | 60 | 28 | Accumulation |
| June | 62 | 20 | Correction |
| July | 63 | 18 | Correction |
| August | 64 | 17 | Correction |
| September | 61 | 18 | Correction |
| October | 62 | 18 | Stabilization |
| November | 63 | 18 | Stabilization |
| December | 64 | 20 | Stabilization |
| **Total** | **720** | **240** | |

---

## 2. Customer Segment Allocation (LOCKED)

| Segment | Customer Count | Orders/Customer | Segment Total |
|---|---:|---|---:|
| Strategic | 8 | 36–54 | 288–432 |
| Regular | 16 | 12–24 | 192–384 |
| Occasional | 14 | 3–8 | 42–112 |
| One-time | 10 | exactly 1 | 10 |
| **Total** | **48** | | **720** |

---

## 3. Supplier Segment Allocation (LOCKED)

| Segment | Supplier Count | POs/Supplier | Segment Total |
|---|---:|---|---:|
| Strategic | 5 | 24–36 | 120–180 |
| Regular | 10 | 6–14 | 60–140 |
| Backup | 6 | 2–6 | 12–36 |
| Occasional | 3 | 1–3 | 3–9 |
| **Total** | **24** | | **240** |

---

## 4. Product Category Quantity Bounds (LOCKED)

### Sales Order Lines

| Category | Min Qty | Max Qty |
|---|---:|---:|
| Heavy Equipment | 1 | 2 |
| Engine/Hydraulic Parts | 1 | 5 |
| Undercarriage Parts | 1 | 8 |
| Filters/Maintenance | 2 | 30 |
| Consumables | 5 | 80 |

### Purchase Order Lines

| Category | Min Qty | Max Qty |
|---|---:|---:|
| Heavy Equipment | 1 | 2 |
| Engine/Hydraulic Parts | 2 | 12 |
| Undercarriage Parts | 4 | 20 |
| Filters/Maintenance | 20 | 120 |
| Consumables | 50 | 300 |

---

## 5. Transaction State Targets (LOCKED)

### Sales Orders (720 total)

| State | Count | % |
|---|---:|---:|
| Confirmed/Sale | 662 | 92% |
| Draft/Sent | 29 | 4% |
| Cancelled | 29 | 4% |

### Deliveries (662 confirmed)

| State | Count | % |
|---|---:|---:|
| Done | 596 | 90% |
| Ready/Waiting | 40 | 6% |
| Late | 16 | 2.4% |
| Backorder/Partial | 10 | 1.5% |

### Purchase Orders (240 total)

| State | Count | % |
|---|---:|---:|
| Confirmed/Purchase | 221 | 92% |
| Draft/Sent | 10 | 4% |
| Cancelled | 9 | 4% |

### Receipts (221 confirmed)

| State | Count | % |
|---|---:|---:|
| Done | 199 | 90% |
| Ready/Waiting | 13 | 6% |
| Late | 9 | 4% |

---

## 6. End-of-Year Operational Counts

| Metric | Min | Max |
|---|---:|---:|
| Pending Delivery Orders | 8 | 15 |
| Late Delivery Orders | 3 | 8 |
| Pending Receipts | 5 | 10 |
| Late Receipts | 2 | 6 |

---

## 7. Deterministic Reference Patterns (LOCKED)

| Model | Field | Pattern |
|---|---|---|
| `sale.order` | `client_order_ref` | `PORTFOLIO_2026_V1-SO-NNNN` |
| `purchase.order` | `partner_ref` | `PORTFOLIO_2026_V1-PO-NNNN` |
| `account.move` (invoice) | `ref` | `PORTFOLIO_2026_V1-INV-NNNN` |
| `account.move` (bill) | `ref` | `PORTFOLIO_2026_V1-BILL-NNNN` |
| `stock.picking` (internal) | `origin` | `PORTFOLIO_2026_V1-INT-NN` |
| `stock.scrap` | `origin` | `PORTFOLIO_2026_V1-SCRAP-NN` |
