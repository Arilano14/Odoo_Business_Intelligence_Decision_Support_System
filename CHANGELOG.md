# Changelog

All notable changes to the Odoo Business Intelligence & Decision Support System (OBIDSS) project will be documented in this file.

## [2.0.0] - 2026-08-06
### Added
- Phase 11.4 Synthetic Transaction Scenario V2 with 240 Verified Portfolio SKUs.
- 6-Model Rolling Horizon Benchmark Engine (Naive, MA3, SES, Croston, SBA, TSB).
- Restructured professional repository layout (`scripts/`, `docs/`, `audits/`, `dashboard_tools/`, `dashboard_assets/`).
- Automated security policy, CODEOWNERS, CITATION.cff, and repository governance workflow.

### Fixed
- Granular month formatting in Odoo 18 Spreadsheet pivot data (`01/2026` ... `12/2026`).
- Product-isolated rolling window forecast calculation with Zero-History Rule.
