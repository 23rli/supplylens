"""
Price forecasting engine (REQUIREMENTS_SPEC A9). One fit per oil over daily prices,
output monthly first/avg/max/min. Uses Prophet if installed; otherwise a numpy
trend + yearly + quarterly seasonality fallback. Same interface either way.
"""
from __future__ import annotations
import math
from datetime import date, timedelta

IQR_MULT = 1.5


def _iqr_filter(series: list[float]) -> tuple[float, float]:
    s = sorted(series)
    n = len(s)
    q1 = s[n // 4]; q3 = s[(3 * n) // 4]
    iqr = q3 - q1
    return q1 - IQR_MULT * iqr, q3 + IQR_MULT * iqr


def _fallback_forecast(days: list[date], y: list[float], horizon: int) -> list[float]:
    """Least-squares trend + yearly + quarterly seasonality (Prophet-free)."""
    import numpy as np
    t = np.arange(len(y), dtype=float)
    yr, qt = 365.25, 365.25 / 4
    X = np.column_stack([np.ones_like(t), t,
                         np.sin(2*np.pi*t/yr), np.cos(2*np.pi*t/yr),
                         np.sin(2*np.pi*t/qt), np.cos(2*np.pi*t/qt)])
    coef, *_ = np.linalg.lstsq(X, np.array(y), rcond=None)
    ft = np.arange(len(y) + horizon, dtype=float)
    Xf = np.column_stack([np.ones_like(ft), ft,
                          np.sin(2*np.pi*ft/yr), np.cos(2*np.pi*ft/yr),
                          np.sin(2*np.pi*ft/qt), np.cos(2*np.pi*ft/qt)])
    return list(Xf @ coef)


def forecast_oil(prices: list[dict], oil_id: str, periods: int = 730,
                 start_date: date | None = None) -> list[dict]:
    """prices: [{'date': date, oil_id: price}]. Returns monthly first/avg/max/min."""
    rows = [(r["date"], float(r[oil_id])) for r in prices if r.get(oil_id) is not None]
    rows.sort()
    lo, hi = _iqr_filter([p for _, p in rows])
    rows = [(d, p) for d, p in rows if lo <= p <= hi]
    if len(rows) < 2:
        raise ValueError(f"Not enough data for {oil_id}")
    days = [d for d, _ in rows]; y = [p for _, p in rows]

    try:
        from prophet import Prophet
        import pandas as pd
        df = pd.DataFrame({"ds": pd.to_datetime(days), "y": y})
        m = Prophet(); m.add_seasonality(name="quarterly", period=365.25/4, fourier_order=5)
        m.fit(df)
        fut = m.make_future_dataframe(periods=periods, freq="D")
        yhat = list(m.predict(fut)["yhat"]); future_days = list(fut["ds"].dt.date)
    except Exception:
        yhat = _fallback_forecast(days, y, periods)
        future_days = days + [days[-1] + timedelta(days=i) for i in range(1, periods + 1)]

    buckets: dict[str, list[float]] = {}
    for d, v in zip(future_days, yhat):
        buckets.setdefault(f"{d.year}-{d.month:02d}", []).append(v)
    out = []
    for mo, vals in sorted(buckets.items()):
        ym = date(int(mo[:4]), int(mo[5:]), 1)
        if start_date and ym < start_date.replace(day=1):
            continue
        out.append({"month": mo, "first": round(vals[0], 2), "avg": round(sum(vals)/len(vals), 2),
                    "max": round(max(vals), 2), "min": round(min(vals), 2)})
    return out
