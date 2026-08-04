# Runtime Identity Audit Report — Phase 11.2 Stage 2C

**Date:** August 4, 2026  
**Status:** **FORENSIC AUDIT COMPLETED — ROOT CAUSES CONFIRMED**  
**Target Environment:** Primary Odoo Web Runtime (`http://localhost:8069`)

---

## 1. Runtime Comparison Matrix

| Component | Deployment CLI | Running Web Service | Match Status | Root Cause Impact |
|---|---|---|---|---|
| **Python Executable** | `C:\Program Files\Odoo 18.0.20241229\python\python.exe` | `C:\Program Files\Odoo 18.0.20241229\python\python.exe` | 🟢 **MATCH** | Normal Python runtime |
| **Odoo Executable** | `C:\Program Files\Odoo 18.0.20241229\server\odoo-bin` | `C:\Program Files\Odoo 18.0.20241229\server\odoo-bin` | 🟢 **MATCH** | Normal Odoo bin |
| **Config File** | `c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo.conf` | `c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo.conf` | 🟢 **MATCH** | Config matched |
| **Addon Path Loaded** | `odoo/addons/obidss_operational_bi` | `odoo/addons/obidss_operational_bi` | 🔴 **MISMATCH** | **ROOT CAUSE 2**: `odoo/addons` was missing `data/dashboard_groups.xml` |
| **Dashboard JSON Data** | Record Placeholders (IDs 5..10) | Record Placeholders (IDs 5..10) | 🔴 **MISMATCH** | **ROOT CAUSE 1**: Dashboard records had NO JSON attachment payload data |
