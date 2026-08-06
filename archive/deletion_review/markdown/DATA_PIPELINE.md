# Data Pipeline Documentation

1. Odoo ORM Transaction Ingestion -> `sale_order` & `sale_order_line`
2. ETL Extract & Transform -> `mart.fact_sales`
3. Rolling Horizon Benchmark -> `mart.fact_forecast_model_comparison`
4. Champion Selection -> `mart.fact_forecast_monthly`