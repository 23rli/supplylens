"""
AI copilot: structured, inline AI helpers grounded on live decision data.
Uses the LLM (Azure Foundry gpt-5-mini) when configured; deterministic fallback
otherwise so the app always works. Results are cached briefly to keep the UI snappy.
"""
import time
from decision.store import explain, today
from db import fetch_all
from ai.llm import chat, is_configured, LLMError

SYS = ("You are SupplyLens AI, a supply-chain risk analyst for a commodity and "
       "manufacturing operation across plants in Boston, Chicago, and Seattle. "
       "Be concise, decisive, and only use the data provided. Lead with the "
       "most critical finding. Never invent numbers.")

_CACHE_TTL = 120  # seconds
_cache: dict[str, tuple[float, str]] = {}


def _cached_llm(key: str, prompt: str) -> str | None:
    hit = _cache.get(key)
    if hit and time.time() - hit[0] < _CACHE_TTL:
        return hit[1]
    if not is_configured():
        return None
    try:
        out = chat([{"role": "system", "content": SYS}, {"role": "user", "content": prompt}])
        _cache[key] = (time.time(), out)
        return out
    except LLMError:
        return None


def briefing() -> dict:
    t = today()
    fallback = (f"{t['critical']} CRITICAL risks need action, {t['high']} HIGH to monitor. "
                f"${t['dollars_at_risk']:,.0f} exposed.")
    cards = "; ".join(f"{c['sku_name']} @ {c['site_id']} (buffer {c['buffer_days']}d, ${c['dollars_at_risk']:,.0f})"
                      for c in t["cards"]) or "none"
    key = f"brief:{t['critical']}:{t['high']}:{t['dollars_at_risk']}:{cards}"
    prompt = (f"Write a 2-sentence morning risk briefing for an operations manager. "
              f"Data: {t['critical']} critical, {t['high']} high, ${t['dollars_at_risk']:,.0f} total exposure. "
              f"Top items: {cards}.")
    return {"headline": _cached_llm(key, prompt) or fallback, "ai": is_configured(),
            "suggestions": [f"Resolve {c['sku_name']} @ {c['site_id']}" for c in t["cards"]],
            "cards": t["cards"]}


def explain_decision(sku: str, site: str) -> dict:
    e = explain(sku, site)
    if not e:
        return {}
    rec = next((a for a in e["actions"] if a["recommended"]), e["actions"][0] if e["actions"] else None)
    fallback = (f"{sku} at {site} is {e['risk']} (buffer {e['buffer_days']}d). "
                f"Recommended: {rec['label']}." if rec else f"{sku} at {site} is {e['risk']}.")
    actions = "; ".join(f"{a['type']} (cost ${a['cost']:,.0f}, benefit ${a['benefit']:,.0f})" for a in e["actions"])
    key = f"explain:{sku}:{site}:{e['risk']}:{e['buffer_days']}"
    prompt = (f"Explain in 2 sentences why SKU {sku} at {site} is {e['risk']} risk "
              f"(buffer {e['buffer_days']} days, ${e['dollars_at_risk']:,.0f} exposed) and which action to take. "
              f"Options: {actions}. Recommended: {rec['label'] if rec else 'n/a'}.")
    e["narrative"] = _cached_llm(key, prompt) or fallback
    e["confidence"] = "High - based on live stock and supplier history"
    e["ai"] = is_configured()
    return e


def ask(question: str) -> dict:
    """Natural-language Q&A grounded on the full live risk picture."""
    rows = fetch_all("SELECT sku_id, sku_name, site_id, category, risk_level, buffer_days, "
                     "days_of_supply, current_stock, primary_supplier_id FROM sku_risk_summary "
                     "ORDER BY buffer_days ASC")
    sups = fetch_all("SELECT supplier_id, supplier_name, contract_tier, on_time_delivery_rate, "
                     "avg_lead_time_days, incident_count_12m FROM suppliers")
    context = "RISK ROWS:\n" + "\n".join(
        f"  {r['sku_name']} @ {r['site_id']}: {r['risk_level']}, buffer {r['buffer_days']}d, "
        f"DoS {r['days_of_supply']}d, stock {r['current_stock']}, supplier {r['primary_supplier_id']}"
        for r in rows[:25])
    context += "\n\nSUPPLIERS:\n" + "\n".join(
        f"  {s['supplier_name']} ({s['supplier_id']}): tier {s['contract_tier']}, "
        f"on-time {round((s['on_time_delivery_rate'] or 0)*100)}%, lead {s['avg_lead_time_days']}d, "
        f"{s['incident_count_12m']} incidents/12mo" for s in sups)
    prompt = (f"Answer the manager's question using ONLY this live data. Be concise, cite specific "
              f"SKUs/sites/suppliers, and end with one recommended next step. Answer in under 80 words.\n\n{context}\n\nQUESTION: {question}")
    fallback = ("AI is offline. Based on the data, focus on the most negative-buffer CRITICAL items first "
                "and check whether their primary supplier is reliable.")
    answer = fallback
    if is_configured():
        try:
            answer = chat([{"role": "system", "content": SYS}, {"role": "user", "content": prompt}], max_tokens=900)
        except LLMError:
            answer = fallback
    return {"answer": answer, "ai": is_configured()}
