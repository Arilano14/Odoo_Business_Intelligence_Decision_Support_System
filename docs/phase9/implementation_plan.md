# PHASE 9 — Implementation Plan
## Operational Transaction Generation for Odoo 18
### PT Prima Alat Nusantara — Heavy Equipment Distribution

**Document:** `docs/phase9/implementation_plan.md`
**Created:** 2026-07-26
**Status:** DRAFT — Awaiting User Approval
**Operating Mode:** Plan-Only (No mutations performed)

---

## 1. Executive Summary

Phase 9 generates **one full year (Jan–Dec 2026) of realistic, interconnected operational transactions** for the Heavy Equipment Distribution case study of PT Prima Alat Nusantara. The generated dataset will cover Sales Orders, Purchase Orders, Inventory operations, Customer Invoices, Vendor Bills, and Payments — all traceable to `PORTFOLIO_2026_V1`.

The plan uses a **demand-driven simulation** where customer demand triggers procurement, not independent random generation. Execution is divided into **6 approval gates** (9A–9F) to ensure safety and incremental validation.

**Key targets:**
- 720 Sales Orders, 240 Purchase Orders
- 24 Internal Transfers, 12 Scrap Operations
- Opening inventory for 240 products
- Full Odoo workflow (SO → Delivery → Invoice → Payment; PO → Receipt → Bill → Payment)
- Scenario-driven monthly story (baseline → disruption → recovery → stabilization)

---

## 2. Actual Current State

### 2.1 Current State Audit

> [!IMPORTANT]
> Audit performed on 2026-07-26 via read-only ORM queries against `Business_Intelegent_Project_v2`.

| Object | Expected | Actual | Status | Evidence | Model |
|---|---:|---:|---|---|---|
| Company (PT Prima Alat Nusantara) | 1 | 1 | ✅ PASS | `res.company` ID 2, currency IDR | `res.company` |
| Main Warehouse (PAN) | 1 | 1 | ✅ PASS | `stock.warehouse` ID 2, code PAN | `stock.warehouse` |
| Portfolio Customers | 48 | 48 | ✅ PASS | ref `PORTFOLIO_2026_V1-CUST-*` | `res.partner` |
| Portfolio Suppliers | 24 | 24 | ✅ PASS | ref `PORTFOLIO_2026_V1-VEND-*` | `res.partner` |
| Product Templates | 240 | 240 | ✅ PASS | default_code `PORTFOLIO_2026_V1-PROD-*` | `product.template` |
| Product Variants | 240 | 240 | ✅ PASS | default_code `PORTFOLIO_2026_V1-PROD-*` | `product.product` |
| Parent Category (Portfolio 2026) | 1 | 1 | ✅ PASS | `product.category` | `product.category` |
| Child Categories | 5 | 5 | ✅ PASS | Heavy Equipment, Engine and Hydraulic Parts, Undercarriage Parts, Filters and Maintenance Parts, Consumables | `product.category` |
| Supplier Mappings | 456 | 456 | ✅ PASS | `product.supplierinfo` | `product.supplierinfo` |
| Portfolio SO 2024/2026 | 0 | 0 | ✅ PASS | No residual transactions | `sale.order` |
| Portfolio PO 2024/2026 | 0 | 0 | ✅ PASS | No residual transactions | `purchase.order` |
| Portfolio Account Moves | 0 | 0 | ✅ PASS | No residual transactions | `account.move` |
| Portfolio Stock Pickings | 0 | 0 | ✅ PASS | No residual transactions | `stock.picking` |
| Duplicate customer refs | 0 | 0 | ✅ PASS | All refs unique | `res.partner` |
| Duplicate supplier refs | 0 | 0 | ✅ PASS | All refs unique | `res.partner` |
| Duplicate product codes | 0 | 0 | ✅ PASS | All default_codes unique | `product.template` |

### 2.2 Additional Observations

| Finding | Detail | Blocker? |
|---|---|---|
| Old BIDSS products exist | 550 `product.product` with code `BIDSS-*` | ⚠️ Non-blocker — Phase 9 uses only `PORTFOLIO_2026_V1-PROD-*` filter |
| Old BIDSS customers exist | 300 `res.partner` with ref `BIDSS-CUST-*` | ⚠️ Non-blocker — Phase 9 uses only `PORTFOLIO_2026_V1-CUST-*` filter |
| Old BIDSS vendors exist | 300 `res.partner` with ref `BIDSS-VEND-*` | ⚠️ Non-blocker — Phase 9 uses only `PORTFOLIO_2026_V1-VEND-*` filter |
| Multiple warehouses exist | 7 internal stock locations across 7 warehouse codes | ⚠️ Non-blocker — Phase 9 uses only PAN warehouse |
| Product prices are low | Prices range Rp 10K–1M; Heavy Equipment items also in this range | ⚠️ **ADVISORY** — see Section 29 |
| Git branch | `main` | ✅ OK |

### 2.3 Product Price Observation

> [!WARNING]
> The Phase 8 product setup used `random.randint(10, 1000) * 1000` for **all** categories, producing costs of Rp 10K–1M uniformly. This means "Heavy Equipment" items have costs of ~Rp 500K instead of realistic ~Rp 1.5B. This is a Phase 8 design decision, not a Phase 9 problem. Phase 9 will work with the existing prices. However, this directly affects whether the annual revenue target (Rp 180B–320B) is achievable with 720 SOs at 2.8–3.6 lines/SO and these price points.
>
> **Estimated max annual revenue with current prices:** 720 SO × 3.6 lines × Rp 1M × avg qty 20 ≈ Rp 51.8B — **well below the Rp 180B minimum.**
>
> **Recommendation:** Either (a) adjust the revenue guardrail to match current product prices (Rp 30B–80B range), or (b) revise Phase 8 product prices before Phase 9 execution. This is flagged as **Open Question #1** in Section 29.

---

## 3. Phase 8 Preconditions

All 17 Phase 8 preconditions **PASS**. No blockers detected.

---

## 4. Confirmed Blockers

| ID | Description | Status |
|---|---|---|
| BLOCK-01 | Revenue guardrail (Rp 180B–320B) may be unreachable with current product prices | **OPEN QUESTION** — see Section 29 |

> The blocker is conditional: if the user adjusts the revenue guardrail or product prices, it is resolved. Phase 9 implementation can proceed with adjusted guardrails.

---

## 5. Scope

Phase 9 generates:

1. Opening inventory adjustment for 240 products (2026-01-01)
2. 720 Sales Orders (Jan–Dec 2026)
3. 240 Purchase Orders (Jan–Dec 2026)
4. 24 Internal Transfers
5. 12 Scrap Operations
6. Customer Invoices, Vendor Bills, and Payments for eligible completed transactions
7. Delivery Orders and Receipts derived from confirmed SO/PO workflows

All records tagged with `PORTFOLIO_2026_V1` batch identifier.

---

## 6. Explicit Out-of-Scope

- CRM leads or opportunities
- Manufacturing Orders
- Multi-company or multi-currency transactions
- E-commerce, dropshipping, subcontracting
- Serial/lot tracking
- Complex return or refund workflows
- Partial payment workflows
- External API integrations
- ETL pipeline execution
- Analytics Mart population
- Power BI file changes
- DSS calculation
- Forecasting calculation
- AI or Machine Learning
- Phase 8 master data modification

---

## 7. Existing Codebase Assessment

### 7.1 Files to Keep (KEEP)

| File | Reason |
|---|---|
| `backend/odoo/connection.py` | Reusable XML-RPC connection helper |
| `backend/run_phase8.py` | Phase 8 orchestrator — not modified by Phase 9 |
| `backend/odoo/setup_company.py` | Phase 8 only |
| `backend/odoo/setup_partners.py` | Phase 8 only |
| `backend/odoo/setup_products.py` | Phase 8 only |
| `backend/validation/validate_phase8.py` | Phase 8 validator |
| `backend/odoo/audit_logic.py` | Phase 8 audit |
| `backend/odoo/cleanup_portfolio_data.py` | Phase 8 cleanup |
| `backend/odoo/repair_odoo_records.py` | Phase 8 repair |
| `backend/config/settings.py` | ETL/Mart config |
| `backend/config/database.py` | Database config |
| `backend/etl/*` | ETL pipeline — untouched |
| `backend/analytics/*` | Analytics — untouched |
| `backend/database/ddl/*` | DDL — untouched |

### 7.2 Files to Archive (ARCHIVE)

| File | Reason |
|---|---|
| `backend/scripts/dataset_generator.py` | Old BIDSS-prefixed generator; references `YEAR = 2024`, uses hardcoded BIDSS master data, direct SQL wipes, direct ORM env access. Incompatible with Phase 9 requirements. Move to `archive/phase6/dataset_generator.py` |
| `backend/generate_extra_transactions_v2.py` | Old BIDSS-prefixed extra transaction script using `datetime.now()`, direct ORM env. Move to `archive/phase6/generate_extra_transactions_v2.py` |
| `backend/fix_dashboard.py` | One-off fix script; already superseded by Phase 8 repair logic. Move to `archive/phase6/fix_dashboard.py` |
| `backend/odoo/unlock_portfolio.sql` | One-off Phase 8 SQL scripts. Move to `archive/phase8/` |
| `backend/odoo/unlock_portfolio_2.sql` | Same |
| `backend/odoo/unlock_portfolio_3.sql` | Same |
| `backend/odoo/unlock_portfolio_4.sql` | Same |
| `backend/odoo/fix_duplicates.sql` | Same |

### 7.3 Files to Refactor (REFACTOR)

None. Phase 9 creates new files and does not modify existing Phase 8 files.

### 7.4 Files to Create (CREATE)

| File | Responsibility |
|---|---|
| `backend/phase9/config.py` | Scenario configuration: seed, dates, monthly targets, customer/supplier segments, category rules |
| `backend/phase9/demand_planner.py` | Project annual demand per product, compute average daily demand, classify movement profiles |
| `backend/phase9/customer_allocator.py` | Allocate 720 SO to 48 customers across 4 segments |
| `backend/phase9/supplier_allocator.py` | Allocate 240 PO to 24 suppliers across 4 segments, respecting supplierinfo |
| `backend/phase9/opening_inventory.py` | Create opening inventory adjustment for 240 products |
| `backend/phase9/sales_generator.py` | Generate SO + confirm + delivery + invoice + payment |
| `backend/phase9/purchase_generator.py` | Generate PO + confirm + receipt + bill + payment |
| `backend/phase9/inventory_ops.py` | Generate 24 internal transfers + 12 scrap operations |
| `backend/phase9/event_scheduler.py` | Build chronological event queue for the full year |
| `backend/phase9/batch_tags.py` | Deterministic reference generation and idempotency logic |
| `backend/phase9/cleanup_phase9.py` | Safe cleanup of Phase 9 batch for re-generation |
| `backend/phase9/run_phase9.py` | CLI orchestrator with gate subcommands |
| `backend/validation/validate_phase9.py` | Automated Phase 9 validation suite |
| `backend/phase9/__init__.py` | Package init |
| `docs/phase9/transaction_data_contract.md` | Locked data contract tables |

---

## 8–11. Files Detail: Keep / Refactor / Archive / Create

See Section 7 above. Each CREATE file is detailed in Sections 12–24 below.

---

## 12. Transaction Data Contract

### 12.1 Sales Orders

| Field | Value |
|---|---|
| Total SO | 720 |
| Lines per SO | 1–5 (avg 2.8–3.6) |
| Total SO lines | 2,016–2,592 |
| Reference field | `sale.order.client_order_ref` |
| Reference pattern | `PORTFOLIO_2026_V1-SO-NNNN` |

### 12.2 Purchase Orders

| Field | Value |
|---|---|
| Total PO | 240 |
| Lines per PO | 2–8 (avg 3.5–5.5) |
| Total PO lines | 840–1,320 |
| Reference field | `purchase.order.partner_ref` |
| Reference pattern | `PORTFOLIO_2026_V1-PO-NNNN` |

### 12.3 Other Operations

| Operation | Count | Reference field | Reference pattern |
|---|---:|---|---|
| Internal Transfers | 24 | `stock.picking.origin` | `PORTFOLIO_2026_V1-INT-NN` |
| Scrap Operations | 12 | `stock.scrap.origin` | `PORTFOLIO_2026_V1-SCRAP-NN` |
| Customer Invoices | derived from SO | `account.move.ref` | `PORTFOLIO_2026_V1-INV-NNNN` |
| Vendor Bills | derived from PO | `account.move.ref` | `PORTFOLIO_2026_V1-BILL-NNNN` |

---

## 13. Monthly Scenario Contract

### 13.1 Monthly Distribution

| Month | SO | PO | Phase | Key Event |
|---|---:|---:|---|---|
| January | 60 | 18 | Baseline | Normal operations, opening inventory |
| February | 58 | 18 | Baseline | Normal operations |
| March | 48 | 15 | **Disruption** | 3–5 suppliers delayed (+4–8 days LT); on-time receipt 55–70%; revenue 65–80% of baseline |
| April | 55 | 32 | **Procurement Response** | Backup suppliers activated; PO value 130–145% of baseline; delivery improving |
| May | 60 | 28 | **Accumulation** | Delayed March/April receipts arrive; inventory value peaks; overstock appears |
| June | 62 | 20 | Correction | Purchasing decreases; sales recover |
| July | 63 | 18 | Correction | Excess stock absorbs demand |
| August | 64 | 17 | Correction | Stock coverage returning to target |
| September | 61 | 18 | Correction | Supplier on-time returns to 80–95% |
| October | 62 | 18 | Stabilization | Revenue near/above baseline |
| November | 63 | 18 | Stabilization | Purchasing stabilizes |
| December | 64 | 20 | Stabilization | Some transactions intentionally left open |
| **Total** | **720** | **240** | | |

### 13.2 Monthly Scenario Mechanisms

#### January–February: Baseline
- **Demand factor:** `so_weight = 1.0`
- **Procurement factor:** `po_weight = 1.0`
- **Supplier lead time:** Product's `supplierinfo.delay` as-is (1–14 days from Phase 8)
- **On-time receipt rate:** 85–95% (receipt date = PO date + lead_time ± random(0, 2))
- **Validation:** Avg monthly revenue within ±10% of median

#### March: Supply Disruption
- **Demand factor:** `so_weight = 0.80` (SO count drops to 48)
- **Procurement factor:** `po_weight = 0.83` (PO count drops to 15)
- **Affected suppliers:** 3–5 Strategic/Regular suppliers (selected deterministically with seed)
- **Lead time change:** Affected supplier lead time += random(4, 8) days
- **On-time receipt rate:** 55–70% (delayed receipts are scheduled but not completed in March)
- **Revenue impact:** Revenue = 65–80% of Jan–Feb average
- **Delivery impact:** 15–25% of March deliveries delayed (assigned + waiting state)
- **Validation:** Monthly revenue < 0.80 × Jan–Feb avg; on-time receipt < 70%

#### April: Procurement Response
- **Demand factor:** `so_weight = 0.92` (55 SO = slight recovery)
- **Procurement factor:** `po_weight = 1.78` (PO count rises to 32)
- **Backup suppliers:** Increase PO allocation to backup segment by 2–3× baseline
- **Purchase value:** 130–145% of Jan–Feb average purchase value
- **Delivery improvement:** Delayed March deliveries begin completing (receipts arriving)
- **Validation:** PO count = 32; purchase value within 130–145% range

#### May: Inventory Accumulation
- **Demand factor:** `so_weight = 1.0` (60 SO = full recovery)
- **Procurement factor:** `po_weight = 1.56` (PO count still elevated at 28)
- **Purchase value:** 115–130% of baseline
- **Stock impact:** March/April delayed receipts complete; inventory value increases
- **Overstock:** 20–30 products cross into overstock territory
- **Validation:** Inventory value > Jan level; overstock products identified

#### June–September: Correction
- **Demand factor:** Gradually increasing from 1.03 to 1.02
- **Procurement factor:** Gradually decreasing from 1.11 to 1.0
- **Stock correction:** Products with excess stock skip new PO creation
- **Supplier on-time:** Returns to 80–95%
- **Validation:** Stock coverage trending toward healthy range

#### October–December: Stabilization
- **Demand factor:** `so_weight = 1.03–1.07`
- **Procurement factor:** `po_weight = 1.0–1.11`
- **Revenue:** Near or slightly above baseline
- **December specifics:** 15–25 SO left in draft/sent; 5–10 deliveries pending; 5–10 PO receipts pending
- **Validation:** End-of-year state counts match Section 14 targets

---

## 14. Customer Allocation Plan

### 14.1 Segment Definition

| Segment | Count | Annual Orders/Customer | Min Total | Max Total |
|---|---:|---|---:|---:|
| Strategic | 8 | 36–54 | 288 | 432 |
| Regular | 16 | 12–24 | 192 | 384 |
| Occasional | 14 | 3–8 | 42 | 112 |
| One-time | 10 | exactly 1 | 10 | 10 |
| **Sum** | **48** | | **532** | **938** |

### 14.2 Allocation Algorithm

Target: exactly 720 orders.

1. **Fix one-time customers:** Assign exactly 1 order each → 10 orders consumed.
2. **Fix minimum for each segment:**
   - Strategic: 8 × 36 = 288
   - Regular: 16 × 12 = 192
   - Occasional: 14 × 3 = 42
   - Subtotal minimum: 288 + 192 + 42 + 10 = 532
3. **Remaining pool:** 720 − 532 = 188 orders to distribute.
4. **Distribution:** Use `random.Random(26072026)` to distribute the 188 remaining orders:
   - Strategic customers each get +0 to +18 additional (max per customer = 54)
   - Regular customers each get +0 to +12 additional (max per customer = 24)
   - Occasional customers each get +0 to +5 additional (max per customer = 8)
5. **Balancing loop:** If total exceeds 720, reduce from the customer with the highest count. If below, add to a random strategic customer.
6. **One-time lockout:** After allocation, assert each one-time customer has exactly 1 order. No further orders may be assigned.
7. **Monthly spread:** Each customer's orders are spread across 12 months using weighted random, with strategic customers present in at least 8 months.

### 14.3 Revenue Guardrails

| Rule | Min | Max | Enforcement |
|---|---|---|---|
| Top 8 revenue share | 55% | 65% | Strategic customers get higher-value product affinity |
| Max single customer | — | 15% | Cap enforced during allocation; if exceeded, redistribute lines |
| Regular customer share | 22% | 32% | Product mix adjusted |
| Occasional + One-time share | — | remainder | Natural from lower order count |
| Customers with ≥1 completed order | 80% | — | At least 39 of 48 customers |
| One-time customers with exactly 1 order | 10 | 10 | Enforced in allocation |

### 14.4 Product-Customer Affinity

| Customer Segment | Primary Categories | Secondary Categories |
|---|---|---|
| Strategic (mining/construction) | Heavy Equipment, Engine/Hydraulic Parts | Undercarriage, Filters |
| Regular (service/maintenance) | Engine/Hydraulic Parts, Filters/Maintenance | Undercarriage, Consumables |
| Occasional (smaller firms) | Filters/Maintenance, Consumables | Undercarriage |
| One-time (special purchase) | Any single category (randomly assigned) | — |

---

## 15. Supplier Allocation Plan

### 15.1 Segment Definition

| Segment | Count | Annual PO/Supplier | Min Total | Max Total |
|---|---:|---|---:|---:|
| Strategic | 5 | 24–36 | 120 | 180 |
| Regular | 10 | 6–14 | 60 | 140 |
| Backup | 6 | 2–6 | 12 | 36 |
| Occasional | 3 | 1–3 | 3 | 9 |
| **Sum** | **24** | | **195** | **365** |

### 15.2 Allocation Algorithm

Target: exactly 240 POs.

1. **Fix minimum:** Strategic 5 × 24 = 120, Regular 10 × 6 = 60, Backup 6 × 2 = 12, Occasional 3 × 1 = 3 → Total min = 195
2. **Remaining pool:** 240 − 195 = 45
3. **Distribution:** Spread 45 using weighted random within each segment's max bounds.
4. **Supplier-product constraint:** PO lines can only contain products where the supplier has a `product.supplierinfo` mapping.
5. **Disruption scenario:** During March, 3–5 strategic/regular suppliers have inflated lead times. During April, backup suppliers receive 2–3× their baseline PO count.
6. **Monthly allocation:** Strategic suppliers appear in at least 8 of 12 months.

### 15.3 Purchase Value Guardrails

| Rule | Min | Max |
|---|---|---|
| Top 5 supplier purchase value share | 60% | 70% |
| Max single supplier share | — | 25% |
| Backup supplier usage in April–May | 2–3× baseline | — |

---

## 16. Product Demand Plan

### 16.1 Product Participation

| Metric | Min | Max |
|---|---|---|
| Products sold ≥ 1 time | 215 | 225 |
| Products with zero demand | 15 | 25 |
| Products qualifying for moving-average forecast (≥ 4 months sold) | 140 | 180 |
| Max single product revenue share | — | 12% |
| Top 20% (48 products) revenue share | 55% | 70% |

### 16.2 Sales Quantity per SO Line by Category

| Category | Min Qty | Max Qty |
|---|---:|---:|
| Heavy Equipment | 1 | 2 |
| Engine/Hydraulic Parts | 1 | 5 |
| Undercarriage Parts | 1 | 8 |
| Filters/Maintenance | 2 | 30 |
| Consumables | 5 | 80 |

### 16.3 Purchase Quantity per PO Line by Category

| Category | Min Qty | Max Qty |
|---|---:|---:|
| Heavy Equipment | 1 | 2 |
| Engine/Hydraulic Parts | 2 | 12 |
| Undercarriage Parts | 4 | 20 |
| Filters/Maintenance | 20 | 120 |
| Consumables | 50 | 300 |

### 16.4 Demand Planning Method

1. Each product gets an **annual demand projection** based on its category:
   - Heavy Equipment: 2–8 units/year
   - Engine/Hydraulic Parts: 10–60 units/year
   - Undercarriage Parts: 15–80 units/year
   - Filters/Maintenance: 50–400 units/year
   - Consumables: 100–800 units/year
2. Products are ranked by projected demand; top 20% labeled "fast-moving", middle 60% "normal-moving", bottom 20% "slow-moving".
3. 15–25 products are designated "no-demand" (zero projected annual demand).

---

## 17. Opening Inventory Plan

### 17.1 Stock Coverage by Movement Profile

| Profile | Opening Stock Coverage (days) | Method |
|---|---|---|
| Fast-moving | 45–75 | `avg_daily_demand × random(45, 75)` |
| Normal-moving | 60–100 | `avg_daily_demand × random(60, 100)` |
| Slow-moving | 120–210 | `avg_daily_demand × random(120, 210)` |
| No-demand | 0–5 units | 60% get 0, 40% get random(1, 5) |

### 17.2 Calculation Steps

1. Compute `annual_demand` per product (from Section 16.4).
2. Compute `avg_daily_demand = annual_demand / 365`.
3. Assign movement profile (fast/normal/slow/no-demand).
4. Compute `opening_qty = int(round(avg_daily_demand × coverage_days))`.
5. Ensure `opening_qty ≥ 0` and is integer.
6. Compute `opening_value = opening_qty × product.standard_price`.

### 17.3 Odoo Workflow

1. Search `stock.quant` for each product at PAN warehouse stock location.
2. If quant exists, set `inventory_quantity = opening_qty`.
3. If quant does not exist, create quant with `inventory_quantity = opening_qty`.
4. Call `action_apply_inventory()` on the quant batch.
5. All operations use XML-RPC ORM — no direct SQL.
6. Inventory date: 2026-01-01.

### 17.4 Validation

- Total products with opening stock > 0: 215–230
- Total products with opening stock = 0: 10–25
- No negative quantities
- Sum of `opening_qty × standard_price` constitutes opening inventory value

---

## 18. Sales Workflow Plan

### 18.1 Workflow Sequence

```
Draft SO → action_confirm() → Delivery Order auto-created
  → Set move quantities → button_validate() on picking
    → _create_invoices() → invoice.action_post()
      → account.payment.register → action_create_payments()
```

### 18.2 Date Rules

| Date | Rule |
|---|---|
| `sale.order.date_order` | Generated date within assigned month |
| `stock.picking.scheduled_date` | `date_order + random(1, 5)` business days |
| `stock.picking.date_done` | `scheduled_date + random(0, 3)` business days (if completed) |
| `account.move.invoice_date` | `date_done` (day of delivery completion) |
| `account.payment.payment_date` | `invoice_date + random(1, 30)` days |

### 18.3 State Targets (from 720 SO)

| State | Count | Percentage |
|---|---:|---|
| Confirmed/Sale (completed workflow) | 662 | 92% |
| Draft or Sent | 29 | 4% |
| Cancelled | 29 | 4% |
| **Total** | **720** | **100%** |

### 18.4 Delivery Targets (from 662 confirmed SO)

| State | Count | Percentage |
|---|---:|---|
| Done | 596 | 90% |
| Ready or Waiting | 40 | 6% |
| Late | 16 | 2.4% |
| Backorder/Partial | 10 | 1.5% |
| **Total** | **662** | |

### 18.5 Invoice and Payment Targets

- Invoiced: 90–95% of 596 completed deliveries → 537–566 invoices
- Posted: 85–92% of created invoices → 456–521 posted
- Paid: 75–85% of posted invoices → 342–443 paid

### 18.6 Implementation Detail

**File:** `backend/phase9/sales_generator.py`

**Key function:** `generate_sales_orders(month: int, count: int, customer_plan: dict, product_pool: list) -> list`

**Processing:**
1. Select customer from month's allocation pool
2. Select 1–5 products using category affinity weights
3. Generate quantities within category bounds
4. Apply discount: 75% → 0%, 20% → random(2,5)%, 5% → random(6,10)%
5. Verify: no duplicate product per SO, no service product, qty > 0
6. Create SO via ORM with `client_order_ref = PORTFOLIO_2026_V1-SO-NNNN`
7. Check idempotency: if reference already exists, skip
8. Confirm, deliver, invoice, pay based on state allocation

---

## 19. Purchase Workflow Plan

### 19.1 Workflow Sequence

```
Draft PO → button_confirm() → Receipt auto-created
  → Set move quantities → button_validate() on picking
    → action_create_invoice() → bill.action_post()
      → account.payment.register → action_create_payments()
```

### 19.2 Procurement Logic

```python
required_qty = (
    forecast_demand_during_lead_time
    + safety_stock
    - projected_available_stock
)
planned_purchase_qty = max(0, required_qty)
```

Where:
- `forecast_demand_during_lead_time = avg_daily_demand × (supplier_lead_time + safety_buffer)`
- `safety_stock = safety_factor × stddev_daily_demand × sqrt(lead_time)`
- `projected_available_stock = current_stock - reserved_qty`

### 19.3 Date Rules

| Date | Rule |
|---|---|
| `purchase.order.date_order` | Generated date within assigned month |
| `purchase.order.date_planned` | `date_order + supplier_lead_time` |
| Receipt `date_done` | `date_planned + random(-2, +3)` days (on-time variation) |
| `account.move.invoice_date` | `receipt_date_done + random(1, 5)` days |
| `account.payment.payment_date` | `invoice_date + random(7, 45)` days |

### 19.4 State Targets (from 240 PO)

| State | Count | Percentage |
|---|---:|---|
| Confirmed/Purchase | 221 | 92% |
| Draft or Sent | 10 | 4% |
| Cancelled | 9 | 4% |
| **Total** | **240** | **100%** |

### 19.5 Receipt Targets (from 221 confirmed PO)

| State | Count | Percentage |
|---|---:|---|
| Done | 199 | 90% |
| Ready or Waiting | 13 | 6% |
| Late | 9 | 4% |
| **Total** | **221** | |

### 19.6 Bill and Payment Targets

- Billed: 88–95% of 199 completed receipts → 175–189 bills
- Posted: 85–92% of created bills → 149–174 posted
- Paid: 70–82% of posted bills → 104–143 paid

---

## 20. Inventory Workflow Plan

### 20.1 Internal Transfers (24 total)

- ~2 per month
- Use PAN warehouse internal locations (e.g., PAN/Stock → PAN/Stock/Shelf)
- 18–20 completed (state `done`)
- 4–6 still in `ready` or `waiting` state at year-end
- Reference: `PORTFOLIO_2026_V1-INT-NN`

**Implementation:**
1. Select a product with positive stock at source location
2. Transfer quantity: 5–15% of source location stock
3. No negative source stock allowed
4. Created via `stock.picking` + `stock.move` ORM
5. Completed transfers: `button_validate()` with quantities set
6. Pending transfers: `action_confirm()` only

### 20.2 Scrap Operations (12 total)

- ~1 per month
- Only products with positive stock
- Reference: `PORTFOLIO_2026_V1-SCRAP-NN`

| Category | Max Scrap Qty |
|---|---:|
| Heavy Equipment | 0 (excluded) |
| Engine/Hydraulic | 1 |
| Undercarriage | 1–2 |
| Filters/Maintenance | 1–5 |
| Consumables | 1–10 |

**Implementation:**
1. Select product from eligible categories with positive stock
2. Create `stock.scrap` via ORM
3. Call `do_scrap()`
4. Validate stock was reduced

---

## 21. Invoice and Payment Plan

### 21.1 Customer Invoice Workflow

1. After delivery completion (`picking.state == 'done'`), call `so._create_invoices()`
2. Set `invoice.invoice_date = picking.date_done`
3. For posted invoices: `invoice.action_post()`
4. For paid invoices: Create payment via `account.payment.register`
5. Payment journal: Bank (BNK1)
6. Payment method: Manual

### 21.2 Vendor Bill Workflow

1. After receipt completion, call `po.action_create_invoice()`
2. Set `bill.invoice_date = receipt_date + random(1, 5) days`
3. For posted bills: `bill.action_post()`
4. For paid bills: Create payment via `account.payment.register`
5. Payment journal: Bank (BNK1)
6. Payment method: Manual (outbound)

### 21.3 Due Date Rule

- Customer invoices: `invoice_date + 30 days`
- Vendor bills: `invoice_date + 30 days`
- (Uses Odoo default payment terms; no custom terms needed)

---

## 22. Date and Event Sequence

### 22.1 Processing Order

The event scheduler processes transactions in strict chronological order:

```
For each day in 2026-01-01 to 2026-12-31:
    1. Process PO receipts scheduled for this day
    2. Process SO deliveries scheduled for this day
    3. Create new Sales Orders assigned to this day
    4. Run procurement check → create new POs if needed
    5. Process invoices for completed deliveries/receipts
    6. Process payments for due invoices/bills
```

### 22.2 Date Invariants

1. `SO.date_order` ∈ [2026-01-01, 2026-12-31]
2. `picking.scheduled_date` ≥ `SO.date_order`
3. `picking.date_done` ≥ `SO.date_order` (if completed)
4. `invoice.invoice_date` ≥ `picking.date_done`
5. `payment.payment_date` ≥ `invoice.invoice_date`
6. `PO.date_order` ∈ [2026-01-01, 2026-12-31]
7. `receipt.scheduled_date` = `PO.date_order + lead_time`
8. `receipt.date_done` ≥ `PO.date_order`
9. `bill.invoice_date` ≥ `receipt.date_done`
10. `payment.payment_date` ≥ `bill.invoice_date`

### 22.3 Scenario As-Of Date

All state evaluations use `scenario_as_of_date = 2026-12-31`. No `datetime.now()` calls.

---

## 23. Idempotency and Batch Tagging

### 23.1 Deterministic References

| Model | Field | Pattern | Example |
|---|---|---|---|
| `sale.order` | `client_order_ref` | `PORTFOLIO_2026_V1-SO-NNNN` | `PORTFOLIO_2026_V1-SO-0001` |
| `purchase.order` | `partner_ref` | `PORTFOLIO_2026_V1-PO-NNNN` | `PORTFOLIO_2026_V1-PO-0001` |
| `account.move` (invoice) | `ref` | `PORTFOLIO_2026_V1-INV-NNNN` | `PORTFOLIO_2026_V1-INV-0001` |
| `account.move` (bill) | `ref` | `PORTFOLIO_2026_V1-BILL-NNNN` | `PORTFOLIO_2026_V1-BILL-0001` |
| `stock.picking` (internal) | `origin` | `PORTFOLIO_2026_V1-INT-NN` | `PORTFOLIO_2026_V1-INT-01` |
| `stock.scrap` | `origin` | `PORTFOLIO_2026_V1-SCRAP-NN` | `PORTFOLIO_2026_V1-SCRAP-01` |

### 23.2 Idempotency Rules

1. Before creating any record, search by the deterministic reference
2. If found, skip creation entirely
3. If partially created (e.g., SO exists but delivery not completed), resume from last completed step
4. All operations wrapped in try/except; failures logged but do not halt the batch
5. Random seed `26072026` ensures identical output on re-run

### 23.3 Cleanup for Re-generation

`backend/phase9/cleanup_phase9.py` reverses Phase 9 in this order:
1. Delete payments linked to Phase 9 invoices/bills
2. Cancel and delete invoices/bills with `PORTFOLIO_2026_V1-INV-*` or `PORTFOLIO_2026_V1-BILL-*`
3. Cancel and delete stock pickings linked to Phase 9 SO/PO
4. Cancel and delete POs with `PORTFOLIO_2026_V1-PO-*`
5. Cancel and delete SOs with `PORTFOLIO_2026_V1-SO-*`
6. Reverse opening inventory
7. Delete internal transfers and scrap operations

---

## 24. Validation Rules

### 24.1 Transaction Count Validations

| Test Name | Model | Expected Min | Expected Max | Blocking |
|---|---|---:|---:|---|
| SO total count | `sale.order` | 720 | 720 | CRITICAL |
| PO total count | `purchase.order` | 240 | 240 | CRITICAL |
| Internal transfer count | `stock.picking` (internal) | 24 | 24 | CRITICAL |
| Scrap count | `stock.scrap` | 12 | 12 | CRITICAL |
| SO line count | `sale.order.line` | 2,016 | 2,592 | HIGH |
| PO line count | `purchase.order.line` | 840 | 1,320 | HIGH |

### 24.2 Monthly Distribution Validations

| Test Name | Month | Expected SO | Expected PO | Blocking |
|---|---|---:|---:|---|
| January distribution | 1 | 60 | 18 | CRITICAL |
| February distribution | 2 | 58 | 18 | CRITICAL |
| March distribution | 3 | 48 | 15 | CRITICAL |
| April distribution | 4 | 55 | 32 | CRITICAL |
| May distribution | 5 | 60 | 28 | CRITICAL |
| June distribution | 6 | 62 | 20 | CRITICAL |
| July distribution | 7 | 63 | 18 | CRITICAL |
| August distribution | 8 | 64 | 17 | CRITICAL |
| September distribution | 9 | 61 | 18 | CRITICAL |
| October distribution | 10 | 62 | 18 | CRITICAL |
| November distribution | 11 | 63 | 18 | CRITICAL |
| December distribution | 12 | 64 | 20 | CRITICAL |

### 24.3 Partner Validations

| Test Name | Expected | Blocking |
|---|---|---|
| No new customers created | Customer count still 48 | CRITICAL |
| No new suppliers created | Supplier count still 24 | CRITICAL |
| One-time customers have exactly 1 SO each | 10 customers × 1 | HIGH |
| ≥80% customers have completed order | ≥39 of 48 | HIGH |
| All SOs use PORTFOLIO_2026_V1-CUST-* partners | 100% | CRITICAL |
| All POs use PORTFOLIO_2026_V1-VEND-* partners | 100% | CRITICAL |
| Supplier-product compatibility | All PO lines have valid supplierinfo | CRITICAL |

### 24.4 Product Validations

| Test Name | Expected | Blocking |
|---|---|---|
| No new products created | Template count still 240 | CRITICAL |
| Products sold ≥ 1 | 215–225 | HIGH |
| No-demand products | 15–25 | HIGH |
| No service products in transactions | 0 service lines | CRITICAL |
| No single product > 12% revenue | Max ≤ 12% | HIGH |
| Top 20% products = 55–70% revenue | Within range | HIGH |

### 24.5 Date Validations

| Test Name | Expected | Blocking |
|---|---|---|
| All SO dates in 2026 | 100% | CRITICAL |
| All PO dates in 2026 | 100% | CRITICAL |
| Delivery date ≥ SO date | 100% | CRITICAL |
| Invoice date ≥ delivery date | 100% | CRITICAL |
| Payment date ≥ invoice date | 100% | CRITICAL |
| Receipt date ≥ PO date | 100% | CRITICAL |
| Bill date ≥ receipt date | 100% | CRITICAL |
| No gap months | All 12 months have transactions | CRITICAL |

### 24.6 Financial Validations

| Test Name | Expected | Blocking |
|---|---|---|
| Annual revenue range | Within guardrail (adjusted per Open Q #1) | HIGH |
| Annual purchase value | 65–82% of revenue | HIGH |
| Monthly gross margin | 18–30% | HIGH |
| No negative margin month | 0 | HIGH |
| No zero-revenue month | 0 | CRITICAL |

### 24.7 State Validations

| Test Name | Model | Expected | Blocking |
|---|---|---|---|
| SO confirmed % | `sale.order` | 91–95% | HIGH |
| SO draft/sent % | `sale.order` | 2–5% | MEDIUM |
| SO cancelled % | `sale.order` | 2–4% | MEDIUM |
| Delivery done % | `stock.picking` (outgoing) | 88–93% | HIGH |
| Pending deliveries | `stock.picking` (outgoing) | 8–15 | MEDIUM |
| Late deliveries | `stock.picking` (outgoing) | 3–8 | MEDIUM |
| PO confirmed % | `purchase.order` | 90–95% | HIGH |
| Pending receipts | `stock.picking` (incoming) | 5–10 | MEDIUM |
| Late receipts | `stock.picking` (incoming) | 2–6 | MEDIUM |

### 24.8 Idempotency Validation

| Test Name | Expected | Blocking |
|---|---|---|
| Second run creates 0 new SOs | 0 duplicates | CRITICAL |
| Second run creates 0 new POs | 0 duplicates | CRITICAL |
| All references unique | 0 duplicates | CRITICAL |
| Phase 8 baseline unchanged | All P8 checks still PASS | CRITICAL |

---

## 25. Approval Gates

### Gate 9A — Read-Only Audit

**Required before any code changes:**
- [x] Phase 8 validation confirmed (all PASS)
- [x] File map documented
- [x] Odoo record counts verified
- [x] Transaction models inspected
- [x] Journals and payment methods inspected
- [x] No database mutation performed

**Status:** ✅ COMPLETE — This document is the Gate 9A deliverable.

→ **STOP. Request user approval before proceeding to Gate 9B.**

---

### Gate 9B — Generator Code and Dry-Run

**Deliverables:**
- Generator code implemented in `backend/phase9/`
- No Odoo records created
- Dry-run produces projected counts:
  - Monthly SO/PO totals matching contract
  - Customer allocation matching segments
  - Supplier allocation matching segments
  - Product demand plan printed
  - Opening inventory quantities printed
  - No invalid product-supplier mapping

→ **STOP. Request user approval before proceeding to Gate 9C.**

---

### Gate 9C — January Pilot

**Execute only January:**
- 60 Sales Orders
- 18 Purchase Orders
- January opening inventory (all 240 products)
- January deliveries and receipts
- January invoices, bills, payments

**Validate:**
- Chronology (all dates in January 2026)
- Stock (opening inventory applied correctly)
- Accounting (invoices posted, payments registered)
- Customer/supplier reuse (no new partners)
- Odoo Overview (visible in Sales/Purchase/Inventory)
- Cleanup and rerun (idempotency test)

→ **STOP. Request user approval before proceeding to Gate 9D.**

---

### Gate 9D — Scenario Pilot Through May

**Generate January–May:**
- Baseline months (Jan–Feb)
- March disruption (fewer SO, delayed receipts)
- April procurement response (elevated PO count)
- May inventory accumulation

**Validate:**
- Scenario trends visible in actual data
- March revenue < baseline
- April PO count = 32
- May inventory elevated

→ **STOP. Request user approval before proceeding to Gate 9E.**

---

### Gate 9E — Full-Year Generation

**Generate January–December:**
- All 720 SO, 240 PO
- All internal transfers and scrap operations
- All invoices, bills, payments
- End-of-year open transactions

→ **STOP before ETL. Request user approval before proceeding to Gate 9F.**

---

### Gate 9F — Full Validation and Idempotency

**Run complete validation suite:**
- All count validations
- All date validations
- All financial validations
- All state validations
- Idempotency: second run creates 0 duplicates
- Phase 8 baseline verification

→ **STOP. Produce final validation report.**

---

## 26. Rollback Strategy

### 26.1 Per-Gate Rollback

Each gate can be independently reversed:

1. **Gate 9C (January):** Run `cleanup_phase9.py --month 1`
2. **Gate 9D (Jan–May):** Run `cleanup_phase9.py --month 1-5`
3. **Gate 9E (Full year):** Run `cleanup_phase9.py --all`

### 26.2 Cleanup Order

```
1. Delete account.payment (linked to Phase 9 invoices/bills)
2. Cancel account.move (invoices/bills) → set state='draft' → unlink
3. Cancel stock.picking (deliveries/receipts) → unlink stock.move → unlink picking
4. Cancel purchase.order → unlink purchase.order.line → unlink purchase.order
5. Cancel sale.order → unlink sale.order.line → unlink sale.order
6. Delete stock.scrap
7. Reverse stock.quant (opening inventory) → set inventory_quantity=0 → apply
```

### 26.3 Safety

- All cleanup uses ORM, not direct SQL
- State must be reset to `cancel`/`draft` before `unlink`
- If ORM refuses (e.g., done pickings), use the Phase 8 unlock pattern (SQL state reset → ORM delete)
- Cleanup is idempotent: re-running after full cleanup produces no errors

---

## 27. Risks and Mitigation

| Risk | Impact | Mitigation |
|---|---|---|
| ORM refuses to delete done pickings | Cleanup blocked | Use SQL state reset (tested in Phase 8) before ORM unlink |
| Odoo server timeout on large batch | Partial creation | Process in monthly batches with commit after each month |
| Revenue guardrail unreachable | Financial validation fails | Adjust guardrail or revise Phase 8 prices (Open Q #1) |
| XML-RPC timeout | Connection lost | Retry logic with exponential backoff; monthly commit boundaries |
| Stock goes negative | Delivery blocked | Check stock availability before delivery; leave pending if insufficient |
| Payment registration fails | Invoice remains unpaid | Catch exception, log, continue; unpaid invoice is valid state |
| Old BIDSS data interferes | Wrong partners/products selected | All queries filter by `PORTFOLIO_2026_V1-*` prefix exclusively |
| Multiple warehouses cause confusion | Wrong picking types used | Filter by PAN warehouse picking types only |

---

## 28. Definition of Done

- [ ] Phase 8 baseline remains unchanged (48 cust, 24 supp, 240 prod)
- [ ] Exactly 720 Sales Orders exist
- [ ] Exactly 240 Purchase Orders exist
- [ ] Monthly order counts match the locked contract
- [ ] Exactly 24 internal transfers exist
- [ ] Exactly 12 scrap operations exist
- [ ] Customer and supplier records are reused (no new partners)
- [ ] All products come from Phase 8 product master
- [ ] No service product in transactions
- [ ] Sales and Purchase lines use valid quantities within category bounds
- [ ] Procurement is linked to demand and projected stock
- [ ] Transaction dates are chronologically valid
- [ ] Odoo Sales, Purchase, Inventory, and Invoicing pages show data
- [ ] Odoo Inventory Overview contains limited realistic backlog
- [ ] No RPC_ERROR occurs
- [ ] No Missing Record error occurs
- [ ] No duplicate portfolio references exist
- [ ] Transaction distribution is within business guardrails
- [ ] Scenario trends appear from actual transactions
- [ ] Cleanup and full regeneration are reproducible
- [ ] Second run creates zero duplicate transactions
- [ ] Phase 9 validation exits with code 0
- [ ] No ETL, Mart, DSS, or Power BI work has started

---

## 29. Remaining Questions

### Open Question #1 — Revenue Guardrail vs Product Prices

> [!IMPORTANT]
> Phase 8 created all 240 products with costs in the Rp 10K–1M range (uniform `random.randint(10, 1000) * 1000`). This includes "Heavy Equipment" items that in reality cost Rp 1.5B+.
>
> With current prices, the maximum achievable annual revenue is approximately **Rp 50B–80B**, which is well below the stated guardrail of **Rp 180B–320B**.
>
> **Options:**
> 1. **Adjust revenue guardrail** to Rp 30B–80B to match existing prices (no Phase 8 changes needed)
> 2. **Revise Phase 8 product prices** using category-appropriate ranges before Phase 9 starts
>
> **Recommendation:** Option 2 is more realistic for portfolio quality, but requires a Phase 8 modification. The user must decide.

### Open Question #2 — Old BIDSS Data

> 550 old BIDSS products, 300 customers, and 300 vendors remain in the database. They do not interfere with Phase 9 (all queries use `PORTFOLIO_2026_V1-*` filter), but they clutter the Odoo UI.
>
> **Question:** Should Phase 9 include a cleanup step for old BIDSS data, or leave it as-is?

---

## 30. Final GO/NO-GO Recommendation

### Assessment

| Criterion | Status |
|---|---|
| Phase 8 preconditions | ✅ All 17 checks PASS |
| Codebase understood | ✅ All files inspected |
| Master data verified | ✅ 48 cust, 24 supp, 240 prod, 456 mappings |
| Transaction models verified | ✅ Journals, payment methods, picking types confirmed |
| Revenue guardrail feasibility | ⚠️ Requires user decision on Open Q #1 |
| Implementation plan complete | ✅ All 30 sections documented |

### Recommendation

**CONDITIONAL GO** — Phase 9 implementation may proceed after the user resolves:

1. **Open Question #1:** Revenue guardrail adjustment OR Phase 8 price revision
2. **Open Question #2:** Old BIDSS data cleanup (non-blocking)

Once Q #1 is resolved, begin at **Gate 9B** (Generator Code and Dry-Run).

---

## Task Matrix

### P0 — Critical Path Tasks

| Task ID | Priority | Problem | Target | File | Odoo Model | Dependency | Validation |
|---|---|---|---|---|---|---|---|
| P9-CFG-01 | P0 | No scenario config exists | Centralized config with seed, dates, monthly targets, segments | `backend/phase9/config.py` | — | None | Config loads without error |
| P9-DEM-01 | P0 | No demand projection exists | Projected annual demand per product; movement profile classification | `backend/phase9/demand_planner.py` | `product.template`, `product.category` | P9-CFG-01 | 215–225 products with demand > 0 |
| P9-CAL-01 | P0 | No customer allocation exists | 720 SO allocated to 48 customers across 4 segments | `backend/phase9/customer_allocator.py` | `res.partner` | P9-CFG-01 | sum(allocations) = 720; one-time = 10 × 1 |
| P9-SAL-01 | P0 | No supplier allocation exists | 240 PO allocated to 24 suppliers across 4 segments | `backend/phase9/supplier_allocator.py` | `res.partner`, `product.supplierinfo` | P9-CFG-01 | sum(allocations) = 240; all PO lines have supplierinfo |
| P9-INV-01 | P0 | No opening inventory | 240 products with demand-derived opening stock | `backend/phase9/opening_inventory.py` | `stock.quant` | P9-DEM-01 | 215–230 products with qty > 0 |
| P9-EVT-01 | P0 | No event scheduler | Chronological event queue for full year | `backend/phase9/event_scheduler.py` | — | P9-CAL-01, P9-SAL-01 | All events ordered by date |
| P9-SOG-01 | P0 | No SO generator | 720 SO with full workflow (confirm → deliver → invoice → pay) | `backend/phase9/sales_generator.py` | `sale.order`, `stock.picking`, `account.move` | P9-EVT-01, P9-INV-01 | SO count = 720; dates valid |
| P9-POG-01 | P0 | No PO generator | 240 PO with full workflow (confirm → receipt → bill → pay) | `backend/phase9/purchase_generator.py` | `purchase.order`, `stock.picking`, `account.move` | P9-EVT-01, P9-INV-01 | PO count = 240; supplier-product valid |
| P9-STO-01 | P0 | No inventory ops generator | 24 transfers + 12 scrap operations | `backend/phase9/inventory_ops.py` | `stock.picking`, `stock.scrap` | P9-INV-01 | Transfer count = 24; scrap count = 12 |

### P1 — Infrastructure Tasks

| Task ID | Priority | Problem | Target | File | Dependency | Validation |
|---|---|---|---|---|---|---|
| P9-TAG-01 | P1 | No batch tagging | Deterministic reference generation | `backend/phase9/batch_tags.py` | None | All refs match pattern |
| P9-CLN-01 | P1 | No Phase 9 cleanup | Safe batch reversal for re-generation | `backend/phase9/cleanup_phase9.py` | None | Cleanup leaves Phase 8 intact |
| P9-ORC-01 | P1 | No Phase 9 orchestrator | CLI with gate subcommands | `backend/phase9/run_phase9.py` | All P0 tasks | All gates executable |
| P9-VAL-01 | P1 | No Phase 9 validation | Automated validation suite | `backend/validation/validate_phase9.py` | All P0 tasks | Exit code 0 when all pass |

### P2 — Documentation Tasks

| Task ID | Priority | Problem | Target | File | Dependency |
|---|---|---|---|---|---|
| P9-DOC-01 | P2 | No data contract doc | Locked data contract tables | `docs/phase9/transaction_data_contract.md` | P9-CFG-01 |
| P9-ARC-01 | P2 | Old scripts clutter codebase | Archive legacy scripts | `archive/phase6/`, `archive/phase8/` | None |

---

*End of Implementation Plan.*
