# Business Requirements & Feature Specification

**Source:** Two spreadsheet models — a **Commodity Procurement / Hedging Planner** and a **52-Week Inventory Overstock / Understock Simulation Engine**.

**Purpose of this document:** Distill the business needs, domain logic, data model, and feature set of each tool so they can be re-implemented as a software application. This is written to be handed to a coding assistant (e.g. GitHub Copilot) as a build brief. Each section states *what the business needs*, *how the spreadsheet currently does it*, and *what an app implementation requires*.

> **Anonymization note:** All organization, facility, vendor, market, and SKU identifiers have been replaced with generic placeholders (e.g. `Plant A`, `Vendor 1`, `Market 12`, `SKU-0001`). Numeric defaults, formulas, and structure are preserved because they are the business logic, not identifying information. Swap the placeholders for real master data at import time.

> **Note on dates:** Both workbooks store months as spreadsheet serial date numbers (e.g. `45505` ≈ 2024-08-01, `45658` ≈ 2025-01-01). Treat every `45xxx` value in this document as a calendar month. An app should use real date types instead of serials.

---

# PART A — Commodity Procurement & Hedging Planner

## A1. Business case & need

The organization produces blended edible-oil products at multiple plants and must buy large volumes of raw vegetable oils (two primary oils plus high-oleic variants) to fulfill customer demand across a set of destination markets. Raw-oil prices are volatile. Buying everything on the **spot market** at delivery time exposes the business to price swings.

The tool exists to answer: **"How much of each oil should we lock in early (hedge) vs. buy on the spot market, on what schedule, to minimize total procurement cost while guaranteeing we cover forecasted customer demand?"**

It does three jobs:
1. **Forecast** how much oil is needed, per plant, per market, per month, derived from product demand and recipes.
2. **Plan & simulate hedging** using two configurable strategies, enforcing minimum coverage deadlines.
3. **Compare** the cost of the hedged strategy vs. buying everything on spot, and report the savings.

**Primary KPI:** *Amount Saved* (and *Saved per Metric Ton*) = (cost of spot-only procurement) − (cost of hedged procurement).

## A2. Core domain concepts

| Concept | Meaning |
|---|---|
| **Oil types** | `OIL_1` (primary oil A), `OIL_1H` (high-oleic variant of A), `OIL_2` (primary oil B), `OIL_2H` (high-oleic variant of B). Hedging is modeled primarily on the two base oils, `OIL_1` and `OIL_2`. |
| **Plants** | Production sites: **Plant A**, **Plant B**, **Plant C**. Each market is served by exactly one plant. |
| **Recipe** | Per (plant, market): the % blend of each oil in the finished product (e.g. 20% `OIL_1` / 50% `OIL_1H` / 15% `OIL_2` / 15% `OIL_2H`). Used to convert finished-product demand into raw-oil demand. |
| **Delivery / Shipment month** | The month a customer order must be delivered (the 12 months of the planning year). |
| **Coverage month** | The month in which a hedge/purchase decision is *made* (can be earlier than delivery). |
| **Hedge** | A forward purchase contract locking price & volume for a future delivery month. |
| **Spot market** | Buying at the prevailing price in the delivery month (no advance lock). |
| **Coverage %** | Fraction of a delivery month's required volume that has been secured by a given deadline. |
| **Metric Ton (MT)** | Base unit for all volumes. All costs are price-per-MT × MT. |

## A3. Two hedging strategies (the heart of the tool)

The total hedging program is split between two strategies by a configurable ratio (default **Strategy 1 = 75% / Strategy 2 = 25%**).

### Strategy 1 — "Toll Gate" (front-loaded)
A strategy that concentrates buying into the months closest to the decision date, governed by a "breakdown" weighting:
- **Three-month breakdown** (default): Month 1 = 48%, Month 2 = 32%, Month 3 = 20% of that delivery month's procurement is taken in successive coverage months.
- **Two-month breakdown**: 50% / 50%.
- Enforces **mandatory minimum coverage by quarterly deadlines** (default: 15% by Q1, 37.5% by Q2, 60% by Q3, 75% by Q4). The simulation reports actual coverage vs. mandatory minimum.
- A **percentage translator** matrix decides, for each (coverage month → delivery month) pair, whether that month is "forecast/enrolled" (1) or already hedged (0), and records the month each delivery's hedging completes.

### Strategy 2 — "Systematic" (smoothed / evenly distributed)
- **Three-month breakdown**: ~33.333% / 33.333% / 33.333% (even thirds).
- **Two-month breakdown**: 50% / 50%.
- Lower mandatory minimums (default: 6.25% / 12.5% / 18.75% / 25% by quarter) — i.e. it trickles coverage in steadily.
- Produces its own "% Enrolled", "Quantity Hedged", and average commodity price per month.

Both strategies output, per oil and per delivery month: **% enrolled, total quantity hedged (MT), total price, and average commodity price.** These feed the procurement comparison.

## A4. Calculation pipeline (data flow)

```
Product demand (Volume Forecasts, per plant/market/month)
        │  × Recipe % per oil
        ▼
Raw-oil volume needed  (Volume Forecast Breakdown: OIL_1 grid + OIL_2 grid, per market/month)
        │
        ▼
Historical daily prices (per oil)
        │  ── Price Forecasting Engine (Prophet, see A9) ──►
        ▼
Price Forecasts (per oil, per coverage month → First / Average / Min [/ Max] price for each delivery month)
        │
        ├─► Strategy 1 (Toll Gate) engine ──┐
        │   (breakdown %, min-coverage       │
        │    deadlines, % translator)        │
        ├─► Strategy 2 (Systematic) engine ──┤
        │                                    ▼
        │                          Hedges + Inventory ledger
        │                          (every hedge: date, oil, action, $/MT, MT, total, delivery month;
        │                           distilled per delivery month → # hedges, avg $/MT, total cost,
        │                           current volume, volume needed, excess inventory)
        ▼                                    │
Command Center  ◄────────────────────────────┘
 (per current month/quarter: contracts set, volume sourced,
  sourcing goal, "Volume Still Needed", available & predicted inventory)
        │
        ▼
Procurement Full Year  vs  Procurement from SPOT ONLY
        │
        ▼
Dashboard  (cost per plant, per oil, per strategy, per market;
            Amount Saved = Spot-only total − Hedged total)
```

## A5. Sheet-by-sheet feature inventory

Implement each of these as a module/view. "Inputs" are user-editable; "Outputs" are computed.

### A5.1 Dashboard (executive summary — read-only)
- **Cost Breakdown of Hedged Procurement by Plant**: per (plant × oil) total cost, total cost per plant, **cost per metric ton**.
- **Supply Ratio of total**: each plant's share of `OIL_1` and `OIL_2` supply.
- **Breakdown of Cost by Resource and Method**: Hedging cost vs Spot-market cost vs Inventory cost, split per oil. Cost per commodity, **Cost per Strategy** (Hedging total vs Spot-only total).
- **Amount Saved** and **Saved per Ton** (headline KPI).
- **Cost Breakdown by Markets**: per market, per delivery month, total cost and cost per MT (~30 markets).
- **Global Inputs panel** (these drive the whole model — see A6): Current Month, Start Year, End Year, Strategy 1 %, Strategy 2 %, Inventory Cost per MT, Starting Inventory per oil.
- **Strategy 1 & Strategy 2 Inputs panels**: the Month-1/2/3 breakdown weights and the 2-month breakdown weights, per oil.

### A5.2 Command Center (operational worklist)
For the current month **and** current quarter, for each oil:
- Contract delivery dates (next 3 delivery months).
- Total # of contracts, average cost/MT, total cost, total volume of contracts (pulled from the hedge ledger).
- **% expectation of contract fulfillment** by current month (e.g. 0.48 monthly, 0.80 quarterly).
- **Forecasted Volume** for the contract month.
- **Volume Sourcing Goal** = forecasted volume × fulfillment %.
- **Volume Still Needed** = sourcing goal − already sourced.
- **Current & Predicted Available Inventory** tables (per month / per quarter, per oil).
- **Simulation Coverage** tables: mandatory minimum vs simulated/current minimum coverage per quarterly deadline.
> Business need: tells a buyer *exactly how much of each oil still needs to be bought this month/quarter to stay on plan.*

### A5.3 Price Forecast (per oil)
- A grid of small per-coverage-month tables. For each coverage month, for each of the 12 delivery months: **First Price, Average Price, Minimum Price** ($/MT).
- A "current table" selector keyed off Current Month (boolean key column picks which sub-table is active).
- **Source of these numbers:** the tables are *generated* by a Prophet-based time-series forecasting engine (see **A9**) run per oil over historical daily prices. The engine outputs first/average/max/min per month; the planner currently consumes first/average/min.
> Business need: price scenarios the hedging engine prices contracts against. In an app this is a price-forecast data source (per oil, per coverage month, per delivery month, with first/avg/min variants), populated by the A9 engine rather than hand-entered.

### A5.4 Volume Forecasts
- Matrix: rows = delivery months, columns = markets (~30), each tagged with its **plant**. Values = forecasted finished-product volume (MT). Row totals per month.

### A5.5 Recipe
- Per (plant, market): `OIL_1` %, `OIL_1H` %, `OIL_2` %, `OIL_2H` %. (Percentages per market sum to 100%.) Includes an oil-abbreviation legend.

### A5.6 Volume Forecast Breakdown
- Takes Volume Forecasts × Recipe to produce **raw-oil demand**: one grid for `OIL_1` and one for `OIL_2`, per market per delivery month, with market totals and grand totals.

### A5.7 Hedges + Inventory (the transaction ledger + distillation)
- **Ledger**: append-only list of hedge transactions — `Date, Oil Type, Action, Cost per MT, Volume (MT), Total Cost, Delivery Month`.
- **Distilled values** per oil (one block per oil), keyed by delivery (procurement) month: **# of Hedges, Average Cost per MT, Total Cost, Total Current Volume, Volume Forecasted, Volume Needed, Excess Inventory (by forecast)**.
- Pivot grids that bucket each hedge by *month-when-contract-was-set* × *delivery month* (counts, volumes, costs).
> Business need: single source of truth for what has actually been hedged; everything else aggregates from here.

### A5.8 Strategy 1 / Strategy 2 engines
Per oil, per delivery month, per coverage month: **Percent of Total Monthly Procurement, Average Price per Commodity, Total Procurement (MT), Total Price**, plus **% Enrolled**, **Quantity Hedged**, **Average Commodity Price per Month**, and a **Simulation Coverage** block (deadline → mandatory minimum vs simulated minimum). A supporting **Percentage Translator** sheet holds the 0/1 enrollment matrices and the "Month Hedging Completed" lookup.

### A5.9 Procurement Full Year vs Procurement from SPOT ONLY
Two parallel scenario sheets, each per oil, per delivery month, grouped into quarters:
- Amount Required by Customer, Procurement from Strategy 2, Procurement from Strategy 1, Procurement from Hedging (All), Total Volume, **Net Remainder** (should be 0 when fully covered; negative in spot-only = unmet by hedging), Spot Market Prices, Total Spot Market Costs, Average Price per month, Inventory Costs, **Costs from Volume Error**, Costs from Hedging, **Total Monthly Procurement Costs**, quarterly & yearly totals.
- The two sheets differ only in whether hedging is applied (Full Year) or everything is spot (SPOT ONLY). The Dashboard's *Amount Saved* is the difference of their totals.

## A6. Global input parameters (the control panel)

These are the levers a user changes to run scenarios. Surface them as a settings/scenario panel:

| Parameter | Default | Effect |
|---|---|---|
| Current Month | 45505 (2024-08) | "Now" — drives Command Center, active price table, deadlines. |
| Start Year (hedging starts) | 2024 | Planning window start. |
| End Year (last shipment arrives) | 2025 | Planning window end. |
| Strategy 1 % | 0.75 | Share of program run by Strategy 1 (front-loaded). |
| Strategy 2 % | 0.25 | Share run by Strategy 2 (systematic); must sum to 1 with above. |
| Inventory Cost per MT | 0.01 | Carrying cost applied to held inventory. |
| Starting Inventory (per oil) | 0 / 0 | Opening stock offsets demand. |
| Strategy 1 3-month breakdown | 48% / 32% / 20% | Front-loaded weighting. |
| Strategy 1 2-month breakdown | 50% / 50% | |
| Strategy 2 3-month breakdown | 33.3% / 33.3% / 33.3% | Even weighting. |
| Strategy 2 2-month breakdown | 50% / 50% | |
| Mandatory min coverage (Strategy 1) | 15/37.5/60/75% by quarter | Compliance floor. |
| Mandatory min coverage (Strategy 2) | 6.25/12.5/18.75/25% by quarter | Compliance floor. |

## A7. Key formulas / business rules (re-implement these)

- **Raw-oil demand** = finished-product forecast (per market, per month) × recipe oil-% for that market.
- **Volume Sourcing Goal** = Forecasted Volume × % expected contract fulfillment.
- **Volume Still Needed** = Sourcing Goal − Volume already sourced (from ledger).
- **Strategy procurement** for a delivery month = breakdown-weight × monthly required volume, spread across coverage months; priced at the relevant forecast price.
- **% Enrolled / Coverage** = hedged volume ÷ total required volume for that month; compared against the quarterly mandatory minimum.
- **Excess Inventory** = current volume + incoming hedged volume − volume needed (per delivery month).
- **Cost per MT (per plant/market)** = total cost ÷ total MT.
- **Cost from Volume Error** = cost attributable to volume that had to be covered on spot because hedging fell short (drives spot-only scenario cost).
- **Amount Saved (headline KPI)** = Spot-only total cost − Hedged total cost; **Saved per Ton** = Amount Saved ÷ total MT.
- Coverage must satisfy: actual coverage ≥ mandatory minimum at each quarterly deadline (flag violations).

## A8. App implementation notes (Hedging Planner)
- **Data model (suggested tables):** `plants`, `markets(plant_id, name)`, `oils`, `recipes(plant_id, market_id, oil_id, pct)`, `product_demand(market_id, delivery_month, mt)`, `historical_prices(oil_id, date, price)`, `price_forecasts(oil_id, coverage_month, delivery_month, first, avg, min, max)`, `hedges(date, oil_id, action, price_per_mt, mt, total_cost, delivery_month, strategy, coverage_month)`, `scenario_params(...)`. The `price_forecasts` table is populated by the A9 forecasting engine from `historical_prices`.
- **Derived/computed:** raw-oil demand, per-strategy coverage, command-center worklist, full-year vs spot-only costs, dashboard aggregates.
- **Scenario engine:** changing any A6 parameter must recompute the whole pipeline and the Amount-Saved KPI. Build the calc layer as pure functions so scenarios can be diffed.
- **Validation:** recipe %s per market sum to 1; Strategy 1 % + Strategy 2 % = 1; coverage ≥ mandatory minimums; Net Remainder = 0 when fully hedged.
- **Replace spreadsheet serial months with real dates; replace cross-sheet cell references with relational joins.**

## A9. Price Forecasting Engine (Prophet time-series)

This is the upstream service that **produces** the Price Forecast tables in A5.3. It exists as a Python script today and should become a scheduled service/module in the app. There is one forecast run per base oil (`OIL_1`, `OIL_2`).

### A9.1 What it does (business need)
Turn a history of **daily** raw-oil prices into a forward **monthly** price outlook (first / average / max / min price per month) that the hedging engine uses to price and schedule contracts. It captures trend plus yearly, weekly, and an added **quarterly** seasonality — quarterly matters because procurement and the hedging deadlines are quarter-based.

### A9.2 Inputs
| Input | Default / example | Notes |
|---|---|---|
| Historical price table | sheet/table with a `Date` column + one price column per oil | Daily granularity. |
| Oil/series to forecast | `OIL_1`, `OIL_2` | One model fit per series. |
| `periods` (horizon) | 730 days (~2 years) | Daily future frame length. |
| `start_date` | user-supplied (MM/DD/YYYY) | Filters output to months on/after this date. |
| Forecast frequency | daily (`D`), then resampled to monthly | |

### A9.3 Processing pipeline (re-implement exactly)
1. **Map columns** to Prophet's expected schema: `Date → ds`, `<oil price> → y`; parse `ds` as datetime.
2. **Outlier removal (IQR method)** on `y`: compute Q1, Q3, `IQR = Q3 − Q1`; keep rows where `Q1 − 1.5·IQR ≤ y ≤ Q3 + 1.5·IQR`. Drops anomalous price spikes/dips before fitting.
3. **Fit Prophet** with default trend + yearly/weekly seasonality, **plus a custom seasonality**: `name='quarterly', period=365.25/4, fourier_order=5`.
4. **Forecast** a future daily frame of `periods` days; predict to get `yhat` (and `yhat_lower`/`yhat_upper` are available if confidence bands are wanted).
5. **Resample to monthly** and aggregate `yhat` into: **First Price of Month, Average (mean) Price of Month, Max Price of Month, Min Price of Month.**
6. **Filter** to months `≥ start_date`.
7. **Persist**: one output table (sheet) per oil — e.g. `OIL_1 Forecast`, `OIL_2 Forecast`. Optionally save a forecast plot per oil (trend + components).

### A9.4 Output → how it feeds the planner
The monthly summary rows (`Month, First, Average, Max, Min`) **are** the Price Forecast tables in A5.3. The planner currently consumes **First / Average / Min**; `Max` is produced but not used downstream (keep it — it's useful for risk/upside views and costs nothing).

### A9.5 Reference implementation (anonymized)
```python
import pandas as pd
from prophet import Prophet

def forecast_oil(data, price_col, periods, start_date):
    """Forecast one oil's price; return monthly first/avg/max/min."""
    df = data.rename(columns={'Date': 'ds', price_col: 'y'})
    df['ds'] = pd.to_datetime(df['ds'])

    # IQR outlier removal on the target series
    q1, q3 = df['y'].quantile(0.25), df['y'].quantile(0.75)
    iqr = q3 - q1
    df = df[(df['y'] >= q1 - 1.5 * iqr) & (df['y'] <= q3 + 1.5 * iqr)]

    model = Prophet()
    model.add_seasonality(name='quarterly', period=365.25 / 4, fourier_order=5)
    model.fit(df)

    future = model.make_future_dataframe(periods=periods, freq='D')  # e.g. periods=730 (~2 yrs)
    forecast = model.predict(future)[['ds', 'yhat']].set_index('ds')

    monthly = forecast.resample('M').agg({'yhat': ['first', 'mean', 'max', 'min']}).reset_index()
    monthly.columns = ['Month', 'First Price of Month', 'Average Price of Month',
                       'Max Price of Month', 'Min Price of Month']
    return monthly[monthly['Month'] >= pd.to_datetime(start_date)]

def run(start_date, prices):
    out = {}
    for oil in ('OIL_1', 'OIL_2'):                 # one fit per oil
        out[oil] = forecast_oil(prices, oil, periods=730, start_date=start_date)
    return out                                      # persist one table per oil
```

### A9.6 App implementation notes (forecasting engine)
- **Service boundary:** keep this as an isolated forecasting service/module (Prophet is a Python dependency — `prophet`, `pandas`; plotting needs `matplotlib`). Expose it as a job that writes to the `price_forecasts` table rather than coupling it into request handlers.
- **Suggested data model additions:** `historical_prices(oil_id, date, price)` as the input; the engine writes `price_forecasts(oil_id, coverage_month, delivery_month, first, avg, min, max)` consumed by A5.3. (Note: the current script keys output by forecast month; map "coverage month = run date / Current Month" when wiring into the planner's per-coverage-month tables.)
- **Parameters to expose:** horizon (`periods`), `start_date`, custom-seasonality settings (period & `fourier_order`), and the IQR multiplier (1.5) — all as config, not hard-codes.
- **Scheduling / regeneration:** re-run when new historical prices arrive or when Current Month advances, then refresh the planner's price tables. Cache fitted models if runs are frequent.
- **Robustness:** Prophet needs enough history and ≥2 non-null points; guard against empty series after IQR filtering, and validate that each oil's price column exists before fitting.
- **Optional:** persist `yhat_lower`/`yhat_upper` to drive best/worst-case price scenarios in the hedging comparison.

---

# PART B — 52-Week Inventory Overstock / Understock Simulation Engine

## B1. Business case & need

A spare-parts / components operation (≈2,500 SKUs across many vendors) must keep enough stock to avoid stockouts **without** tying up cash and warehouse pallet space in overstock. Each part has its own demand rate, lead time, reorder economics, and packaging (products per case, cases per pallet).

The engine exists to answer, per part, over the next **52 weeks**: **"Will this part go understocked (below safety stock) or overstocked (above the overstock point) — and in which weeks — given current on-hand, on-order, demand forecast, lead time, and reorder behavior?"**

It then surfaces the **worst offenders** (parts most over- or under-stocked) and quantifies the **pallet-space** impact.

**Primary outputs:** per part — # weeks overstocked, # weeks understocked, min/max/avg projected inventory (in products and in pallets), and ranked worst-offender lists.

## B2. Core domain concepts

| Concept | Meaning |
|---|---|
| **Part** | A stocked SKU: Part Number, Description, Vendor, Vendor Name. |
| **ABC group** | Inventory classification (A/B/C) by value/importance. |
| **On Hand / On Order / Forecast** | Current stock, inbound stock, annual demand forecast (products). |
| **Lead Time (weeks)** | Time from placing an order to its arrival. |
| **EOQ** | Economic Order Quantity — reorder batch size. |
| **Safety Stock** | Buffer below which the part is "understocked". |
| **Reorder / Restock Point** | Inventory level that triggers a new order. |
| **Overstock Point** (product & pallet) | Upper threshold above which the part is "overstocked". |
| **Product per Case / Cases per Pallet** | Packaging used to convert product counts → pallet counts. |
| **Weeks on Hand** | On-hand ÷ weekly demand. |
| **Unit Price** | Per-unit evaluation price (used with forecast to compute Annual Spend). |
| **Annual Spend** | Forecast × Unit Price (used to rank importance). |
| **Backlog / Pipeline** | Outstanding orders flowing in over time. |

## B3. The simulation (heart of the engine)

For each part, the engine rolls a **week-by-week inventory projection across 52 weeks** (week 0 = today). The projection is built from a chain of supporting calculations (each is a 2,500-row × 52-week grid). Re-implement this chain exactly:

1. **Data Processing (per part):**
   - `Average Demand during LT` = annual Forecast ÷ 52 (weekly demand), rounded up → **ADdLT**.
   - `On Order + On Hand`.
   - `Restock Point` = ADdLT × Lead Time + Safety Stock.
   - `# shipments in pipeline` = On Order ÷ EOQ (rounded up) → **SIP**.
   - `Arrival Interval` = Lead Time ÷ SIP (weeks between inbound shipments).

2. **Order Backlog grid** — distributes the existing pipeline (SIP shipments) across weeks using the arrival interval (a shipment "arrives" every `Arrival Interval` weeks).

3. **Order BL Arrival** — per week, how many backlog shipments arrive (difference of consecutive backlog levels).

4. **52 Wk Prediction (projected on-hand, products):**
   - Week 0 = current On Hand.
   - Each subsequent week: `prev_week + Total Gain(this week) − weekly demand (ADdLT)`.
   - **Total Gain** = (shipment arrivals this week) × EOQ — i.e. inbound replenishment.

5. **New Pipeline Log / reorder trigger:** when projected inventory drops **below Safety Stock**, the engine places a **new order** (flag = 1) that arrives `Lead Time` weeks later (tracked in *Order Arrival Dates* and *New Order Arrival* via COUNTIF on arrival week).

6. **Total Shipment Arrivals** = new-order arrivals + backlog arrivals → feeds Total Gain → closes the loop.

7. **Pallet Prediction:** projected products ÷ (Cases per Pallet × Product per Case) = projected **pallets** per week. Summed across all parts for a **total warehouse pallet load** per week (with and without backlog).

8. **OS Pallet Indicator:** per week, flag = 1 if projected inventory **> Overstock Point**.

### Per-part output metrics (the deliverables)
- **# of Weeks Overstocked** = COUNT of weeks above overstock point.
- **# of Weeks Understocked** = COUNT of weeks below 0 / below safety stock.
- **Min / Max / Average # of Products** over 52 weeks.
- **Min / Max / Average # of Pallets** over 52 weeks.
- **Max # of Pallets Over/Understocked** (space wasted or shortfall, in pallets).
- **Overstock Product Point** = ADdLT × Lead Time + Safety Stock + EOQ (the level above which you're carrying too much).
- **Overstock Pallet Point** = Overstock Product Point ÷ (Cases per Pallet × Product per Case).

## B4. Sheet-by-sheet feature inventory

### B4.1 Interface (master parts table + KPIs + search)
- One row per part (~2,500). **Input columns:** Part Number, Description, Vendor, Vendor Name, Lead Time (wks), ABC Group, On Hand, On Order, Forecast, Last Year Usage, Unit Price, Product per Case, Cases per Pallet, EOQ, Safety Stock.
- **Computed columns:** Weeks on Hand, Annual Spend, Overstock Product Point, Overstock Pallet Point, # Weeks Over/Understocked, Min/Max/Avg products, Min/Max/Avg pallets, Max pallets over/understocked.
- **Search panel:** enter a Part ID or Name → returns matching row and key attributes (Vendor, Lead Time, EOQ, Forecast, Safety Stock). Implement as a lookup/detail view.

### B4.2 52 Wk Prediction (product-level projection)
- Grid: rows = parts, columns = weeks 0–51, values = projected on-hand products. Plus per-row Min / Max / Average / Weeks-Understocked summary columns.

### B4.3 52 Wk Pallet Prediction (pallet-level projection)
- Same grid converted to pallets, plus a **top summary row**: total warehouse pallets per week **with backlog** and **without backlog**. Per-row Min/Max/Avg pallet columns.

### B4.4 Worst Offenders (ranked exception report)
- **Worst Overstock Offenders** and **Worst Understock Offenders** — the parts with the largest/most-persistent over- or under-stock, with all their key attributes. This is the action list for buyers/planners.

### B4.5 Organized Chart (charting feed)
- Reshaped series (per searched part) feeding inventory-vs-week charts: projected products, overstock point line, weekly demand line, etc. In an app this becomes interactive chart data for the selected part.

### B4.6 Supporting calc sheets (hidden — implement as internal services)
`Data Processing`, `Total Gain`, `Order Backlog`, `Order BL Arrival`, `Total Pipeline Log`, `New Pipeline Log`, `Total Shipment Arrivals`, `New Order Arrival`, `Order Arrival Dates`, `OS Pallet Indicator`. These are the intermediate grids of the B3 simulation; users never edit them.

## B5. Key formulas / business rules (re-implement these)

```
weekly_demand (ADdLT) = ceil(annual_forecast / 52)
restock_point         = ADdLT * lead_time + safety_stock
overstock_point       = ADdLT * lead_time + safety_stock + EOQ
overstock_pallet_pt   = overstock_point / (cases_per_pallet * product_per_case)
weeks_on_hand         = on_hand / weekly_demand
annual_spend          = unit_price * annual_forecast
SIP (pipeline ships)  = ceil(on_order / EOQ)
arrival_interval      = lead_time / SIP            (weeks between inbound shipments)

projection[0]         = on_hand
projection[w]         = projection[w-1] + total_gain[w] - ADdLT
total_gain[w]         = shipment_arrivals[w] * EOQ
reorder if projection[w] < safety_stock  -> new order arrives at week (w + lead_time)
pallets[w]            = projection[w] / (cases_per_pallet * product_per_case)
overstock_flag[w]     = projection[w] > overstock_point
understock_count      = count weeks where projection[w] < 0 (or < safety_stock)
overstock_count       = count weeks where overstock_flag[w] = 1
```

## B6. App implementation notes (Inventory Engine)
- **Data model:** `parts` (all input attributes above); everything else is **computed** — do not store the 52-week grids, generate them on demand from a simulation function `simulate(part) -> week[0..51] {products, pallets, overstock, understock}`.
- **Engine:** one pure function per part producing the weekly series; aggregate across parts for warehouse-level pallet load and for worst-offender ranking. This replaces the 11 interlocking spreadsheets.
- **Views:** (1) master parts table with computed KPI columns + filters (by ABC group, vendor, over/under-stock); (2) per-part detail with the 52-week inventory chart; (3) Worst Offenders dashboards (over & under); (4) warehouse pallet-load-over-time chart.
- **Performance:** 2,500 parts × 52 weeks = ~130k cells per grid and ~11 grids in the spreadsheet. In code this is a fast O(parts × weeks) loop — recompute live on input change.
- **Replace COUNTIF/array-formula plumbing with explicit loops; replace hard-coded 2,500-row ranges with the actual part list.**

---

# PART C — Shared / cross-cutting requirements

- **Units & dates:** standardize on Metric Tons (Planner) and product/pallet counts (Inventory Engine); convert spreadsheet serial months to ISO dates on import.
- **Scenario-driven recompute:** both tools are "change an input → recompute everything → compare." Architect the calculation layer as pure, testable functions decoupled from the UI.
- **Exception surfacing:** both tools exist to flag where the plan breaks — Planner: coverage below mandatory minimum / volume still needed; Inventory Engine: weeks over/understocked + worst offenders. Make these the primary dashboards.
- **Import path:** users will likely keep maintaining the source spreadsheets initially, so support importing the input columns (parts list / demand forecast / price forecast / recipes) from `.xlsx`/`.csv`.
- **Auditability:** keep the hedge ledger (Planner) and the parts master (Inventory Engine) as the single sources of truth; everything else is derived and reproducible.
- **Forecasting dependency:** the Planner's price inputs come from a Prophet-based Python forecasting engine (Part A, A9). It's an upstream batch job, not part of the live request path — schedule it and have the planner read its persisted output.

## Suggested build order
1. Data models + import for input tables (incl. `historical_prices`).
2. Price Forecasting Engine (A9, Prophet) → populates `price_forecasts`; unit-test monthly aggregates against the spreadsheet's price tables.
3. Pure calculation engines (Planner pipeline; per-part inventory simulation) with unit tests against the spreadsheet's known outputs.
4. Master tables + computed KPI columns.
5. Exception dashboards (Command Center / Worst Offenders).
6. Scenario controls + comparison views (Hedged vs Spot; warehouse pallet load).
7. Charts and per-item detail views.
