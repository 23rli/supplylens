from inventory.demand_forecast import forecast_demand


def test_seasonal_shape():
    r = forecast_demand({"part_number": "SKU-0001", "forecast": 5200, "on_hand": 400})
    assert r["avg_weekly"] == 100.0
    assert len(r["weeks"]) == 52
    assert r["peak_pct"] >= 0


def test_zero_demand_safe():
    r = forecast_demand({"part_number": "X", "forecast": 0, "on_hand": 0})
    assert r["avg_weekly"] == 0.0
