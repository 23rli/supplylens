"""Tests for the hedging engine (run: python -m pytest)."""
from hedging.engine import OilPlan, ScenarioParams, plan_oil, plan_all


def _oil():
    return OilPlan(oil_id="OIL_1", demand_mt=[100]*12,
                   forecast_price=[900]*12, spot_price=[1000]*12)


def test_saving_when_forecast_below_spot():
    r = plan_oil(_oil(), ScenarioParams())
    assert r.amount_saved > 0
    assert r.spot_only_cost == 100*12*1000


def test_full_coverage_meets_minimums():
    r = plan_oil(_oil(), ScenarioParams(s1_pct=0.75, s2_pct=0.25))
    assert r.coverage_ok
    assert abs(r.coverage_by_quarter[-1] - 1.0) < 1e-6


def test_saved_per_ton():
    r = plan_oil(_oil(), ScenarioParams(inventory_cost_per_mt=0))
    assert r.saved_per_ton == 100  # 1000 spot - 900 hedged


def test_plan_all_aggregates():
    out = plan_all([_oil(), _oil()], ScenarioParams())
    assert out["total_mt"] == 2400
    assert out["amount_saved"] > 0
