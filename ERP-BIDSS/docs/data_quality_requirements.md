# Data Quality Requirements

## Dimensi Kualitas Data

| Dimensi | Target | Definisi |
| :--- | :--- | :--- |
| Completeness | > 95% | Persentase field wajib yang terisi |
| Validity | > 95% | Persentase nilai yang sesuai dengan tipe data dan business rule |
| Consistency | > 95% | Persentase data yang konsisten antar tabel (FK valid) |
| Uniqueness | 100% | Tidak ada duplikasi primary key |

## Formula DQS
```
DQS = (Completeness + Validity + Consistency + Uniqueness) / 4
```

**Target:** DQS > 90%

## Validasi Khusus
| Check | Table | Rule |
| :--- | :--- | :--- |
| FK Integrity | sale_order_line.order_id | Harus ada di sale_order.id |
| FK Integrity | sale_order.partner_id | Harus ada di res_partner.id |
| FK Integrity | stock_move.product_id | Harus ada di product_product.id |
| Value Range | sale_order_line.price_unit | > 0 |
| Value Range | stock_move.product_uom_qty | > 0 |
| State Valid | sale_order.state | IN ('draft', 'sent', 'sale', 'cancel') |
