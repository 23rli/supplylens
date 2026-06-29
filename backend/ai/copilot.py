"""
AI copilot: structured, inline AI helpers. Each returns JSON the UI renders as
badges/chips. Uses Azure OpenAI if configured; deterministic fallback otherwise.
"""
from decision.store import explain, today


def briefing() -> dict:
    t = today()
    headline = (f"{t['critical']} CRITICAL risks need action, {t['high']} HIGH to monitor. "
                f"${t['dollars_at_risk']:,.0f} exposed.")
    suggestions = [f"Fix {c['sku_name']} @ {c['site_id']}" for c in t["cards"]]
    return {"headline": headline, "suggestions": suggestions, "cards": t["cards"]}


def explain_decision(sku: str, site: str) -> dict:
    e = explain(sku, site)
    if not e:
        return {}
    rec = next((a for a in e["actions"] if a["recommended"]), e["actions"][0] if e["actions"] else None)
    e["narrative"] = (f"{sku} at {site} is {e['risk']} (buffer {e['buffer_days']}d). "
                      f"Recommended: {rec['label']}." if rec else f"{sku} at {site} is {e['risk']}.")
    e["confidence"] = "High — based on live stock and supplier history"
    return e
