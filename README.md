# Odoo Business Intelligence & Decision Support System (OBIDSS)

[![Security Policy](https://img.shields.io/badge/security-policy-blue.svg)](SECURITY.md)
[![License Notice](https://img.shields.io/badge/notice-copyright-green.svg)](NOTICE)

Professional enterprise decision support system and statistical demand forecasting engine integrated with Odoo 18.0 ERP and PostgreSQL Data Mart.

## Architecture Overview
- **ERP Engine**: Odoo 18.0 (Port 8069 Main, Port 8070 Clone)
- **Data Mart Schema**: PostgreSQL `mart` (`fact_sales`, `fact_forecast_model_comparison`, `fact_forecast_monthly`)
- **Forecasting Models**: 6 Candidate Models (*Naive, MA3, SES, Croston, SBA, TSB*) with Syntetos-Boylan demand pattern classification.
- **Analytics Visualization**: Odoo Spreadsheet Dashboards & Power BI Desktop (`PowerBI/Odoo DSS_Arilano Excelovell Pinem_2304140070.pbix`).

## Portfolio Scope & Accuracy
- **Scope**: Exactly 240 Verified Portfolio SKUs (`PORTFOLIO_2026_*`).
- **Holdout Accuracy (FY 2026)**: **81.17%** (WAPE = **18.83%**).
- **Positive-Demand Accuracy**: **87.60%**.

## Governance & Security
- Canonical Repository: `https://github.com/Arilano14/Odoo_Business_Intelligence_Decision_Support_System.git`
- Maintainer: `@Arilano14`
