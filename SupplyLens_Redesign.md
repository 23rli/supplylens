# SupplyLens Product Redesign

## Product Vision

- Shift from a dashboard and chatbot-centric product toward a comprehensive Decision Engine.
- Structure the product around a Detect → Decide → Execute → Learn loop.
- Four pillars:
  - Detect: Automated, proactive risk scoring, alerts, and daily briefings.
  - Decide: Leverage ranked actions with added financial impact and confidence/probability.
  - Execute: Introduce execution capabilities (create PO, transfer stock, contact suppliers, assign owners).
  - Learn: Track outcomes, refine recommendations, incorporate supplier performance feedback loops.
- Position the platform as an operational system that executes fixes and aligns with automation, outcomes, and ROI.

## Core Workflows

### Morning Ops Review

- Users log in to see today's Risk Briefing in under 60 seconds.
- Highlight key risks:
  - CRITICAL, HIGH risk items requiring action or monitoring.
  - Early warnings on supplier degradation.
- Example: "3 CRITICAL risks action needed in < 48 hrs, 5 HIGH risks to monitor or act, 1 supplier degrading."
- Display impact in dollar terms and recommended actions with one-click actions.

### Fix Problem

- Clicking a CRITICAL SKU reveals a Decision Panel:
  - **Left:** Inventory context, demand, lead time, supplier stats.
  - **Center:** Visualization of Days of Supply vs. Lead Time and network map.
  - **Right:** Ranked actions (rebalance, expedite, substitute) with cost, benefit, and execute button.
- Example: Rebalance from Chicago (saves $180k), expedite cost $2.4k, substitute SKU with clinical tradeoffs.

### Rebalance Network

- Show a network graph of sites (Boston, Chicago, Seattle) with imbalances.
- Suggest stock transfers (e.g., move 120 units from Chicago to Boston reduces global risk by 38%).

### Ask AI

- AI decision support for explanations and simulations:
  - Provide clarity on why a risk is high.
  - Model scenarios: What happens if we do nothing? Cheapest fix? Worst-case scenario.
- Evolve AI analyst from reactive chat to proactive alerts and briefings.

## UX / UI Layout

### Navigation

- **Left Nav:** Today (default), Risks, Network, Suppliers, Forecasting Actions (NEW), AI Analyst.

### Screen 1: Today

- Replaces current dashboard.
- Top section: 3 CRITICAL risks cards (e.g., SKU: Surgical Gloves, Site: Boston, Risk: CRITICAL, Time to stockout) with action buttons.

### Screen 2: Risks

- Existing risk table with added columns: impact, probability, recommended actions inline.
- Filters to show actionable risks for the week.

### Screen 3: Decision View

- Split into three panels:
  - **Left:** Context (inventory, demand, lead time, supplier stats).
  - **Center:** Visualization (days of supply vs lead time chart, network map).
  - **Right:** Ranked actions list with cost/benefit and execute button.

### Screen 4: Actions

- New module for tracking pending and executed actions and their outcomes.
- Example: Expedite PO #123 (arriving in 2 days), transfer progress.

## Technical Architecture

### Backend Stack

- **Base:** FastAPI + Azure SQL Database (pyodbc) + Azure OpenAI.
- **Frontend:** React 18 (Vite) + Tailwind CSS + Recharts.
- **Local Dev:** SQLite with backend DB_BACKEND environment variable selecting SQLite or Azure.

### New Backend Layers and Services

- Add decision engine layer:
  - `risk_engine.py` for core risk scoring.
  - `decision_engine.py` for recommended actions logic.
  - `execution_engine.py` for execution stubs.
- Execution stubs simulate PO creation, transfers, supplier communication, logging to DB.

### Database Enhancements

- New tables:
  - `actions` (pending and executed actions).
  - `action_status` (status of each action).
  - `decision_logs` (audit trail).
- Enables traceability, compliance, and learning loops.

### AI Layer Upgrade

- Raw chat endpoint enhanced to inject decision context.
- Structured queries and explanations.
- `explain_decision(sku, site)` endpoint.
- `simulate_no_action` endpoint for scenario analysis.

### Frontend Enhancements

- Move from static pages to stateful workflows.
- Use React Query for optimistic updates on actions.
- Provide interactive network maps and visualizations.

## API Design

### Endpoints (examples)

- `GET /api/dashboard-stats`: Headline KPIs for the Today page.
- `GET /api/top-risks?limit=10`: Returns highest-risk SKUs.
- `GET /api/risk-summary?site={}&level={}`: Returns risk table filtered by site and level.
- `GET /api/risk-by-site`: Risk counts per site.
- `GET /api/heatmap`: Site risk heatmap.
- `GET /api/suppliers/on-time`: On-time rates and incident counts.
- `POST /api/chat`: Chat endpoint for AI Analyst.
- `GET /api/explain-decision?sku={}&site={}`: Returns explanation for decision drivers.
- `POST /api/actions/create-po`: Executes PO creation stub.
- `POST /api/actions/transfer`: Executes stock transfer stub.
- `GET /api/actions/status`: Fetch current status of actions.

## Roadmap and Prioritization

### V1.5 (2-3 Weeks)

- Implement Today page with briefing.
- Decision Panel redesign with action execute logging (fake execution).
- Track actions in Actions module.
- Add basic financial impact display ($ at risk, cost vs benefit).

### V2 (4-6 Weeks)

- Real execution flows (PO creation, export formats).
- Introduce probability-based risk scoring with demand variance (safety stock logic, stockout probability).
- Network rebalancing suggestions.
- Proactive alerts and briefings.

### V3 (Broader Scope)

- ERP integrations with SAP, Oracle, NetSuite connectors.
- Supplier intelligence network for cross-customer benchmarks and predictive risk signals (port delays, supplier disruptions).
- Decision logs, approval workflows, recall linkage for regulated medical device distribution compliance.
- Advanced AI and learning loops to refine recommendations continually.

## Positioning and GTM

- Redefine SupplyLens as a risk intelligence platform with execution capabilities, not just visibility.
- Emphasize AI copilot role: prevents stockouts, executes fixes before too late, aligns with ROI and revenue protection.
- Target enterprise and regulated buyers with compliance and audit trail features.

## Summary

- Focus on sharp redesign rather than incremental features.
- Build the Action → Execution bridge and embed financial reasoning.
- Prioritize usability: reduce ERP pull time from 2 hours to <60 seconds review.
- Embrace proactive AI and explainability to build trust.
- Create a platform moat via integrations, compliance, and supplier intelligence.
