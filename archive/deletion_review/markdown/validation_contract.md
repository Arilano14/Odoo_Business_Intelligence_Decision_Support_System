# Implementation Validation Contract — Phase 11.2 Revision

**Date:** August 4, 2026  
**Status:** **CONTRACT SPECIFICATION APPROVED**  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. 6-Layer Validation Criteria

| Validation Layer | Required Evidence | Verification Method | Pass Criteria |
|---|---|---|---|
| **Layer 1: Source File** | Active addon file diffs & manifest sequence | File inspection | All files exist in `custom_addons/obidss_operational_bi/` |
| **Layer 2: Module Upgrade** | CLI upgrade logfile & module state | `odoo-bin` CLI test | Exit Code `0`; `state = 'installed'` |
| **Layer 3: ORM Records** | ORM record existence & XML ID resolution | XML-RPC / SQLAlchemy | Group IDs & Menu IDs resolve without error |
| **Layer 4: RPC Calls** | RPC window actions & view resolution | XML-RPC `search_read` | Zero RPC server tracebacks |
| **Layer 5: Browser UI** | Refreshed launcher & dashboard sidebar | Web client test | Clean app launcher; OBIDSS sidebar active; 0 critical JS errors |
| **Layer 6: Data Reconciliation**| Dashboard values vs PostgreSQL SQL queries | SQL truth comparison | SO Count: **740**; PO Count: **251**; Sales: **Rp 17.55B**; Purchase: **Rp 30.08B** |
