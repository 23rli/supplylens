"""Tests for the price forecasting engine (numpy fallback)."""
from datetime import date, timedelta
from hedging.forecast import forecast_oil


def _series():
    d0 = date(2024, 1, 1)
    return [{"date": d0 + timedelta(days=i), "OIL_1": 900 + i * 0.5} for i in range(400)]


def test_forecast_shape_and_trend():
    out = forecast_oil(_series(), "OIL_1", periods=180)
    assert len(out) > 12
    assert all(set(m) == {"month", "first", "avg", "max", "min"} for m in out)
    assert out[-1]["avg"] > out[0]["avg"]  # upward trend continues


def test_start_date_filter():
    out = forecast_oil(_series(), "OIL_1", periods=180, start_date=date(2025, 1, 1))
    assert out[0]["month"] >= "2025-01"
