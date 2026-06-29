from fastapi import APIRouter
from database import get_dashboard_stats

router = APIRouter()

@router.get("/dashboard-stats")
def dashboard_stats():
    """Returns 4 headline KPIs for the dashboard KPIBar."""
    return get_dashboard_stats()
