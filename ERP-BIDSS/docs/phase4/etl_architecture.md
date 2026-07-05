# ETL Architecture

- **Source System**: Odoo 18 (PostgreSQL) / Simulation Mock
- **ETL Engine**: Python (Pandas + SQLAlchemy)
- **Target System**: Analytics Mart (PostgreSQL schema `mart`)
- **Orchestration**: Python Scheduler / Cron
