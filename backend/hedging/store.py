"""Hedging planner data + scenario orchestration for commodity procurement."""
import random
from datetime import date, timedelta
from hedging.engine import OilPlan, ScenarioParams, plan_all, plan_oil
from hedging.forecast import forecast_oil

random.seed(11)
COMMODITIES = ["STEEL", "ALUMINUM"]
_BASE = {"STEEL": 900, "ALUMINUM": 2400}
REALIZED_PREMIUM = 1.06  # delivery-month spot sits above the forward curve


def _history(commodity: str, days: int = 540) -> list[dict]:
    base = _BASE.get(commodity, 900)
    d0 = date.today() - timedelta(days=days)
    out = []
    for i in range(days):
        trend = base + i * (base * 0.0006)        # gentle upward drift
        season = base * 0.03 * random.uniform(0.9, 1.1) * (1 + 0.3 * ((i // 90) % 2))
        out.append({"date": d0 + timedelta(days=i), commodity: round(trend + season, 2)})
    return out


def price_forecast(commodity: str) -> list[dict]:
    return forecast_oil(_history(commodity), commodity, periods=365)


def _forward_curve(commodity: str) -> list[float]:
    """12-month forward price curve derived from the forecast (rising)."""
    fc = price_forecast(commodity)[:12]
    if len(fc) >= 12:
        return [round(m["avg"], 2) for m in fc]
    base = _BASE.get(commodity, 900)
    return [round(base * (1 + 0.015 * i), 2) for i in range(12)]


def _commodity_plans() -> list[OilPlan]:
    plans = []
    for c in COMMODITIES:
        base = _BASE.get(c, 900)
        demand = [round(base * 4 * random.uniform(0.85, 1.15), 1) for _ in range(12)]
        forward = _forward_curve(c)
        spot = [round(f * REALIZED_PREMIUM, 2) for f in forward]
        plans.append(OilPlan(oil_id=c, demand_mt=demand, forecast_price=forward, spot_price=spot))
    return plans


def run_scenario(s1=0.75, s2=0.25, inv_cost=0.01, start_inv=0.0) -> dict:
    p = ScenarioParams(s1_pct=s1, s2_pct=s2, inventory_cost_per_mt=inv_cost, starting_inventory=start_inv)
    plans = _commodity_plans()
    summary = plan_all(plans, p)
    return {
        "amount_saved": summary["amount_saved"], "saved_per_ton": summary["saved_per_ton"],
        "hedged_total": summary["hedged_total"], "spot_total": summary["spot_total"],
        "total_mt": summary["total_mt"], "all_coverage_ok": summary["all_coverage_ok"],
        "oils": [{"oil_id": r.oil_id, "total_mt": r.total_mt, "hedged_cost": r.hedged_cost,
                  "spot_only_cost": r.spot_only_cost, "avg_hedged_price": r.avg_hedged_price,
                  "avg_spot_price": r.avg_spot_price, "amount_saved": r.amount_saved,
                  "coverage_by_quarter": r.coverage_by_quarter, "min_required": r.min_required,
                  "coverage_ok": r.coverage_ok, "monthly": r.monthly} for r in
                 [plan_oil(o, p) for o in plans]],
    }
