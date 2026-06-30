"""
Commodity Procurement & Hedging engine (REQUIREMENTS_SPEC Part A).

Pure & deterministic. The two strategies now genuinely differ by TIMING, so the
strategy split changes the blended price (and therefore the savings):

  * Strategy 1 - "Toll Gate" / front-loaded: locks coverage early, ~2 months
    before delivery, capturing lower forward prices on a rising market.
  * Strategy 2 - "Systematic": spreads buying evenly, paying the trailing average.

Spot is the delivery-month realised price. On a rising market, front-loading
beats systematic beats spot -- and pushing the slider toward S1 increases savings.
"""
from __future__ import annotations
from dataclasses import dataclass, field

MONTHS = 12
MIN_S1 = [0.15, 0.375, 0.60, 0.75]   # mandatory minimum coverage by quarter


@dataclass
class OilPlan:
    oil_id: str
    demand_mt: list[float]
    forecast_price: list[float]   # forward price curve per delivery month
    spot_price: list[float]       # delivery-month realised price


@dataclass
class ScenarioParams:
    s1_pct: float = 0.75
    s2_pct: float = 0.25
    inventory_cost_per_mt: float = 0.01
    starting_inventory: float = 0.0


@dataclass
class OilResult:
    oil_id: str
    total_mt: float
    hedged_cost: float
    spot_only_cost: float
    inventory_cost: float
    avg_hedged_price: float
    avg_spot_price: float
    amount_saved: float
    saved_per_ton: float
    coverage_by_quarter: list[float]
    min_required: list[float]
    coverage_ok: bool
    monthly: list[dict] = field(default_factory=list)


def _front_price(F, m):
    # Strategy 1 locks ~2 months earlier (lower on a rising curve).
    return F[max(0, m - 2)]


def _systematic_price(F, m):
    # Strategy 2 pays the trailing 3-month average.
    lo = max(0, m - 2)
    window = F[lo:m + 1]
    return sum(window) / len(window)


def plan_oil(oil: OilPlan, p: ScenarioParams) -> OilResult:
    total_mt = sum(oil.demand_mt)
    inv = p.starting_inventory
    hedged_cost = spot_cost = inv_cost = 0.0
    cumulative = 0.0
    coverage_q = [0.0, 0.0, 0.0, 0.0]
    monthly = []
    for m in range(MONTHS):
        need = max(0.0, oil.demand_mt[m] - (inv if m == 0 else 0))
        f1 = _front_price(oil.forecast_price, m)
        f2 = _systematic_price(oil.forecast_price, m)
        blended = p.s1_pct * f1 + p.s2_pct * f2
        hedged_cost += need * blended
        spot_cost += oil.demand_mt[m] * oil.spot_price[m]
        held = max(0.0, need - oil.demand_mt[m])
        inv_cost += held * p.inventory_cost_per_mt
        cumulative += need
        coverage_q[m // 3] = cumulative / total_mt if total_mt else 0
        monthly.append({"month": m + 1, "demand_mt": round(oil.demand_mt[m], 1),
                        "hedged_mt": round(need, 1), "hedged_price": round(blended, 2),
                        "spot_price": oil.spot_price[m]})
    hedged_total = hedged_cost + inv_cost
    saved = spot_cost - hedged_total
    ok = all(coverage_q[q] + 1e-9 >= MIN_S1[q] for q in range(4))
    return OilResult(
        oil_id=oil.oil_id, total_mt=round(total_mt, 1),
        hedged_cost=round(hedged_total, 2), spot_only_cost=round(spot_cost, 2),
        inventory_cost=round(inv_cost, 2),
        avg_hedged_price=round(hedged_cost / total_mt, 2) if total_mt else 0,
        avg_spot_price=round(spot_cost / total_mt, 2) if total_mt else 0,
        amount_saved=round(saved, 2), saved_per_ton=round(saved / total_mt, 2) if total_mt else 0,
        coverage_by_quarter=[round(c, 4) for c in coverage_q], min_required=MIN_S1,
        coverage_ok=ok, monthly=monthly)


def plan_all(oils: list[OilPlan], p: ScenarioParams) -> dict:
    results = [plan_oil(o, p) for o in oils]
    hedged = sum(r.hedged_cost for r in results)
    spot = sum(r.spot_only_cost for r in results)
    mt = sum(r.total_mt for r in results)
    return {"oils": results, "hedged_total": round(hedged, 2), "spot_total": round(spot, 2),
            "amount_saved": round(spot - hedged, 2),
            "saved_per_ton": round((spot - hedged) / mt, 2) if mt else 0,
            "total_mt": round(mt, 1), "all_coverage_ok": all(r.coverage_ok for r in results)}
