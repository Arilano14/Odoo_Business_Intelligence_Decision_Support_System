def generate_recommendations(kpis: dict):
    recommendations = []
    
    # Rule 1: Inventory Turnover
    if kpis['inventory_turnover']['value'] < 5.0:
        recommendations.append({
            "type": "Operations",
            "priority": "High",
            "message": "Inventory Turnover is low (< 5.0). Recommend: Increase procurement frequency to reduce average stock holding."
        })
        
    # Rule 2: Conversion Rate
    if kpis['conversion_rate']['value'] < 30.0:
        recommendations.append({
            "type": "Sales & CRM",
            "priority": "Medium",
            "message": "Lead Conversion is declining. Recommend: Review sales funnel process and re-evaluate lead quality."
        })
        
    # Rule 3: Cash Flow
    if kpis['cash_flow_health']['value'] < 1.0:
        recommendations.append({
            "type": "Finance",
            "priority": "Critical",
            "message": "Cash Flow Health is negative (Cash Out > Cash In). Recommend: Reduce operating expenses or delay non-urgent payables."
        })
        
    # Rule 4: Enterprise Score
    if kpis['enterprise_score'] < 80:
        recommendations.append({
            "type": "Executive",
            "priority": "High",
            "message": "Enterprise Intelligence Score is below threshold. Review all sub-metrics."
        })
        
    if not recommendations:
        recommendations.append({
            "type": "Executive",
            "priority": "Low",
            "message": "All KPIs are within healthy thresholds. Maintain current operations."
        })
        
    return recommendations
