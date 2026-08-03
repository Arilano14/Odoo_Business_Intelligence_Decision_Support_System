# IMPLEMENTATION PLAN V2 — PHASE 11.0
## Odoo Dashboard Recovery, Dataset Quality Audit, and Cross-System Integration Assurance

**Date:** August 3, 2026  
**Status Mode:** **STAGE 1 — READ-ONLY PLANNING MODE (REVISED)**  
**Project:** Odoo Business Intelligence Decision Support System (OBIDSS)  
**Company:** PT Prima Alat Nusantara (Company ID: 2)  
**Target Period:** Fiscal Year 2026 (Jan 1, 2026 – Dec 31, 2026)

---

> [!IMPORTANT]
> **STAGE 1 CONTROL NOTICE**: Dokumen ini adalah revisi rencana implementasi read-only. Tidak ada perubahan kode, perbaikan module, penghapusan record, atau penulisan data ke Odoo/PostgreSQL/Power BI yang dieksekusi sebelum persetujuan eksplisit user (`APPROVE PHASE 11.0 IMPLEMENTATION V2`).

---

# 1. Root Cause Status

```text
LEADING ROOT-CAUSE HYPOTHESIS — NOT YET PROVEN
```

### Direct Empirical Audit Findings:
1. **Confirmed Fact 1**: `spreadsheet.dashboard` records IDs 1, 2, 3, 4 exist in database `Business_Intelegent_Project_v2`. Record ID 8 does NOT exist.
2. **Confirmed Fact 2**: Official sample JSON files exist on disk in `odoo/addons/` (sizes 21 KB to 78 KB).
3. **Confirmed Fact 3**: `ir_attachment` records exist for IDs 1, 2, 3, 4 with linked SHA1 checksums.
4. **Inference**: In Odoo 18, `spreadsheet_data` is a computed text field from `spreadsheet_binary_data` attachment and sample JSON files. When ORM evaluation or data model filters fail during QWeb rendering, `spreadsheet_data` computes to empty string `""` triggering Python `json.loads` `JSONDecodeError`.
5. **Unverified Assumption**: That running `-u` directly on the primary DB will resolve the issue without side effects.
6. **Required Proof**: Successful isolated rehearsal on a clone database (`Business_Intelegent_Project_v2_clone`) with 0 RPC errors in browser.

---

# 2. Dashboard Identity Reconciliation

📄 **Full Report**: [docs/phase11_0/dashboard_identity_reconciliation.md](file:///c:/Users/Arilano/Downloads/Project%20ARICE/Project%20Odoo/docs/phase11_0/dashboard_identity_reconciliation.md)

- **ID 8**: Non-existent artifact from pre-reset database build.
- **IDs 1, 2, 3, 4**: Canonical active dashboard records in `Business_Intelegent_Project_v2`.

---

# 3. Storage Audit & Module Data Loading Analysis

📄 **Full Reports**: 
- [docs/phase11_0/module_data_loading_analysis.md](file:///c:/Users/Arilano/Downloads/Project%20ARICE/Project%20Odoo/docs/phase11_0/module_data_loading_analysis.md)
- [docs/phase11_0/dashboard_storage_audit.md](file:///c:/Users/Arilano/Downloads/Project%20ARICE/Project%20Odoo/docs/phase11_0/dashboard_storage_audit.md)

All 4 records have `noupdate = False` in `ir_model_data` and linked `ir_attachment` binaries.

---

# 4. Clone-First Rehearsal Strategy

📄 **Full Protocol**: [docs/phase11_0/clone_rehearsal_plan.md](file:///c:/Users/Arilano/Downloads/Project%20ARICE/Project%20Odoo/docs/phase11_0/clone_rehearsal_plan.md)

### Rehearsal Command Template (Targeting Clone Database Only):
```powershell
& "C:\Program Files\Odoo 18.0.20241229\python\python.exe" "C:\Program Files\Odoo 18.0.20241229\server\odoo-bin" `
  -c "c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo.conf" `
  -d "Business_Intelegent_Project_v2_clone" `
  -u "spreadsheet_dashboard_sale,spreadsheet_dashboard_account,spreadsheet_dashboard_stock_account" `
  --stop-after-init `
  --no-http `
  --logfile "c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\docs\phase11_0\clone_upgrade.log"
```

---

# 5. Dashboard Repair Decision Tree

📄 **Full Specification**: [docs/phase11_0/dashboard_repair_decision.md](file:///c:/Users/Arilano/Downloads/Project%20ARICE/Project%20Odoo/docs/phase11_0/dashboard_repair_decision.md)

- **Case A**: Module update on clone succeeds -> Proceed to primary DB.
- **Case B**: Module update runs but data empty -> Fallback to ORM binary attachment restoration script.
- **Case C**: Overwrites custom records -> Restore clone filestore & DB.
- **Case D**: Creates duplicate IDs -> Reconcile XML IDs before cleanup.
- **Case E**: Broken model references -> Resolve missing module dependencies.
- **Case F**: Repair fails -> Rollback and mark BLOCKED.

---

# 6. Correct KPI Terminology & Power BI Protocol

📄 **Full Specifications**:
- [docs/phase11_0/dashboard_alignment_specification.md](file:///c:/Users/Arilano/Downloads/Project%20ARICE/Project%20Odoo/docs/phase11_0/dashboard_alignment_specification.md)
- [docs/phase11_0/powerbi_validation_protocol.md](file:///c:/Users/Arilano/Downloads/Project%20ARICE/Project%20Odoo/docs/phase11_0/powerbi_validation_protocol.md)

- **Confirmed Sales Value**: `sale_order.amount_total` (`state='sale'`, FY 2026, Company 2) = Rp 1,572,400,000 (NOT Recognized Revenue).
- **Recognized Revenue**: `account_move.amount_total` (`move_type='out_invoice'`, `state='posted'`) = **NOT AVAILABLE IN CURRENT MVP**.
- **Confirmed Purchase Value**: `purchase_order.amount_total` (`state='purchase'`) = Rp 1,120,800,000.
- **Power BI Status**: **PENDING MANUAL VALIDATION**.

---

# 7. Custom OBIDSS Operational Dashboard Build Plan

📄 **Full Specification**: [docs/phase11_0/odoo_dashboard_build_specification.md](file:///c:/Users/Arilano/Downloads/Project%20ARICE/Project%20Odoo/docs/phase11_0/odoo_dashboard_build_specification.md)

1. OBIDSS Executive Operations
2. OBIDSS Sales Operations
3. OBIDSS Purchase Operations (Resolves missing standard Purchase dashboard)
4. OBIDSS Inventory Operations

---

# 8. Revised 17-Step Implementation Sequence

1. Reconcile dashboard IDs and evidence (`dashboard_identity_reconciliation.md`).
2. Inspect source code, manifests, XML data, and storage (`module_data_loading_analysis.md`, `dashboard_storage_audit.md`).
3. Create verified backup plan (`safety_baseline.md`).
4. Create clone rehearsal plan (`clone_rehearsal_plan.md`).
5. Test module update on clone DB (`Business_Intelegent_Project_v2_clone`).
6. Select repair path based on evidence (`dashboard_repair_decision.md`).
7. Validate all standard dashboards on clone.
8. Design custom OBIDSS operational dashboards (`odoo_dashboard_build_specification.md`).
9. Audit dataset quality and scenario realism (`dataset_quality_test_specification.md`).
10. Prepare cleanup manifest (`cleanup_manifest.csv`).
11. Dry-run cleanup on clone DB.
12. Run Odoo deep health tests on clone.
13. Run Phase 10 validation suite on clone (15/15 PASS).
14. Reconcile Odoo and mart schema.
15. Prepare Power BI validation protocol (`powerbi_validation_protocol.md`).
16. Produce Phase 11.0 completion documentation.
17. Stop and request Stage 2 approval.

---

# 9. Approval Checkpoint

```text
STAGE 1 REVISION COMPLETE — NO WRITES PERFORMED

The revised plan is ready for review.

To authorize execution (Stage 2), please provide explicit approval:

APPROVE PHASE 11.0 IMPLEMENTATION V2
```
