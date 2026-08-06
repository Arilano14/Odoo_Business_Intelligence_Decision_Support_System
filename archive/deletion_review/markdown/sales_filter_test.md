# Sales Pilot Filter Test Log
## GATE 2E.6 — Dynamic Filter Verification

| Filter Applied | Confirmed Revenue (IDR) | Confirmed SO Count | AOV (IDR) | Filter Behavior |
|----------------|------------------------:|-------------------:|----------:|-----------------|
| **Baseline (FY 2026)** | 17,552,025,691.43 | 677 | 25,926,182.71 | Full Year Baseline |
| **January 2026** | 1,659,770,035.08 | 56 | 29,638,750.63 | Period Filter Active |
| **March 2026** | 990,921,358.92 | 46 | 21,541,768.67 | Period Filter Active |
| **December 2026** | 1,295,943,864.37 | 59 | 21,965,150.24 | Period Filter Active |
| **Top Customer (ID 67)** | 1,234,689,531.29 | 41 | 30,114,378.81 | Relation Filter Active |
| **Top Category (ID 19)** | 10,719,234,354.34 | 310 | N/A | Relation Filter Active |

**Result:** Filter inputs dynamically recalculate all metric values. No stale static numbers remain.
