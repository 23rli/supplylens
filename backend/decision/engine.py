"""
Decision engine: ranks fix actions for an at-risk SKU with cost/benefit/confidence.
Pure & deterministic — consumes plain dicts, no DB. Doubles as the AI fallback.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict

EXPEDITE_PREMIUM = 0.35   # +35% unit cost to air-freight
TRANSFER_COST_PER_UNIT = 0.50


@dataclass
class Action:
    type: str            # REBALANCE | EXPEDITE | SUBSTITUTE | DEFER
    label: str
    cost: float
    benefit: float       # $ stockout exposure avoided
    confidence: float    # 0..1
    detail: str
    recommended: bool = False


def dollars_at_risk(row: dict) -> float:
    """Exposure if the SKU stocks out: shortfall days × demand × unit cost."""
    buffer = row.get("buffer_days", 0) or 0
    if buffer >= 0:
        return 0.0
    demand = row.get("avg_daily_demand", 0) or 0
    cost = row.get("unit_cost", 0) or 0
    return round(abs(buffer) * demand * cost, 2)


def rank_actions(row: dict, sisters: list[dict] = None, supplier: dict = None) -> list[dict]:
    sisters = sisters or []
    demand = row.get("avg_daily_demand", 0) or 0
    cost = row.get("unit_cost", 0) or 0
    lead = row.get("lead_time_days", 0) or 0
    exposure = dollars_at_risk(row)
    qty = round(demand * lead)
    actions: list[Action] = []

    donor = max(sisters, key=lambda s: s.get("buffer_days", 0), default=None)
    if donor and donor.get("buffer_days", 0) > lead:
        actions.append(Action("REBALANCE", f"Rebalance {qty} units from {donor['site_id']}",
                              round(qty * TRANSFER_COST_PER_UNIT, 2), exposure,
                              0.9, f"{donor['site_id']} has {donor['buffer_days']}d buffer"))
    actions.append(Action("EXPEDITE", "Expedite from backup supplier",
                          round(qty * cost * EXPEDITE_PREMIUM, 2), exposure,
                          0.8, "Air-freight; arrives 1-3 days"))
    if row.get("category") != "Critical":
        actions.append(Action("SUBSTITUTE", "Substitute alternate SKU", 0.0, round(exposure * 0.7, 2),
                              0.55, "Confirm clinical acceptability"))
    actions.append(Action("DEFER", "Accept temporary shortage", 0.0, 0.0, 0.3,
                          "Only for non-critical items"))

    actions.sort(key=lambda a: a.benefit - a.cost, reverse=True)
    if actions:
        actions[0].recommended = True
    return [asdict(a) for a in actions]


def simulate(row: dict, mode: str, sisters=None, supplier=None) -> dict:
    if mode == "no_action":
        return {"mode": mode, "cost": dollars_at_risk(row), "summary": "Stockout exposure if unaddressed"}
    acts = rank_actions(row, sisters, supplier)
    a = min(acts, key=lambda x: x["cost"]) if mode == "cheapest" else max(acts, key=lambda x: x["cost"])
    return {"mode": mode, "cost": a["cost"], "summary": a["label"]}
