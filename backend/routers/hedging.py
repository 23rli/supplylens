from fastapi import APIRouter, Query
from hedging.store import run_scenario, price_forecast

router = APIRouter()

@router.get("/hedging/scenario")
def scenario(s1: float = Query(0.75), s2: float = Query(0.25),
             inv_cost: float = Query(0.01), start_inv: float = Query(0.0)):
    return run_scenario(s1=s1, s2=s2, inv_cost=inv_cost, start_inv=start_inv)

@router.get("/hedging/forecast")
def forecast(oil: str = Query("OIL_1")):
    return price_forecast(oil)
