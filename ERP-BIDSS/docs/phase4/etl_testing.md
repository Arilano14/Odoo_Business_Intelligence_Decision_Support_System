# ETL Testing

## Test Cases

| Test | Scope | Expected Result | Status |
| :--- | :--- | :--- | :--- |
| TC-01 | Database Connection | Source & Target connected successfully | Pending |
| TC-02 | Extract sale_order | DataFrame not empty, columns match | Pending |
| TC-03 | Extract purchase_order | DataFrame not empty, columns match | Pending |
| TC-04 | Extract stock_move | DataFrame not empty, columns match | Pending |
| TC-05 | Extract account_move | DataFrame not empty, columns match | Pending |
| TC-06 | Transform fact_sales | Revenue calculated correctly | Pending |
| TC-07 | Transform dim_product | Join product_product + template + category | Pending |
| TC-08 | Business Rule: state filter | Only confirmed/done/posted records | Pending |
| TC-09 | Load dim tables | All 6 dimension tables loaded | Pending |
| TC-10 | Load fact tables | All 4 fact tables loaded | Pending |
| TC-11 | FK Integrity | All FK in fact reference valid dim keys | Pending |
| TC-12 | Pipeline end-to-end | Extract → Transform → Load without error | Pending |

## Success Criteria
- Extraction Success: 100%
- Transformation Success: 100%
- Loading Success: 100%
- Pipeline Success: 100%
