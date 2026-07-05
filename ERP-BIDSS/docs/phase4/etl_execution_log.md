# ETL Execution Log

*Log ini akan diisi secara otomatis oleh logger.py setelah pipeline dijalankan.*

Refer to: `backend/etl_execution.log` untuk raw system logs.

## Format Log
```
[TIMESTAMP] - INFO - START OBIDSS_ETL_PIPELINE
[TIMESTAMP] - INFO - TABLE: dim_product | Extracted: N | Transformed: N | Loaded: N | Failed: 0
[TIMESTAMP] - INFO - TABLE: fact_sales | Extracted: N | Transformed: N | Loaded: N | Failed: 0
[TIMESTAMP] - INFO - END OBIDSS_ETL_PIPELINE | Duration: X.XXs
```
