# Phase 8 Cleanup Candidate Manifest

The following records are identified as synthetic portfolio data and are candidates for deletion.

## 1. Customers (300)
- ID: 1353, Name: Agus Setiawan 25, Ref: BIDSS-CUST-92
- ID: 1341, Name: Agus Setiawan 38, Ref: BIDSS-CUST-80
- ID: 1427, Name: Agus Setiawan 39, Ref: BIDSS-CUST-166
- ID: 1380, Name: Agus Setiawan 40, Ref: BIDSS-CUST-119
- ID: 1297, Name: Agus Setiawan 40, Ref: BIDSS-CUST-36
- ... and 295 more

## 2. Suppliers (300)
- ID: 1706, Name: Budi Engineering 10, Ref: BIDSS-VEND-145
- ID: 1686, Name: Budi Engineering 10, Ref: BIDSS-VEND-125
- ID: 1817, Name: Budi Engineering 27, Ref: BIDSS-VEND-256
- ID: 1618, Name: Budi Engineering 34, Ref: BIDSS-VEND-57
- ID: 1679, Name: Budi Engineering 50, Ref: BIDSS-VEND-118
- ... and 295 more

## 3. Products (50)
- ID: 1139, Name: Hitachi Mining Equipment - 452, SKU: BIDSS-HE-1183
- ID: 1119, Name: JCB PC200 Excavator - 842, SKU: BIDSS-HE-1196
- ID: 1159, Name: Komatsu Wheel Loader - 506, SKU: BIDSS-HE-1449
- ID: 1116, Name: Hitachi Forklift - 404, SKU: BIDSS-HE-1532
- ID: 1114, Name: Volvo Bulldozer - 402, SKU: BIDSS-HE-1672
- ... and 45 more

## 4. Sales Orders (936)
- ID: 1606, Ref: S01606, Date: 2026-07-13 12:23:45, State: sale
- ID: 1605, Ref: S01605, Date: 2026-07-13 12:23:45, State: sale
- ID: 1604, Ref: S01604, Date: 2026-07-13 12:23:44, State: sale
- ID: 1603, Ref: S01603, Date: 2026-07-13 12:23:44, State: sale
- ID: 1602, Ref: S01602, Date: 2026-07-13 12:23:44, State: sale
- ... and 931 more

## 5. Purchase Orders (1036)
- ID: 1704, Ref: P01704, Date: 2026-07-13 12:23:32, State: purchase
- ID: 1703, Ref: P01703, Date: 2026-07-11 12:23:32, State: purchase
- ID: 1702, Ref: P01702, Date: 2026-07-01 12:23:32, State: purchase
- ID: 1701, Ref: P01701, Date: 2026-07-12 12:23:32, State: purchase
- ID: 1700, Ref: P01700, Date: 2026-06-23 12:23:32, State: purchase
- ... and 1031 more

## 6. Stock Pickings (1684)
- ID: 1216, Ref: WH/OUT/00614, Date: 2026-07-09 00:04:34, State: assigned
- ID: 1215, Ref: WH/OUT/00613, Date: 2026-07-09 00:04:33, State: assigned
- ID: 1214, Ref: WH/OUT/00612, Date: 2026-07-09 00:04:32, State: assigned
- ID: 1213, Ref: WH/OUT/00611, Date: 2026-07-09 00:04:30, State: assigned
- ID: 1212, Ref: WH/OUT/00610, Date: 2026-07-09 00:04:28, State: assigned
- ... and 1679 more

## 7. Account Moves (Invoices/Bills) (1663)
- ID: 11849, Ref: INV/2026/00003, Date: 2026-07-13, State: posted
- ID: 11846, Ref: BILL/2026/07/0004, Date: 2026-07-13, State: posted
- ID: 11844, Ref: BILL/2026/07/0003, Date: 2026-07-13, State: posted
- ID: 11842, Ref: BILL/2026/07/0002, Date: 2026-07-13, State: posted
- ID: 11841, Ref: BILL/2026/07/0001, Date: 2026-07-13, State: posted
- ... and 1658 more

## 8. Dashboard Issues
- Found 1 dangling reference in `ir_act_client` (ID: 348, tag: action_spreadsheet_dashboard). Needs manual review if it explicitly opens dashboard 11.
- Sale order 19 missing references need to be cleaned up in `ir_filters` or UI if any exist.
