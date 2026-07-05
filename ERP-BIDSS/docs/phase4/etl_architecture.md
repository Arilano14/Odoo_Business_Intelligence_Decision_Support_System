# ETL Architecture

## Overview
```
Odoo 18 PostgreSQL ──→ Python ETL ──→ Analytics Mart (PostgreSQL schema 'mart') ──→ Power BI
```

## Components
| Component | Technology | Role |
| :--- | :--- | :--- |
| Source System | Odoo 18 PostgreSQL | Operational database (OLTP) |
| ETL Engine | Python (Pandas + SQLAlchemy) | Extract, Transform, Load |
| Target System | PostgreSQL schema 'mart' | Analytics Mart (OLAP - Star Schema) |
| Presentation | Microsoft Power BI (Import Mode) | Dashboard & Visualization |

## ETL Pattern
- **Extraction:** SQL query per table via SQLAlchemy
- **Transformation:** Pandas DataFrame operations (join, filter, aggregate, surrogate key)
- **Loading:** pandas.DataFrame.to_sql() with if_exists='replace' (full refresh for MVP)
- **Orchestration:** Python script (pipeline.py), no Airflow/Kafka
- **Logging:** Python logging module → etl_execution.log
