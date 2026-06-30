# Features & Purpose

## The problem SupplyLens solves

Supply-chain teams usually find out about a stockout **after** it happens — when a
plant line stops or a customer order can't ship. By then the only fix is an
expensive emergency (air-freight, spot buys, expedite fees).

SupplyLens flips this. It continuously scores every SKU and supplier, surfaces the
items that will run out *before their lead-time window closes*, and recommends the
cheapest action that still avoids the stockout. It also helps procurement decide
**when** to lock in commodity prices to save money.

It is a **decision-support tool**, not a general chatbot: every number comes from
your live operational data.

---

## The screens

### Today — daily risk briefing
Your morning landing page. Shows a plain-English AI briefing ("3 critical risks need
action, $X exposed"), the top critical items, and a one-click **Resolve** button for
each. Includes an **Ask AI** box for natural-language questions about your data.

### Risk Intelligence — SKU & supplier scoring
- A filterable table of every SKU with its risk level, days of supply, and buffer.
- A site heatmap (Boston / Chicago / Seattle) of where risk is concentrated.
- Supplier reliability: on-time delivery rate, quality score, and a 12-month
  incident history.

**How risk is scored** (see also the README):

| Term | Formula |
|---|---|
| Days of Supply | `current_stock / avg_daily_demand` |
| Buffer Days | `days_of_supply - lead_time` (negative = stockout is unavoidable without emergency action) |

| Risk | Condition |
|---|---|
| CRITICAL | Days of Supply ≤ Lead Time |
| HIGH | ≤ Lead Time × 1.5 |
| MEDIUM | ≤ Lead Time × 2.0 |
| LOW | > Lead Time × 2.0 |

### Inventory Engine — 52-week simulation
Projects each part's stock level week-by-week for a year using forecast demand,
lead time, safety stock, and economic order quantity (EOQ). From this it derives:
- **Worst offenders** — the parts most overstocked (tying up cash) or most
  understocked (stockout risk).
- **Warehouse pallet load** — projected total pallets per week, for space planning.
- **Demand forecasting** — seasonal weekly demand and a forecast-adjusted runway.
- **Import** — drop in your own parts via CSV or XLSX (see
  [Using Your Own Data](data-guide.md)).

### Hedging Planner — commodity procurement
For commodities like **steel** and **aluminum**, compares two buying strategies:
- **Strategy 1 (front-loaded / "Toll Gate")** — locks coverage early, ~2 months
  ahead, capturing lower forward prices on a rising market.
- **Strategy 2 (systematic)** — spreads buying evenly, paying the trailing average.

A slider blends the two; the **Amount Saved** KPI updates live to show hedged cost
vs. buying everything at delivery-month spot price. Pricing is fed by the forecast,
so the recommendation reflects expected market movement.

### Actions — execution log
A tracked, per-tenant record of every executed action (expedite POs, stock
transfers) with cost and benefit, so decisions are auditable.

### AI Analyst — grounded chat
A conversational analyst that can answer free-form questions across every module.
Each request injects the current database state into the prompt, so answers are
computed from live data and cite specific SKUs, sites, and suppliers.

---

## How the AI stays trustworthy

1. **Grounding** — before each call, the app reads the live database and embeds the
   relevant rows directly into the prompt. The model is told to use *only* that data.
2. **Deterministic fallback** — if no AI key is configured (or the model is
   unreachable), every AI feature falls back to a rule-based summary, so the app
   never breaks.
3. **Speed** — answers are cached briefly and run at `reasoning_effort=minimal` for
   sub-3-second responses.

See [Architecture](architecture.md) for the full data flow.
</content>
