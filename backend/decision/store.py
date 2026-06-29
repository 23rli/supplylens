"""Decision orchestration: pull risk row + sisters, rank actions, today briefing."""
from db import fetch_all, fetch_one
from decision.engine import rank_actions, simulate, dollars_at_risk


def _row(sku, site):
    return fetch_one("SELECT * FROM sku_risk_summary WHERE sku_id=? AND site_id=?", (sku, site))


def _sisters(sku, site):
    return fetch_all("SELECT site_id, buffer_days FROM sku_risk_summary WHERE sku_id=? AND site_id<>?", (sku, site))


def explain(sku, site) -> dict:
    row = _row(sku, site)
    if not row:
        return {}
    return {"sku": sku, "site": site, "risk": row["risk_level"], "buffer_days": row["buffer_days"],
            "dollars_at_risk": dollars_at_risk(row),
            "actions": rank_actions(row, _sisters(sku, site)),
            "simulations": [simulate(row, m, _sisters(sku, site)) for m in ("no_action", "cheapest", "worst_case")]}


def today() -> dict:
    rows = fetch_all("SELECT * FROM sku_risk_summary ORDER BY buffer_days ASC")
    crit = [r for r in rows if r["risk_level"] == "CRITICAL"]
    high = [r for r in rows if r["risk_level"] == "HIGH"]
    at_risk = round(sum(dollars_at_risk(r) for r in rows), 2)
    cards = [{"sku_id": r["sku_id"], "sku_name": r["sku_name"], "site_id": r["site_id"],
              "buffer_days": r["buffer_days"], "dollars_at_risk": dollars_at_risk(r)} for r in crit[:3]]
    return {"critical": len(crit), "high": len(high), "dollars_at_risk": at_risk, "cards": cards}
