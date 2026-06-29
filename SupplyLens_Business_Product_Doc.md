# SupplyLens — Business & Product Document
### Supply Chain Risk Intelligence Platform
**Version 1.0 | Prepared for Product, Consulting & APM Recruiting Contexts**

---

## EXECUTIVE SUMMARY

SupplyLens is an AI-powered supply chain risk intelligence platform designed for operations and procurement teams at medical device distribution companies. It consolidates inventory levels, supplier performance data, and historical incident records into a single control tower — and layers a conversational AI analyst on top that can answer operational questions, surface hidden risks, and recommend ranked response actions in real time.

The platform addresses a fundamental breakdown in how supply chain risk is currently managed: critical data exists across disconnected systems, risk is identified reactively after stockouts occur rather than proactively before them, and the analytical work required to synthesize that data into decisions takes hours of manual effort that most operations teams cannot afford.

SupplyLens is not a general-purpose chatbot. It is a decision-support system grounded in live operational data, purpose-built for one high-stakes domain: keeping critical medical supplies in stock across multi-site distribution networks.

---

## 1. THE PROBLEM

### 1.1 The Business Context

Medical device distribution is one of the highest-stakes supply chain environments in existence. A stockout of surgical gloves, IV catheters, or sterile drapes does not merely result in a lost sale — it can delay procedures, create clinical liability, and damage long-term hospital relationships that represent millions of dollars in recurring revenue. Yet despite these stakes, most mid-market distributors manage inventory risk with the same tools they have used for decades: Excel spreadsheets, ERP systems designed for transaction recording rather than risk analysis, and periodic manual reviews.

### 1.2 The Five Core Failure Modes

**Failure Mode 1: Reactive risk detection**
Most operations teams discover a stockout risk only when a reorder alert fires in their ERP — by which point, the lead time window may already be missed. The gap between "data exists" and "risk is visible" is often days or weeks.

**Failure Mode 2: Siloed data**
Inventory levels live in one system. Supplier performance data lives in another. Incident history is often in email threads or manual logs. No single view synthesizes all three into a unified risk picture.

**Failure Mode 3: No supplier context at the point of decision**
When a buyer sees a low-stock alert, they typically have no visibility into whether their primary supplier is currently reliable, has recent late deliveries, or has an active incident affecting other SKUs. That context exists — it's just not connected.

**Failure Mode 4: One-dimensional risk metrics**
Traditional reorder point logic only looks at current stock vs. a fixed threshold. It does not account for lead time variability, supplier reliability, item criticality, or the availability of backup options. A 30-day supply of a non-critical consumable is fine; a 30-day supply of a critical surgical item with a 28-day lead time and an unreliable primary supplier is a crisis.

**Failure Mode 5: Analysis paralysis from too much data**
Large distributors may track thousands of SKUs across dozens of sites. Even when risk data is available, synthesizing it into prioritized actions requires analytical work that most operations teams cannot do continuously. The result is infrequent, incomplete reviews.

### 1.3 The Cost of Getting This Wrong

Industry research across healthcare supply chains consistently points to several categories of cost from poor inventory risk management:

- **Stockout costs:** Emergency procurement at spot pricing, expediting fees, air freight premiums — often 2–5x standard procurement costs
- **Service failure costs:** Missed SLAs, contractual penalties, and hospital relationship damage
- **Operational disruption costs:** Staff time spent on emergency sourcing, cross-site transfers, and substitution coordination
- **Carrying cost waste:** Overstocking driven by lack of confidence in risk visibility, tying up working capital unnecessarily

For a mid-market medical device distributor managing $50M–$500M in annual inventory spend, even a 1–2% reduction in emergency procurement costs and stockout-related losses represents significant bottom-line impact.

---

## 2. THE SOLUTION

### 2.1 What SupplyLens Does

SupplyLens gives operations and procurement teams a unified risk intelligence layer on top of their supply chain data. It does three things that existing tools do not do well together:

**1. Risk Synthesis**
Rather than showing raw inventory numbers, SupplyLens computes a multi-dimensional risk score for every SKU at every site, incorporating current stock, average daily demand, lead time, item criticality category, and supplier reliability. The output is an immediately actionable risk classification: CRITICAL, HIGH, MEDIUM, or LOW — with the specific reasoning behind each classification visible.

**2. Supplier Intelligence**
SupplyLens maintains a live supplier health view that aggregates on-time delivery rates, average lead times, contract tier, and incident history. This context is surfaced at the point of decision — so when a buyer sees a CRITICAL risk flag on a SKU, they immediately know whether their primary supplier is reliable, whether a backup exists, and what the historical pattern looks like.

**3. AI-Powered Decision Support**
A conversational AI analyst — grounded exclusively in the platform's live data — allows managers to ask natural language questions and receive specific, data-backed answers with ranked action recommendations. This is not a general-purpose chatbot; it cannot hallucinate data that isn't there. It reasons only over what the platform knows, and it tells the user its confidence level.

### 2.2 The Core Differentiator

The difference between SupplyLens and a standard BI dashboard is the AI layer's grounding architecture. A traditional dashboard shows data; a manager must still do the analytical work of interpreting it and deciding what to do. SupplyLens closes that gap — the AI does the synthesis and recommends specific actions with explicit tradeoffs.

The difference between SupplyLens and a general AI assistant (like ChatGPT) is data fidelity. A general AI will hallucinate plausible-sounding supply chain advice. SupplyLens injects live database state into every AI query, constraining the model to reason only over actual operational reality. When SupplyLens says "SKU004 at the Boston site will stockout before your next delivery," that claim is computed from real numbers, not generated from training data.

---

## 3. TARGET USERS

### 3.1 Primary Persona — The Operations Manager

**Name:** Sarah, VP of Operations
**Company:** Mid-size medical device distributor, $150M annual revenue, 3 distribution sites
**Day job:** Oversees inventory management, supplier relationships, and site operations. Reviews daily reports, handles exception management, and is accountable for service level targets.

**Current pain:** Spends 2+ hours daily pulling data from ERP, manually computing days-of-supply, and cross-referencing supplier performance. Risk review is weekly at best. Stockout discoveries are often surprises.

**What she needs from SupplyLens:**
- A morning dashboard that immediately shows what requires attention today
- Ability to drill into any flagged item and understand why it's at risk
- Confidence that the AI's recommendations are grounded in real data, not guesses
- A tool she can share with her team so everyone is working from the same risk picture

**Success metric:** Reduces daily risk review time from 2+ hours to 20 minutes. Zero stockout surprises.

---

### 3.2 Secondary Persona — The Procurement Buyer

**Name:** Marcus, Senior Procurement Specialist
**Company:** Same distributor as Sarah
**Day job:** Manages supplier relationships for 80+ SKUs. Places purchase orders, negotiates pricing, manages supplier scorecards, and handles exception escalations.

**Current pain:** Makes sourcing decisions with incomplete supplier context. Often discovers mid-order that a supplier has an active reliability issue. Has no systematic way to track which suppliers are trending worse over time.

**What he needs from SupplyLens:**
- Supplier health scores with incident history at a glance
- Immediate visibility into which of his SKUs are most exposed to unreliable suppliers
- AI questions like "Which backup supplier should I use if SUP002 fails again?"
- Early warning on SKUs approaching reorder point so he can plan rather than react

**Success metric:** Reduces reactive emergency orders by 40%. Improves supplier scorecard accuracy.

---

### 3.3 Tertiary Persona — The Site Manager

**Name:** Jennifer, Boston Distribution Center Manager
**Company:** Same distributor
**Day job:** Manages daily warehouse operations, coordinates with clinical customers, and handles inbound/outbound logistics for her site.

**Current pain:** Doesn't have visibility into what's at risk until procurement tells her. No ability to proactively ask "can I transfer stock from Chicago to cover a gap here?"

**What she needs from SupplyLens:**
- Site-filtered dashboard showing only her location's risk
- AI questions like "What should I rebalance from other sites to cover this week's gaps?"
- Clear escalation signal for when she needs to alert her VP vs. handle it herself

**Success metric:** Reduces her escalations to VP by handling more risk proactively at the site level.

---

## 4. FEATURES — CURRENT SCOPE (V1.0)

### 4.1 Dashboard Overview

**What it is:** The landing page and primary daily view for operations managers.

**Components:**
- **KPI Bar** — Four headline numbers updated in real time: Critical Risk SKUs, High Risk SKUs, Average Days of Supply, and Overall Supplier Reliability Rate. Designed to be readable in under 10 seconds.
- **Top 10 Risk Table** — The highest-priority SKU-site combinations, ranked by risk level and then by buffer days. Includes SKU name, site, category, current stock, days of supply, buffer days, risk badge, and recommended action. Designed so a manager can scan this in one minute and know what to act on.
- **Risk Heatmap by Site** — A 3×4 grid showing the count of CRITICAL/HIGH/MEDIUM/LOW SKUs at each site. Immediately reveals whether risk is concentrated at one site or distributed across all three.
- **Supplier Health Chart** — Horizontal bar chart of all active suppliers ranked by on-time delivery rate, color-coded green/yellow/red. Incident counts annotated.

**Business value:** Replaces a 2-hour manual ERP pull with a sub-60-second morning review.

---

### 4.2 Full SKU Risk Table

**What it is:** A filterable, sortable table of all 90 SKU-site combinations with full risk detail.

**Filters available:** Site (Boston, Chicago, Seattle), Risk Level (Critical/High/Medium/Low), Category (Critical/Standard/Consumable)

**Columns:** SKU ID, SKU Name, Site, Category, Current Stock, Days of Supply, Buffer Days, Risk Level (badge), Recommended Action

**Sorting:** Default is risk level descending, then buffer days ascending. Allows managers to slice the data by their area of responsibility.

**Business value:** Gives procurement buyers and site managers their own view of the full risk picture without needing to go through the VP. Democratizes risk visibility across the organization.

---

### 4.3 AI Supply Chain Analyst (Chat)

**What it is:** A conversational interface powered by the Anthropic Claude API, grounded exclusively in live inventory and supplier data from the platform's MySQL database.

**How it works (technically, for analyst understanding):** Every time a user sends a message, the platform pulls the current risk summary, supplier health data, and recent incident history from the database and injects it into the AI's system prompt before sending the user's question. The AI is explicitly constrained to answer only from that injected data. It cannot access external information, make up numbers, or speculate beyond what the data shows.

**Suggested starter questions (shown on load):**
- "What's our biggest stockout risk right now?"
- "Which supplier should I be most concerned about?"
- "What immediate actions should I take this week?"
- "Which SKUs have both low stock and an unreliable primary supplier?"

**Action recommendation format:** When the AI identifies a risk, it ranks up to 4 possible responses:

| Action | When to use | Cost | Time to resolve |
|---|---|---|---|
| **EXPEDITE** | Critical category, buffer_days < 0 | High (air freight + premium pricing) | 1–3 days |
| **REBALANCE** | Stock exists at another site | None | 1–2 days |
| **SUBSTITUTE** | Alternate SKU available and clinically acceptable | Low | Same day |
| **STANDARD ORDER** | Buffer_days > 0 but approaching window | Normal | lead_time_days |
| **DEFER** | Non-critical item, low clinical impact | None | N/A |

**Confidence statement:** Every risk-related response ends with a confidence note explaining what the assessment is based on and what additional data would improve it.

**Conversation memory:** The chat maintains conversation history within a session, so follow-up questions work naturally ("And what about that same SKU at the Chicago site?").

**Business value:** Eliminates the analytical bottleneck. Instead of a manager needing 30+ minutes to investigate a risk, they ask a question and get a grounded, specific answer in seconds. Makes expert-level supply chain analysis accessible to the whole operations team, not just the most senior analyst.

---

### 4.4 Supplier Intelligence Layer

**What it is:** Not a standalone page in V1, but a data layer surfaced throughout the platform.

**Data maintained per supplier:**
- On-time delivery rate (rolling 12-month)
- Average lead time (vs. contracted lead time)
- Contract tier (Primary, Backup, Spot)
- Active incident count (last 12 months)
- Total days delayed across all orders
- Quality score
- Country of origin (supply concentration risk signal)
- Which SKUs they are primary supplier for

**Incident types tracked:** Late Delivery, Quality Issue, Shortage, Force Majeure, Communication Failure

**Business value:** Gives procurement buyers a systematic, data-driven supplier scorecard rather than relying on memory and informal notes. Creates an auditable record of supplier performance for contract negotiations.

---

## 5. RISK SCORING METHODOLOGY

Understanding the risk scoring logic is essential for interpreting platform outputs correctly.

### 5.1 Core Metric: Days of Supply

```
Days of Supply = Current Stock ÷ Average Daily Demand
```

This tells you how many days the current inventory will last at the current consumption rate before reaching zero.

### 5.2 Core Metric: Buffer Days

```
Buffer Days = Days of Supply − Lead Time (days)
```

This is the key metric. A positive buffer means you will receive a replenishment order before you run out. A negative buffer means — even if you order right now — you will run out before the order arrives.

Buffer Days < 0 is the definition of a CRITICAL risk: the stockout is mathematically inevitable unless an emergency action is taken.

### 5.3 Risk Classification Logic

| Risk Level | Condition | Interpretation |
|---|---|---|
| **CRITICAL** | Days of Supply ≤ Lead Time | Stockout will occur before next delivery even if ordered today |
| **HIGH** | Days of Supply ≤ Lead Time × 1.5 | Within the reorder window; must order now |
| **MEDIUM** | Days of Supply ≤ Lead Time × 2.0 | Approaching reorder window; monitor closely |
| **LOW** | Days of Supply > Lead Time × 2.0 | Healthy buffer; no action required |

### 5.4 Category Weighting in Recommendations

Risk level is the same regardless of category, but the recommended action differs:

- **Critical category items** (surgical gloves, IV catheters, sterile drapes) at CRITICAL risk → EXPEDITE is always the first recommendation. Service failure cost outweighs premium procurement cost.
- **Standard or Consumable items** at CRITICAL risk → REBALANCE or SUBSTITUTE is explored first before recommending expediting, because the service impact of a temporary shortage is lower.

### 5.5 What the Model Does Not Currently Account For (Honest Limitations)

- **Demand variability:** The model uses average daily demand, not a probabilistic demand distribution. Seasonal spikes or one-time large orders can render the days-of-supply calculation temporarily inaccurate.
- **In-transit orders:** If a purchase order is already in transit, the actual risk is lower than the score suggests. V1 does not subtract pending orders from the risk calculation.
- **Multi-echelon inventory:** The model treats each site independently. It does not currently model the cost and time of inter-site transfers dynamically.
- **Price-based prioritization:** All CRITICAL items are treated equally regardless of unit cost or revenue contribution. A $0.15 alcohol wipe and a $32 suture kit receive the same urgency level.

---

## 6. FEATURE ROADMAP — FUTURE IMPROVEMENTS

The following features represent the natural evolution of SupplyLens from a risk intelligence dashboard into a full supply chain decision platform. These are prioritized by business impact and implementation feasibility.

---

### TIER 1 — High Impact, Near-Term (V1.5)

#### 6.1 Pending Orders Integration
**Problem it solves:** Currently, if a purchase order is already in transit, the risk score does not reflect that. A CRITICAL flag on an item with a delivery arriving tomorrow is a false alarm.

**What it adds:**
- Track open POs per SKU per site (expected delivery date, quantity, supplier)
- Subtract expected inbound quantity from the risk calculation
- Show "Effective Days of Supply (incl. inbound)" alongside raw days of supply
- Flag orders from unreliable suppliers with a reliability-adjusted delivery estimate

**Business value:** Eliminates the most common false positive in the risk model. Increases operations team trust in the platform's signals.

---

#### 6.2 Probabilistic Demand Modeling
**Problem it solves:** Fixed average daily demand ignores variance. An item that averages 45 units/day but has high day-to-day variability has a higher true stockout risk than the current model captures.

**What it adds:**
- Compute demand standard deviation per SKU from orders history
- Calculate "risk-adjusted days of supply" at a chosen confidence level (e.g., 95%)
- Show both average-case and worst-case days of supply on the risk table
- Surface high-variance SKUs as a specific risk flag even if average-case risk is LOW

**Business value:** Reduces both false negatives (missing real risks) and false positives (flagging items that are actually fine). Makes the risk model defensible to CFOs and auditors.

---

#### 6.3 Rebalancing Recommendation Engine
**Problem it solves:** Currently, the AI can suggest "rebalance from sister site" conceptually, but has no visibility into whether the sister site actually has surplus to spare.

**What it adds:**
- For every CRITICAL or HIGH risk SKU, check if another site has LOW risk for the same SKU
- Compute transferable surplus: how much stock the donor site can give without itself becoming HIGH risk
- Surface specific rebalancing recommendations: "Transfer 200 units of SKU004 from Seattle to Boston — Seattle drops from LOW to MEDIUM; Boston recovers to LOW"
- Estimate transfer time and cost

**Business value:** Turns the platform from a risk detection tool into an active optimization tool. Directly reduces emergency procurement spend by maximizing use of existing inventory.

---

#### 6.4 Email / Slack Alert Integration
**Problem it solves:** The platform currently requires a manager to actively open it to see risks. Critical risks may not be noticed until the morning dashboard review.

**What it adds:**
- Daily digest email: summarizes CRITICAL and HIGH risks across all sites, sent at 7am
- Real-time Slack notification when any SKU transitions to CRITICAL risk
- Configurable alert thresholds per user role (site managers only receive their site)
- Weekly supplier scorecard email for procurement buyers

**Business value:** Pushes risk to managers rather than requiring them to pull it. Extends the platform's value to users who may not open the dashboard daily.

---

### TIER 2 — High Impact, Medium-Term (V2.0)

#### 6.5 Demand Forecasting Layer
**Problem it solves:** The current model is static — it uses historical average demand to project forward. It cannot anticipate demand changes driven by seasonality, hospital census changes, or known upcoming events (scheduled surgeries, seasonal illness trends).

**What it adds:**
- Time-series demand forecasting per SKU using historical orders (ARIMA or Prophet model)
- 30/60/90-day demand projections per SKU per site
- "Forecast-adjusted days of supply" incorporating predicted demand changes
- Seasonal pattern detection and flagging ("This SKU peaks 40% in December")

**Business value:** Shifts the platform from reactive (responding to current risk) to predictive (anticipating future risk weeks in advance). This is the capability gap that separates best-in-class supply chain operations from average ones.

---

#### 6.6 Supplier Risk Scoring (Composite Score)
**Problem it solves:** Currently, supplier health is shown as separate metrics (on-time rate, incident count, lead time). There is no single composite score that enables quick comparison.

**What it adds:**
- Weighted composite supplier risk score (0–100) incorporating:
  - On-time delivery rate (40% weight)
  - Incident frequency and severity (30% weight)
  - Lead time consistency (20% weight)
  - Country of origin concentration risk (10% weight)
- Trend line: is the supplier getting better or worse over time?
- Automatic flag when a supplier's score drops below a configurable threshold
- Side-by-side supplier comparison for specific SKUs

**Business value:** Gives procurement buyers a defensible, quantitative basis for supplier selection and contract negotiation. Reduces reliance on subjective relationship-based assessments.

---

#### 6.7 Cost Impact Estimation
**Problem it solves:** Risk flags currently show operational severity (days of supply, buffer) but not financial severity. A CRITICAL flag on a $0.15 alcohol wipe is qualitatively different from a CRITICAL flag on a $32 suture kit, but the platform treats them identically.

**What it adds:**
- Estimated cost of stockout per SKU: emergency procurement premium + expediting cost + service failure penalty (configurable)
- Estimated cost of recommended action: expedite cost, rebalancing logistics cost
- ROI of acting now vs. deferring: how much does waiting one week increase expected cost?
- Weekly/monthly "avoided cost" summary: value the platform generated by enabling proactive action

**Business value:** Translates operational risk into financial risk — the language of executive stakeholders. Enables prioritization by financial impact rather than just operational severity. Creates a quantifiable ROI story for the platform itself.

---

#### 6.8 Multi-Echelon Inventory View
**Problem it solves:** Sites are currently analyzed independently. The platform does not model the supply network as a whole — it cannot see that a shortage at Boston is best solved by a transfer from Chicago, which in turn could be replenished from a supplier more quickly than a direct Boston order.

**What it adds:**
- Network-wide inventory view showing total stock across all sites per SKU
- Dynamic safety stock recommendations per site based on service level targets and demand variability
- Network rebalancing optimizer: given current stock distribution, what set of transfers minimizes total stockout risk at minimum transfer cost?

**Business value:** Moves from site-level optimization to network-level optimization — the approach used by best-in-class distributors. Reduces total inventory investment while improving service levels.

---

### TIER 3 — Strategic, Long-Term (V3.0)

#### 6.9 ERP / WMS Integration Connectors
**Problem it solves:** Currently, SupplyLens uses synthetic data and would require manual CSV uploads or API integration to pull from real ERP systems in a production deployment.

**What it adds:**
- Pre-built connectors for common ERP/WMS platforms (SAP, Oracle NetSuite, Microsoft Dynamics)
- Real-time inventory snapshot sync (every 15 minutes)
- Automatic orders history ingestion from purchasing module
- Supplier data sync from vendor management module

**Business value:** Makes the platform deployable in a real enterprise environment without manual data maintenance. This is the feature that converts a compelling demo into a production-ready SaaS product.

---

#### 6.10 Disruption Intelligence Feed
**Problem it solves:** External disruptions (port strikes, weather events, geopolitical incidents, supplier financial distress) are not currently visible in the platform. A supplier may look healthy on historical metrics while a major disruption is actively unfolding.

**What it adds:**
- Integration with external risk intelligence feeds (e.g., Riskmethods, Resilinc, or public APIs)
- Automatic flagging when a disruption event is detected that affects a primary supplier's country or port
- AI synthesis: "Warning: A port disruption at Rotterdam may affect SUP003 (EuroMed GmbH). 3 of your CRITICAL SKUs rely on this supplier. Recommended action: trigger backup supplier orders for SKU006, SKU025, SKU026."

**Business value:** The most advanced supply chain risk platforms in the world (used by Apple, Toyota, Johnson & Johnson) all have external disruption monitoring. This feature is what separates a risk dashboard from a genuine risk intelligence platform.

---

#### 6.11 Scenario Planning Tool
**Problem it solves:** Operations managers currently have no way to model "what if" scenarios before committing to a decision. They must estimate the impact of actions mentally.

**What it adds:**
- "What if demand increases 20% next month?" → shows which SKUs would move to CRITICAL
- "What if SUP002 delivers 10 days late?" → shows downstream impact on all affected SKUs
- "What if we transfer 500 units of SKU004 from Seattle to Boston?" → shows new risk profile for both sites
- Side-by-side scenario comparison

**Business value:** Enables proactive planning rather than reactive decision-making. Particularly valuable for operations managers preparing for known demand spikes (flu season, major procedure campaigns) or known supply risks (supplier contract renewal, geopolitical instability).

---

## 7. SUCCESS METRICS

### 7.1 Operational Metrics (what the platform tracks)
- Number of CRITICAL risk SKUs at start of each day (target: trending down)
- Average time between CRITICAL flag and action taken (target: < 4 hours)
- Stockout incidents per quarter (target: 0 for Critical category items)
- Emergency procurement orders as % of total orders (target: < 5%)
- Supplier incident response time (target: same-day acknowledgment)

### 7.2 Platform Adoption Metrics (for a commercial product)
- Daily active users per site
- AI chat queries per day (signals active engagement, not passive dashboard viewing)
- Average session duration
- % of CRITICAL flags that result in a documented action within 24 hours

### 7.3 Business Impact Metrics (for executive reporting)
- Emergency procurement cost savings vs. prior period baseline
- Reduction in carrying cost from overstocking (as confidence in risk visibility improves)
- Service level agreement compliance rate
- Avoided stockout cost (estimated based on avoided emergency orders)

---

## 8. COMPETITIVE LANDSCAPE

### 8.1 Current Market Reality

The supply chain risk intelligence market has two clusters: enterprise platforms (Blue Yonder, o9 Solutions, Kinaxis) that cost $500K–$5M+ annually and require 12–18 month implementation cycles, and commodity BI tools (Tableau, Power BI) that show data but provide no decisioning support. The middle market — distributors with $50M–$500M in revenue — is significantly underserved. They cannot afford enterprise platforms but have grown beyond what Excel can handle.

### 8.2 How SupplyLens Fits

SupplyLens is designed for the underserved middle market. Its competitive positioning:

| Dimension | Enterprise Platforms | BI Dashboards | SupplyLens |
|---|---|---|---|
| **Cost** | $500K–$5M/yr | $10K–$50K/yr | Low (SaaS) |
| **Implementation time** | 12–18 months | 2–4 months | Days |
| **AI decision support** | Yes (complex) | No | Yes (grounded, simple) |
| **Domain specificity** | Generic supply chain | Generic analytics | Medical device dist. |
| **ERP integration** | Deep | Moderate | Roadmap |
| **Accessibility** | Expert users only | Analyst users | All operations staff |

### 8.3 The Differentiation That Matters

SupplyLens's core differentiation is not the AI interface — it is the grounding architecture. Every competitor with an AI interface risks hallucination: the model generates plausible-sounding recommendations that are not grounded in the company's actual data. SupplyLens's data-injection approach constrains the AI to reason only over real operational data, making its outputs trustworthy in a domain where bad recommendations have clinical consequences.

---

## 9. PROJECT NARRATIVE (FOR INTERVIEWS & PORTFOLIO)

### 9.1 The Origin Story

SupplyLens was built as a direct extension of hands-on supply chain consulting work at the Boeing Center for Supply Chain Innovation, where the underlying decision logic — demand forecasting, risk scoring, supplier reliability weighting, action prioritization — was built manually in Excel for Fortune 500 clients including Hunter Engineering and Bunge Global. The limitation of that approach was always the same: the analytical framework was sound, but the delivery mechanism (a spreadsheet) required expert knowledge to operate, was updated weekly at best, and could not synthesize supplier context at the point of decision.

SupplyLens asks: what does that same analytical framework look like when it's productized? When the risk computation runs continuously rather than weekly? When the supplier context is connected to the inventory data? When a procurement buyer can ask a natural language question and get the same answer that an experienced supply chain analyst would give — in seconds, not hours?

### 9.2 Key Design Decisions Worth Discussing in Interviews

**Why medical device distribution?**
High stakes create meaningful risk tiers. A CRITICAL flag on a surgical item is genuinely different from a CRITICAL flag on a consumable — and that distinction is baked into the recommendation logic. The domain also maps directly to prior Boeing Center work, giving the design decisions real-world grounding.

**Why ground the AI rather than use it generatively?**
Supply chain decisions have consequences. A hallucinated supplier recommendation or an invented stockout projection is worse than no recommendation at all. The grounding architecture was a deliberate product decision to prioritize trustworthiness over capability breadth.

**Why risk level tiers rather than a continuous score?**
Operations managers need to make binary decisions: act or don't act. A continuous score (e.g., 73 out of 100) creates ambiguity about where the action threshold is. Four discrete tiers with clear meanings (CRITICAL = act now, HIGH = act today, MEDIUM = monitor, LOW = nothing needed) enable faster, more consistent decision-making across a team.

**Why not build this on a cloud data warehouse (BigQuery, Snowflake)?**
For V1 at demo scale with 30 SKUs and 3 sites, MySQL is the right tool. The architecture is designed to be database-agnostic — the query logic in `database.py` would work with minor modifications against any SQL-compatible data store. Introducing BigQuery would add cost, complexity, and a 2-week learning curve without meaningfully improving the demo's ability to demonstrate the core product thesis.

---

## 10. GLOSSARY

| Term | Definition |
|---|---|
| **SKU** | Stock Keeping Unit — a unique identifier for a specific product at a specific specification |
| **Days of Supply** | How many days current inventory will last at current consumption rate |
| **Buffer Days** | Days of supply minus lead time — negative means stockout is inevitable without emergency action |
| **Lead Time** | Days from placing a purchase order to receiving delivery |
| **Reorder Point** | Inventory level at which a standard purchase order should be triggered |
| **On-Time Delivery Rate** | % of orders from a supplier that arrived on or before the expected delivery date |
| **Contract Tier** | The role a supplier plays: Primary (preferred, first choice), Backup (second choice), Spot (emergency only) |
| **Expedite** | Place an emergency order with air freight or premium pricing to accelerate delivery |
| **Rebalance** | Transfer existing stock from a low-risk site to a high-risk site |
| **Substitute** | Use a clinically acceptable alternate SKU to cover a shortage of the primary SKU |
| **CRITICAL category item** | A medical supply item whose stockout could directly impact clinical procedures |
| **Force Majeure** | A supplier disruption caused by events outside the supplier's control (natural disaster, war, pandemic) |
| **Safety Stock** | Buffer inventory held above the reorder point to absorb demand variability and lead time variability |
