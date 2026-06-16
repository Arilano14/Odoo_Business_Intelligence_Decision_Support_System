import pandas as pd
from sqlalchemy.orm import Session
from app.models.schema import FactSales, FactInventory, FactCRM, FactPurchase, FactFinance

def calculate_revenue_growth(db: Session):
    # Simplified mock calculation: Current Month vs Previous Month
    # In a real app, you'd aggregate fact_sales grouping by month.
    # We will return dummy aggregated logic for the MVP
    return {
        "value": 15.2, # % growth
        "current_revenue": 125000,
        "previous_revenue": 108500
    }

def calculate_inventory_turnover(db: Session):
    # COGS / Average Inventory
    return {
        "value": 4.5, # times per year
        "cogs": 450000,
        "avg_inventory": 100000
    }

def calculate_conversion_rate(db: Session):
    # Won Leads / Total Leads
    return {
        "value": 24.5, # %
        "won_leads": 120,
        "total_leads": 490
    }

def calculate_average_lead_time(db: Session):
    # Average days between PO date and receipt
    return {
        "value": 14.2, # days
    }

def calculate_cash_flow_health(db: Session):
    # Cash In vs Cash Out
    return {
        "value": 1.2, # Ratio
        "cash_in": 150000,
        "cash_out": 125000
    }

def calculate_enterprise_intelligence_score(db: Session):
    """
    30% Financial Health
    25% Sales Performance
    20% Inventory Efficiency
    15% Customer Performance
    10% Operational Stability
    """
    score = (
        (85 * 0.30) + # Mock Financial Health
        (90 * 0.25) + # Mock Sales
        (75 * 0.20) + # Mock Inventory
        (88 * 0.15) + # Mock Customer
        (92 * 0.10)   # Mock Operations
    )
    return round(score, 1)

def get_all_kpis(db: Session):
    return {
        "revenue_growth": calculate_revenue_growth(db),
        "inventory_turnover": calculate_inventory_turnover(db),
        "conversion_rate": calculate_conversion_rate(db),
        "avg_lead_time": calculate_average_lead_time(db),
        "cash_flow_health": calculate_cash_flow_health(db),
        "enterprise_score": calculate_enterprise_intelligence_score(db)
    }
