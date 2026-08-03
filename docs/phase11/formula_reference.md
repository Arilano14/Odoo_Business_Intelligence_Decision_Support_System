# Formula Reference Specification — Phase 11 Analytics & DSS

**Date:** August 3, 2026  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. Moving Average Forecast (MA3)

- **Formula**:
  $$\text{MA3 Forecast}_{i,t} = \frac{\text{Actual}_{i,t-1} + \text{Actual}_{i,t-2} + \text{Actual}_{i,t-3}}{3}$$
- **Variables**: `actual_qty` (Monthly Sales Volume in units)
- **Units**: Quantity (units)
- **Source Field**: `mart.fact_sales.quantity` aggregated by `SUBSTRING(date_id::text, 1, 6)`
- **Assumptions**: Demand follows short-term historical trend; requires 3 prior months of history (`min_periods=3`).
- **Null / Zero Handling**: Months 202601–202603 set `ma3_forecast = 0` and `forecast_available = False`.

---

## 2. Forecast Error Metrics

- **MAE (Mean Absolute Error)**:
  $$\text{MAE} = \frac{1}{N} \sum |\text{Actual} - \text{Forecast}|$$
- **WAPE (Weighted Absolute Percentage Error)**:
  $$\text{WAPE} = \frac{\sum |\text{Actual} - \text{Forecast}|}{\sum \text{Actual}} \times 100\%$$
- **MAPE (Mean Absolute Percentage Error)**:
  $$\text{MAPE} = \frac{1}{N} \sum_{A > 0} \left| \frac{\text{Actual} - \text{Forecast}}{\text{Actual}} \right| \times 100\%$$
- **Zero Handling**: MAPE is calculated only for product-months where $\text{Actual} > 0$ to prevent division by zero.

---

## 3. Economic Order Quantity (EOQ)

- **Formula**:
  $$\text{EOQ} = \sqrt{\frac{2 \times D \times S}{H}}$$
- **Variables**:
  - $D = \text{annual\_demand}$ (Total units sold in 2026)
  - $S = \text{ORDERING\_COST} = \text{Rp } 500,000$ per purchase order
  - $H = \text{standard\_price} \times \text{HOLDING\_COST\_RATE} \quad (\text{rate} = 20\%)$
- **Units**: Quantity (units)
- **Assumptions**: Constant annual demand rate, constant unit cost, constant ordering cost.

---

## 4. Safety Stock & Reorder Point (ROP)

- **Safety Stock**:
  $$\text{Safety Stock} = (\text{max\_daily\_demand} \times \text{max\_lead\_time}) - (\text{avg\_daily\_demand} \times \text{avg\_lead\_time})$$
- **ROP**:
  $$\text{ROP} = (\text{avg\_daily\_demand} \times \text{avg\_lead\_time}) + \text{Safety Stock}$$
- **Variables**: Daily sales demand stats (`avg_daily_demand`, `max_daily_demand`), supplier lead time stats (`avg_lead_time`, `max_lead_time` in days).
- **Zero / Negative Handling**: $\text{Safety Stock} = \max(0, \text{Safety Stock})$; $\text{ROP} \ge \text{Safety Stock}$.

---

## 5. Supplier Performance Weighted Score

- **Formula**:
  $$\text{Final Score} = 0.30 \times \text{OTD} + 0.25 \times \text{Price} + 0.25 \times \text{Volume} + 0.20 \times \text{Lead Time Consistency}$$
- **Grade Boundaries**:
  - Grade A: Final Score $\ge 80.0$
  - Grade B: Final Score $60.0 - 79.9$
  - Grade C: Final Score $< 60.0$

---

## 6. Contribution & Growth Formulas

- **Revenue Contribution %**:
  $$\text{Revenue Contribution}_{i} = \frac{\text{Product Revenue}_{i}}{\sum \text{Total Sales Revenue}} \times 100\%$$
- **Purchase Contribution %**:
  $$\text{Purchase Contribution}_{j} = \frac{\text{Vendor Purchase Total}_{j}}{\sum \text{Total Purchase Value}} \times 100\%$$
- **Revenue Growth %**:
  $$\text{Revenue Growth}_{t} = \frac{\text{Revenue}_{t} - \text{Revenue}_{t-1}}{\text{Revenue}_{t-1}} \times 100\% \quad (\text{replaced with 0 if } \text{Revenue}_{t-1} = 0)$$
