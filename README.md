# SupplyLens

**Supply Chain Risk Intelligence Platform for medical device distribution.**

SupplyLens is a decision-support system — not a general chatbot — that consolidates inventory, supplier performance, and incident history into one control tower, and layers an AI analyst on top that answers operational questions and recommends ranked actions, grounded exclusively in live operational data.

A stockout of surgical gloves, IV catheters, or sterile drapes doesn't just lose a sale — it delays procedures and damages hospital relationships worth millions. SupplyLens shifts risk management from **reactive** (discover stockouts after they happen) to **proactive** (surface risk before the lead-time window closes).

## Who it's for
- **Operations Manager** — morning dashboard showing exactly what needs attention today; cuts a 2-hour ERP pull to a sub-60-second review.
- **Procurement Buyer** — supplier health and incident history at the point of decision; fewer reactive emergency orders.
- **Site Manager** — site-filtered risk view and rebalancing questions ("what can I pull from Chicago to cover Boston this week?").

## What it does
1. **Risk synthesis** — multi-dimensional CRITICAL/HIGH/MEDIUM/LOW score per SKU per site from stock, demand, lead time, criticality, and supplier reliability.
2. **Supplier intelligence** — live on-time rates, lead times, contract tier, and 12-month incident history surfaced at the point of decision.
3. **AI decision support** — every chat query injects live data into the prompt, so answers are computed from real inventory state, never hallucinated. Recommendations are ranked: EXPEDITE / REBALANCE / SUBSTITUTE / STANDARD ORDER / DEFER.

## Risk scoring
- **Days of Supply** = Current Stock ÷ Avg Daily Demand
- **Buffer Days** = Days of Supply − Lead Time (negative = stockout is inevitable without emergency action)

| Risk | Condition | Meaning |
|---|---|---|
| CRITICAL | Days of Supply ≤ Lead Time | Stockout before next delivery |
| HIGH | ≤ Lead Time × 1.5 | Must order now |
| MEDIUM | ≤ Lead Time × 2.0 | Monitor closely |
| LOW | > Lead Time × 2.0 | Healthy buffer |

## Stack
- **Backend:** FastAPI + Azure SQL Database (pyodbc) + Azure OpenAI
- **Frontend:** React 18 (Vite) + Tailwind CSS + Recharts
- **Domain:** 3 sites (Boston, Chicago, Seattle), 30 SKUs, 8 suppliers

## Modules
- **Inventory Engine** — 52-week over/understock simulation (~2,500 parts), worst-offender action lists, warehouse pallet load, CSV/XLSX part import. (`/inventory`)
- **Hedging Planner** — commodity procurement: hedged vs spot-only, strategy split, Amount Saved KPI, Prophet-style price forecast. (`/hedging`)
- **Risk** — SKU stockout risk + supplier reliability for medical-device distribution. (`/dashboard`)
- **AI Analyst** — grounded across all modules' live data. (`/chat`)

## Forecasting
The hedging price forecaster (per A9) uses **Prophet** when installed; otherwise a numpy trend + yearly/quarterly seasonality fallback with IQR outlier removal — same monthly first/avg/max/min interface. Prophet is optional (heavy build; skip on ARM64).

## Local dev (no Azure required)
SQLite runs the platform out of the box: `DB_BACKEND=sqlite` (default). Seed parts with `python backend/inventory/seed_parts.py`. Set `DB_BACKEND=azure` for production.

## Prerequisites
- Python 3.11+ · Node.js 18+
- [ODBC Driver 18 for SQL Server](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)
- An Azure SQL Database instance
- An Azure OpenAI resource with a deployed model (e.g. `gpt-4o`)

## Setup

### 1. Database — Azure SQL
```bash
sqlcmd -S your-server.database.windows.net -d supplylens -U <admin> -P <password> -i backend/schema.sql
```

### 2. Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # fill in Azure SQL + Azure OpenAI values
uvicorn main:app --reload --port 8000
```

### 3. Seed data (first time)
```bash
cd backend/data
python seed_data.py     # generates CSVs
python import_data.py   # imports into Azure SQL
```

### 4. Frontend
```bash
cd frontend
npm install
npm run dev             # http://localhost:5173
```

## Environment variables (`backend/.env`)
```
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_azure_openai_key_here
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_API_VERSION=2024-06-01

# Azure SQL Database
AZURE_SQL_SERVER=your-server.database.windows.net
AZURE_SQL_DATABASE=supplylens
AZURE_SQL_USER=your_admin_user
AZURE_SQL_PASSWORD=your_password
AZURE_SQL_DRIVER=ODBC Driver 18 for SQL Server
```

The frontend reads `VITE_API_URL` from `frontend/.env.local` (defaults to `http://localhost:8000/api`).

## API endpoints
- `GET /api/dashboard-stats` — headline KPIs
- `GET /api/top-risks?limit=10` — highest-risk SKUs
- `GET /api/risk-summary?site=&risk_level=&category=` — full SKU risk table
- `GET /api/risk-by-site` — risk counts per site (heatmap)
- `GET /api/suppliers` — suppliers with on-time rates and incident counts
- `GET /api/incidents?supplier_id=` — supplier incidents
- `POST /api/chat` — AI analyst, grounded on live data

Health check: `curl http://localhost:8000/api/dashboard-stats`

## Known V1 limitations
- Uses average demand (no variance/seasonality), ignores in-transit POs, treats sites independently, and prioritizes by operational severity not cost. See the business doc for the V1.5–V3 roadmap.
