from fastapi import APIRouter, Query
from database import get_risk_summary, get_top_risks, get_risk_counts_by_site
from typing import Optional

router = APIRouter()

@router.get("/risk-summary")
def risk_summary(
    site: Optional[str] = Query(None, description="Filter by site: BOSTON, CHICAGO, SEATTLE"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level: CRITICAL, HIGH, MEDIUM, LOW"),
    category: Optional[str] = Query(None, description="Filter by category: Critical, Standard, Consumable")
):
    """Returns all SKUs with risk scores, filtered by optional params."""
    return get_risk_summary(site=site, risk_level=risk_level, category=category)

@router.get("/top-risks")
def top_risks(limit: int = Query(10, ge=1, le=50)):
    """Returns the top N highest-risk SKUs across all sites."""
    return get_top_risks(limit=limit)

@router.get("/risk-by-site")
def risk_by_site():
    """Returns risk level counts grouped by site, for the heatmap."""
    return get_risk_counts_by_site()
