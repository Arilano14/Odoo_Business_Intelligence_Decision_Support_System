from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.analytics.kpi import get_all_kpis
from app.analytics.decision import generate_recommendations

router = APIRouter()

@router.get("/dashboard/overview")
def get_dashboard_overview(db: Session = Depends(get_db)):
    """Returns the main executive overview KPIs and Score."""
    try:
        kpis = get_all_kpis(db)
        return {
            "kpis": kpis,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard/insights")
def get_executive_insights(db: Session = Depends(get_db)):
    """Returns AI-rule based insights and recommendations."""
    try:
        kpis = get_all_kpis(db)
        recommendations = generate_recommendations(kpis)
        return {
            "insights": recommendations,
            "enterprise_score": kpis["enterprise_score"],
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
