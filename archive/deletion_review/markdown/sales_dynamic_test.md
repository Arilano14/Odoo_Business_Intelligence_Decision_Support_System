# Sales Pilot Dynamic Source-Change Test Log
## GATE 2E.6 — Source Change Validation

1. **Baseline State:** 677 Confirmed SOs, Rp 17,552,025,691.43 Total Revenue.
2. **Controlled Injection (Clone Only):** Inserted temporary SO (`SO-TEMP-TEST-001`, Amount: Rp 1,000,000.00).
3. **Observed Result:** Recalculated total dynamically changed to **678 SOs** (+1) and **Rp 17,553,025,691.43** (+Rp 1,000,000.00).
4. **Rollback Action:** Rollback executed; database returned to baseline state of 677 SOs / Rp 17,552,025,691.43.
5. **Status:** **PASS** — Dashboard metrics are proven 100% dynamic against underlying Odoo tables.
