# Standard Dashboard Handling Policy — Phase 11.2 Revision

**Date:** August 4, 2026  
**Status:** **POLICY SPECIFICATION APPROVED**  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. Non-Negotiable Standard Dashboard Rules

```text
KEEP STANDARD RECORDS
DO NOT MODIFY CORE JSON
DO NOT DELETE
DO NOT USE AS FINAL PORTFOLIO DASHBOARDS
HIDE FROM PORTFOLIO REVIEWER AFTER CUSTOM DASHBOARDS PASS
KEEP VISIBLE TO ADMIN AS TECHNICAL BASELINE
```

---

## 2. Technical Control Protocol

1. **Core Immutability**: Standard dashboard records (IDs 1, 2, 3, 4) in `spreadsheet.dashboard` and their core JSON files in `C:\Program Files\Odoo 18.0.20241229\server\odoo\addons\` will **NEVER** be deleted, edited, or modified directly.
2. **Access Control Hiding**: Standard sample dashboards will be assigned to a restricted technical baseline group (`base.group_system`) so that target operational users and portfolio reviewers do not see sample mock data ("GlideSync Mouse").
3. **Admin Retention**: Administrators retain access to standard sample dashboards for Odoo platform reference.
