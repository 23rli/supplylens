"""
AI copilot: structured, inline AI helpers grounded on live decision data.
Uses the LLM (Azure Foundry gpt-5-mini) when configured; deterministic fallback
otherwise so the app always works.
"""
from decision.store import explain, today
from ai.llm import chat, is_configured, LLMError

SYS = ("You are SupplyLens AI, a supply-chain risk analyst for a commodity and "
       "manufacturing operation across plants in Boston, Chicago, and Seattle. "
       "Be concise, decisive, and only use the data provided. Lead with the "
       "most critical finding. Never invent numbers.")


def _llm_or_none(prompt: str, max_tokens: int = 3000) -> str | None:
    if not is_configured():
        return None
    try:
        return chat([{"role": "system", "content": SYS}, {"role": "user", "content": prompt}], max_tokens=max_tokens)
    except LLMError:
        return None


def briefing() -> dict:
    t = today()
    fallback = (f"{t['critical']} CRITICAL risks need action, {t['high']} HIGH to monitor. "
                f"${t['dollars_at_risk']:,.0f} exposed.")
    cards = "; ".join(f"{c['sku_name']} @ {c['site_id']} (buffer {c['buffer_days']}d, ${c['dollars_at_risk']:,.0f})"
                      for c in t["cards"]) or "none"
    prompt = (f"Write a 2-sentence morning risk briefing for an operations manager. "
              f"Data: {t['critical']} critical, {t['high']} high, ${t['dollars_at_risk']:,.0f} total exposure. "
              f"Top items: {cards}.")
    headline = _llm_or_none(prompt) or fallback
    return {"headline": headline, "ai": is_configured(),
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
    prompt = (f"Explain in 2 sentences why SKU {sku} at {site} is {e['risk']} risk "
              f"(buffer {e['buffer_days']} days, ${e['dollars_at_risk']:,.0f} exposed) and which action to take. "
              f"Options: {actions}. Recommended: {rec['label'] if rec else 'n/a'}.")
    e["narrative"] = _llm_or_none(prompt) or fallback
    e["confidence"] = "High - based on live stock and supplier history"
    e["ai"] = is_configured()
    return e
