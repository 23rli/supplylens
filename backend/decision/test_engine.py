from decision.engine import dollars_at_risk, rank_actions, simulate

ROW = {"sku_id": "SKU004", "site_id": "BOSTON", "category": "Critical",
       "avg_daily_demand": 28, "lead_time_days": 10, "unit_cost": 12.75, "buffer_days": -3}
SIS = [{"site_id": "CHICAGO", "buffer_days": 20}, {"site_id": "SEATTLE", "buffer_days": 2}]


def test_exposure_only_when_negative_buffer():
    assert dollars_at_risk(ROW) == round(3 * 28 * 12.75, 2)
    assert dollars_at_risk({**ROW, "buffer_days": 5}) == 0.0


def test_rebalance_from_best_sister_recommended():
    acts = rank_actions(ROW, SIS)
    assert acts[0]["type"] == "REBALANCE" and acts[0]["recommended"]
    assert "CHICAGO" in acts[0]["detail"]


def test_no_substitute_for_critical():
    assert not any(a["type"] == "SUBSTITUTE" for a in rank_actions(ROW, SIS))


def test_simulate_modes():
    assert simulate(ROW, "no_action")["cost"] > 0
    assert simulate(ROW, "cheapest", SIS)["cost"] <= simulate(ROW, "worst_case", SIS)["cost"]
