# Analytical Data Contract — Phase 11

**Date:** August 3, 2026  
**Project:** Odoo Business Intelligence Decision Support System (OBIDSS)  
**Company:** PT Prima Alat Nusantara (Company ID: 2)  
**Target Horizon:** Fiscal Year 2026 (Jan 1, 2026 – Dec 31, 2026)

---

## 1. Forecast Data Contract (`mart.fact_forecast_monthly`)

- **Business Purpose**: Predict monthly demand quantity per product using 3-Month Moving Average (MA3) and calculate forecast accuracy metrics (MAE, WAPE).
- **Source Table**: `mart.fact_sales`, `mart.dim_product`, `mart.dim_date`
- **Required Columns**: `product_id`, `date_id`, `quantity`
- **Grain**: One row per product (`sk_product_id`) per month (`month_id`, format YYYYMM)
- **Filter**: Confirmed sales demand only (`fact_sales`), dates within FY 2026
- **Measurement Unit**: Quantity units (pieces / units)
- **Formula**:
  $$\text{MA3 Forecast}_{i,t} = \frac{\text{Actual}_{i,t-1} + \text{Actual}_{i,t-2} + \text{Actual}_{i,t-3}}{3}$$
- **Null Handling**: First 3 months of FY 2026 (202601, 202602, 202603) set `ma3_forecast_qty = NULL` and `forecast_available = FALSE`.
- **Zero Handling**: Zero demand is valid actual demand (`0`). Division by zero in MAPE excluded when `actual_qty = 0`.
- **Output Table**: `mart.fact_forecast_monthly`
- **Known Limitation**: Single fiscal year (12 months) means forecast is available for months 202604–202612 (9 evaluation months).

---

## 2. EOQ Data Contract (`mart.fact_decision_support`)

- **Business Purpose**: Determine optimal order quantity per product to minimize total inventory ordering and holding costs.
- **Source Table**: `mart.fact_sales`, `mart.dim_product`
- **Required Columns**: `sk_product_id`, `annual_demand` (sum of quantity), `standard_price` (unit cost in IDR)
- **Grain**: One row per product (`sk_product_id`)
- **Filter**: Active products with selling/list price > 0
- **Measurement Unit**: Units (quantity) & IDR (currency)
- **Formula**:
  $$H = \text{standard\_price} \times \text{HOLDING\_COST\_RATE} \quad (20\%)$$
  $$\text{EOQ} = \sqrt{\frac{2 \times D \times S}{H}} = \sqrt{\frac{2 \times \text{annual\_demand} \times 500,000}{H}}$$
- **Null Handling**: If product has no sales history, `annual_demand = 0`.
- **Zero Handling**: If `holding_cost = 0` or `annual_demand = 0`, `eoq = 0` (no order needed).
- **Output Table**: `mart.fact_decision_support` (Column `eoq`)

---

## 3. Safety Stock & ROP Data Contract (`mart.fact_decision_support`)

- **Business Purpose**: Calculate buffer inventory to prevent stockouts and reorder point threshold for automated purchasing alerts.
- **Source Table**: `mart.fact_sales`, `mart.fact_purchase`, `mart.dim_product`
- **Required Columns**: `quantity`, `date_id`, `lead_time_days`
- **Grain**: One row per product (`sk_product_id`)
- **Measurement Unit**: Units & Days (Lead time)
- **Formula**:
  $$\text{Safety Stock} = (\text{max\_daily\_demand} \times \text{max\_lead\_time}) - (\text{avg\_daily\_demand} \times \text{avg\_lead\_time})$$
  $$\text{ROP} = (\text{avg\_daily\_demand} \times \text{avg\_lead\_time}) + \text{Safety Stock}$$
- **Null Handling**: Default `avg_lead_time = 5` days if no purchase history exists.
- **Zero Handling**: `Safety Stock = max(0, Safety Stock)` (prevent negative safety stock).
- **Output Table**: `mart.fact_decision_support` (Columns `safety_stock`, `rop`)

---

## 4. Inventory Classification & Recommendation Data Contract

- **Business Purpose**: Categorize inventory velocity and assign actionable reorder recommendations (P1–P5).
- **Source Table**: `mart.fact_sales`, `mart.fact_inventory`, `mart.dim_product`
- **Grain**: One row per product
- **Classification Rules**:
  - `Fast Moving`: Turnover $\ge 4.0$
  - `Normal`: Turnover $2.0 - 3.99$
  - `Slow Moving`: Turnover $0.5 - 1.99$
  - `Dead Stock`: Turnover $< 0.5$
- **Recommendation Rules**:
  - `P1 (Critical Reorder)`: Stock $\le$ ROP AND Fast Moving
  - `P2 (Reorder)`: Stock $\le$ ROP
  - `P3 (Slow Moving Warning)`: Stock $>$ ROP AND Slow Moving
  - `P4 (Overstock Warning)`: Stock $> 2 \times$ ROP
  - `P5 (Normal Stock)`: All other balanced products
- **Output Table**: `mart.fact_decision_support`

---

## 5. Supplier Performance Scoring Data Contract (`mart.fact_supplier_score`)

- **Business Purpose**: Evaluate and grade suppliers across 4 operational dimensions.
- **Source Table**: `mart.fact_purchase`, `mart.dim_vendor`
- **Required Columns**: `vendor_id`, `lead_time_days`, `price_unit`, `quantity`
- **Grain**: One row per supplier (`sk_vendor_id`)
- **Weights**:
  - On-Time Delivery (OTD): 30%
  - Price Competitiveness: 25%
  - Volume Reliability: 25%
  - Lead-Time Consistency: 20%
- **Grade Boundaries**:
  - Grade A: Score $\ge 80.0$
  - Grade B: Score $60.0 - 79.9$
  - Grade C: Score $< 60.0$
- **Output Table**: `mart.fact_supplier_score`
