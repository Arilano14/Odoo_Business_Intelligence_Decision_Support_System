# Data Loading Strategy

- **Dimension Tables**: Upsert (SCD Type 1 for MVP)
- **Fact Tables**: Truncate and Load (Replace) for simplicity in MVP, scaling to Incremental Load in production.
