# User Group & Dedicated Reviewer Strategy — Phase 11.2 Revision

**Date:** August 4, 2026  
**Status:** **SECURITY STRATEGY APPROVED**  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. Dedicated Portfolio Reviewer User Strategy

To prevent accidental modification of global standard module menus, access visibility is controlled primarily via a **Dedicated User Role Architecture**:

1. **Dedicated User Creation**: `OBIDSS Portfolio Reviewer` (`login: reviewer`, `company_id = 2`).
2. **Assigned Security Groups**:
   - `base.group_user` (Internal User)
   - `obidss_operational_bi.group_obidss_user`
   - `obidss_operational_bi.group_obidss_reviewer`
   - `sales_team.group_sale_salesman` (Sales Read)
   - `purchase.group_purchase_user` (Purchase Read)
   - `stock.group_stock_user` (Inventory Read)
3. **Excluded Groups**:
   - `mass_mailing.group_mass_mailing_user` (Email Marketing Excluded)
   - `survey.group_survey_user` (Surveys Excluded)
   - `hr.group_hr_user` (Employees Excluded)
   - `base.group_system` (Settings Excluded)

---

## 2. Menu Access Strategy Matrix

| Launcher Menu Name | Admin User | Portfolio Reviewer | Operational User | Access Enforcement Method | Global System Impact |
|---|---|---|---|---|---|
| **Dashboards** | 🟢 Visible | 🟢 Visible | 🟢 Visible | Core Module Access | None |
| **Sales** | 🟢 Visible | 🟢 Visible | 🟢 Visible | Standard Sales Group | None |
| **Purchase** | 🟢 Visible | 🟢 Visible | 🟢 Visible | Standard Purchase Group | None |
| **Inventory** | 🟢 Visible | 🟢 Visible | 🟢 Visible | Standard Stock Group | None |
| **Invoicing** | 🟢 Visible | 🟡 Role-based | 🔴 Hidden | Group Access Rule | Safe |
| **Contacts** | 🟢 Visible | 🟢 Visible | 🔴 Hidden | Partner Manager Group | Safe |
| **Discuss** | 🟢 Visible | 🔴 Hidden | 🔴 Hidden | Group Exclusion | Target User Only |
| **Email Marketing** | 🟢 Visible | 🔴 Hidden | 🔴 Hidden | Group Exclusion | Target User Only |
| **Surveys** | 🟢 Visible | 🔴 Hidden | 🔴 Hidden | Group Exclusion | Target User Only |
| **Employees** | 🟢 Visible | 🔴 Hidden | 🔴 Hidden | Group Exclusion | Target User Only |
| **Apps & Settings** | 🟢 Visible | 🔴 Hidden | 🔴 Hidden | `base.group_system` | Safe |
