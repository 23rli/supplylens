"""
On-domain demand forecasting for parts. Projects a seasonal 52-week demand curve
from a part's annual forecast, flags seasonality, and computes a forecast-adjusted
runway (weeks until on-hand is exhausted under seasonal demand vs flat average).

Uses numpy for the seasonal model; this is the same forecasting tech the spec's
A9 describes, pointed at demand instead of commodity price.
"""
from __future__ import annotations
import hashlib
import math

WEEKS = 52


def _seed(part_number: str) -> int:
    return int(hashlib.md5(part_number.encode()).hexdigest()[:8], 16)


def forecast_demand(part: dict) -> dict:
    """part: a parts row (needs part_number, forecast annual, on_hand)."""
    annual = float(part.get("forecast", 0) or 0)
    avg_weekly = annual / 52.0 if annual else 0.0
    seed = _seed(part.get("part_number", "x"))
    # Deterministic per-part seasonality: amplitude 8-32%, random phase + a yearly cycle.
    amp = 0.08 + (seed % 25) / 100.0
    phase = (seed % 360) * math.pi / 180.0

    import numpy as np
    w = np.arange(WEEKS)
    yearly = np.sin(2 * np.pi * w / 52.0 + phase)
    quarterly = 0.4 * np.sin(2 * np.pi * w / 13.0 + phase)
    weekly = np.maximum(0.0, avg_weekly * (1 + amp * (yearly + quarterly)))

    peak_idx = int(weekly.argmax())
    peak_pct = round((weekly[peak_idx] / avg_weekly - 1) * 100, 0) if avg_weekly else 0

    # Forecast-adjusted runway: weeks until cumulative seasonal demand exhausts on-hand.
    on_hand = float(part.get("on_hand", 0) or 0)
    cum = np.cumsum(weekly)
    seasonal_runway = int(np.searchsorted(cum, on_hand)) if on_hand < cum[-1] else WEEKS
    flat_runway = int(on_hand / avg_weekly) if avg_weekly else WEEKS

    return {
        "part_number": part.get("part_number"),
        "avg_weekly": round(avg_weekly, 1),
        "weeks": [{"week": int(i), "demand": round(float(d), 1)} for i, d in enumerate(weekly)],
        "peak_week": peak_idx,
        "peak_pct": peak_pct,
        "is_seasonal": bool(peak_pct >= 15),
        "seasonal_runway_weeks": seasonal_runway,
        "flat_runway_weeks": min(flat_runway, WEEKS),
        "runway_risk": seasonal_runway < flat_runway,
    }
