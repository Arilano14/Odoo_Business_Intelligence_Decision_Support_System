# Dataset Quality & Scenario Realism Test Specification — Phase 11.0

**Date:** August 3, 2026  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. Test Categories & Thresholds

| Category | Test Description | Target Metric / Threshold | Expected Status |
|---|---|---|---|
| **Structure** | Critical Completeness | 100% (0 NULLs in Partner, Product, Date, Quantity, Price) | **PASS** |
| **Structure** | Business-Key Uniqueness | 0 Duplicates (720 SOs, 240 POs) | **PASS** |
| **Structure** | Referential Integrity | 0 Orphan Foreign Keys in `mart` schema | **PASS** |
| **Distribution** | Monthly Demand Non-Uniformity | Monthly sales volume variance $> 0$ | **PASS** |
| **Distribution** | Product & Customer Concentration | Top customer revenue contribution $< 30\%$ | **PASS** |
| **Scenario Realism** | March Disruption Impact | Sales volume drop in March 2026 | **PASS** |
| **Scenario Realism** | April-May Procurement Response | PO volume spike in April-May 2026 | **PASS** |
| **Scenario Realism** | June-Sept Recovery & Oct-Dec Stabilization | Sales recovery in Q3-Q4 2026 | **PASS** |
| **Operational Coherence** | Stock Balance Identity | $\text{Opening} + \text{In} - \text{Out} - \text{Scrap} = \text{Closing}$ | **PASS** |
