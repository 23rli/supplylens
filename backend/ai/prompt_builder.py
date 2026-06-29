"""
Builds the system prompt for Claude API calls.
This is the most important file — it determines quality of AI responses.
"""
from datetime import date

def format_risk_data(risk_rows: list[dict]) -> str:
    """Formats risk data as a readable table for the system prompt."""
    critical = [r for r in risk_rows if r["risk_level"] == "CRITICAL"]
    high = [r for r in risk_rows if r["risk_level"] == "HIGH"]
    medium = [r for r in risk_rows if r["risk_level"] == "MEDIUM"]
    low = [r for r in risk_rows if r["risk_level"] == "LOW"]

    lines = []
    lines.append(f"TOTAL SKU-SITE COMBINATIONS: {len(risk_rows)}")
    lines.append(f"CRITICAL: {len(critical)} | HIGH: {len(high)} | MEDIUM: {len(medium)} | LOW: {len(low)}")
    lines.append("")

    if critical:
        lines.append("=== CRITICAL RISK SKUs (stockout likely before next delivery) ===")
        for r in critical:
            lines.append(
                f"  {r['sku_name']} @ {r['site_id']} | "
                f"Stock: {r['current_stock']} units | "
                f"Days of supply: {r['days_of_supply']} | "
                f"Lead time: {r['lead_time_days']} days | "
                f"Buffer: {r['buffer_days']} days | "
                f"Category: {r['category']} | "
                f"Action: {r['recommended_action']}"
            )

    if high:
        lines.append("")
        lines.append("=== HIGH RISK SKUs (within 1.5x lead time) ===")
        for r in high:
            lines.append(
                f"  {r['sku_name']} @ {r['site_id']} | "
                f"Days of supply: {r['days_of_supply']} | "
                f"Lead time: {r['lead_time_days']} days | "
                f"Category: {r['category']}"
            )

    if medium:
        lines.append("")
        lines.append("=== MEDIUM RISK SKUs (approaching reorder window) ===")
        for r in medium[:5]:  # Cap at 5 to keep prompt manageable
            lines.append(f"  {r['sku_name']} @ {r['site_id']} | Days of supply: {r['days_of_supply']}")
        if len(medium) > 5:
            lines.append(f"  ... and {len(medium) - 5} more MEDIUM risk items")

    return "\n".join(lines)


def format_supplier_data(supplier_rows: list[dict]) -> str:
    """Formats supplier data for the system prompt."""
    lines = []
    for s in supplier_rows:
        reliability_pct = round(s["on_time_delivery_rate"] * 100, 1)
        incident_note = f" | ⚠️ {s['incident_count_12m']} incidents in last 12 months" if s["incident_count_12m"] > 0 else ""
        lines.append(
            f"  {s['supplier_name']} ({s['supplier_id']}) | "
            f"Tier: {s['contract_tier']} | "
            f"Country: {s['country']} | "
            f"On-time: {reliability_pct}% | "
            f"Avg lead time: {s['avg_lead_time_days']} days{incident_note}"
        )
    return "\n".join(lines)


def format_incidents(incident_rows: list[dict]) -> str:
    """Formats recent incident data for the system prompt."""
    if not incident_rows:
        return "  No recent incidents on record."
    lines = []
    for i in incident_rows:
        delay_note = f" ({i['days_delayed']} days delayed)" if i["days_delayed"] > 0 else ""
        lines.append(
            f"  [{i['incident_date']}] {i['supplier_name']}: {i['incident_type']}{delay_note} — "
            f"Severity: {i['severity']} — Affected SKUs: {i['affected_skus']}"
        )
    return "\n".join(lines)


def build_system_prompt(context: dict) -> str:
    """
    Builds the full system prompt for Claude.
    context is the dict returned by database.get_ai_context()
    """
    today = date.today().strftime("%B %d, %Y")
    stats = context["stats"]

    return f"""You are SupplyLens AI, an intelligent supply chain risk analyst for a medical device distribution company operating across three sites: Boston, Chicago, and Seattle.

TODAY'S DATE: {today}

YOUR ROLE:
- Identify and explain inventory risks based on real operational data
- Recommend specific, ranked actions with clear tradeoffs
- Answer questions about suppliers, SKUs, sites, and trends
- Help managers make confident, data-driven decisions

CRITICAL RULE: You must ONLY answer based on the data provided below. Do not invent numbers, SKUs, suppliers, or incidents that are not in this data. If you cannot answer from the data, say so and explain what additional data would help.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CURRENT INVENTORY RISK DATA (as of {today})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{format_risk_data(context["risk_summary"])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUPPLIER HEALTH DATA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{format_supplier_data(context["suppliers"])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECENT SUPPLIER INCIDENTS (last 10)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{format_incidents(context["recent_incidents"])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HEADLINE STATS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Critical risk SKU-site pairs: {stats.get("critical_skus", "n/a")}
- High risk SKU-site pairs: {stats.get("high_risk_skus", "n/a")}
- Average days of supply across all SKUs: {stats.get("avg_days_of_supply", "n/a")} days
- Overall supplier reliability: {stats.get("supplier_reliability_pct", "n/a")}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INVENTORY ENGINE (52-week simulation)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Total parts: {context.get("inventory", {}).get("total_parts", "n/a")}
- Parts at risk of understock: {context.get("inventory", {}).get("understock_parts", "n/a")}
- Parts at risk of overstock: {context.get("inventory", {}).get("overstock_parts", "n/a")}
- Annual spend: ${context.get("inventory", {}).get("total_annual_spend", "n/a")}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HEDGING PLANNER (current scenario)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Amount Saved (hedged vs spot-only): ${context.get("hedging", {}).get("amount_saved", "n/a")}
- Saved per ton: ${context.get("hedging", {}).get("saved_per_ton", "n/a")}
- Coverage on plan: {context.get("hedging", {}).get("all_coverage_ok", "n/a")}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESPONSE GUIDELINES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
When recommending actions, always rank them and explain the tradeoff:
  • EXPEDITE — Fastest resolution; higher cost; use for Critical category items only
  • REBALANCE — Transfer stock between sites; no cost; takes 1-2 days; good for non-critical
  • SUBSTITUTE — Use alternate SKU; may affect clinical workflow; confirm with operations
  • STANDARD ORDER — Appropriate when buffer_days > 0 but monitoring needed
  • DEFER — Accept temporary shortage; only appropriate for Consumable/Standard category

Keep responses concise and decisive. Supply chain managers need clear direction, not lengthy explanations. Use bullet points for action lists. Lead with the most critical finding.

End responses involving risk with a one-line confidence note, e.g.: "Confidence: High — based on current stock levels and 12-month supplier history."
"""
