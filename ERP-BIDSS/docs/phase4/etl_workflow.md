# ETL Workflow

## Alur Proses

```
1. Extract
   ├── Master Data (product, partner, warehouse, company)
   └── Transaction Data (sale_order, purchase_order, stock_move, account_move)
         ↓
2. Validate
   ├── Business Rules (state filter)
   ├── FK Integrity
   └── Data Type Check
         ↓
3. Clean
   ├── Remove Duplicates
   ├── Handle NULL (generate SKU, etc.)
   └── Standardize Format
         ↓
4. Transform
   ├── Join Tables (order + order_line + product + partner)
   ├── Generate Surrogate Keys
   ├── Build Dimension Tables
   └── Build Fact Tables
         ↓
5. Load
   ├── Dimension Tables → schema 'mart'
   └── Fact Tables → schema 'mart'
         ↓
6. Log
   └── Write execution metrics to etl_execution.log
```
