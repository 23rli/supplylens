"""Hedging planner data + scenario orchestration. Synthetic in-memory plan for demo."""
import random
from datetime import date, timedelta
from hedging.engine import OilPlan, ScenarioParams, plan_all, plan_oil
from hedging.forecast import forecast_oil

random.seed(11)
OILS = ["OIL_1", "OIL_2"]


def _history(oil: str, days: int = 540) -> list[dict]:
    base = 900 if oil == "OIL_1" else 720
    d0 = date.today() - timedelta(days=days)
    out = []
    for i in range(days):
        trend = base + i * 0.4
        season = 40 * random.uniform(0.9, 1.1) * (1 + 0.3 * ((i // 90) % 2))
        out.append({"date": d0 + timedelta(days=i), oil: round(trend + season, 2)})
    return out


def price_forecast(oil: str) -> list[dict]:
    return forecast_oil(_history(oil), oil, periods=365)


def _demo_oils() -> list[OilPlan]:
    oils = []
    for oid in OILS:
        base = 8000 if oid == "OIL_1" else 5000
        demand = [round(base * random.uniform(0.85, 1.15), 1) for _ in range(12)]
        fc = [round(900 + 60 * i + random.uniform(-30, 30), 2) for i in range(12)]
        spot = [round(f * random.uniform(1.04, 1.18), 2) for f in fc]
        oils.append(OilPlan(oil_id=oid, demand_mt=demand, forecast_price=fc, spot_price=spot))
    return oils


def run_scenario(s1=0.75, s2=0.25, inv_cost=0.01, start_inv=0.0) -> dict:
    p = ScenarioParams(s1_pct=s1, s2_pct=s2, inventory_cost_per_mt=inv_cost, starting_inventory=start_inv)
    oils = _demo_oils()
    summary = plan_all(oils, p)
    return {
        "amount_saved": summary["amount_saved"], "saved_per_ton": summary["saved_per_ton"],
        "hedged_total": summary["hedged_total"], "spot_total": summary["spot_total"],
        "total_mt": summary["total_mt"], "all_coverage_ok": summary["all_coverage_ok"],
        "oils": [{"oil_id": r.oil_id, "total_mt": r.total_mt, "hedged_cost": r.hedged_cost,
                  "spot_only_cost": r.spot_only_cost, "avg_hedged_price": r.avg_hedged_price,
                  "avg_spot_price": r.avg_spot_price, "amount_saved": r.amount_saved,
                  "coverage_by_quarter": r.coverage_by_quarter, "min_required": r.min_required,
                  "coverage_ok": r.coverage_ok, "monthly": r.monthly} for r in
                 [plan_oil(o, p) for o in oils]],
    }
