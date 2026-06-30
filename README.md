# SupplyLens

**AI-powered supply-chain risk intelligence for commodity & manufacturing operations.**

SupplyLens is a decision-support platform - not a general chatbot - that consolidates inventory, supplier performance, demand forecasts, and commodity prices into one control tower, then layers an AI analyst that explains risk and recommends ranked, executable actions, grounded exclusively in live operational data.

It shifts supply-chain management from **reactive** (discover stockouts after they happen) to **proactive** (surface and resolve risk before the lead-time window closes), across plants in Boston, Chicago, and Seattle.

## Modules
- **Today** - daily AI risk briefing, top critical items, one-click resolve, and a natural-language "Ask AI" box.
- **Risk Intelligence** - SKU stockout risk scoring + supplier reliability, heatmap, and a filterable SKU table.
- **Inventory Engine** - 52-week over/understock simulation, worst-offender lists, warehouse pallet load, demand forecasting with seasonality, and CSV/XLSX part import.
- **Hedging Planner** - commodity procurement: front-loaded vs systematic strategies, forecast-fed pricing, hedged-vs-spot, and an "Amount Saved" KPI.
- **Actions** - tracked, tenant-scoped log of executed POs and stock transfers.
- **AI Analyst** - grounded chat across every module's live data.

## How the AI works
Every AI call injects the live database state into the model prompt, so answers are computed from real inventory/supplier data and never hallucinated. It uses **Azure OpenAI (gpt-5-mini)** when configured, and falls back to deterministic logic when not - so the app always works. Responses are cached briefly and run at `reasoning_effort=minimal` for sub-3-second latency.

## Risk scoring
- **Days of Supply** = Current Stock / Avg Daily Demand
- **Buffer Days** = Days of Supply - Lead Time (negative = stockout is inevitable without emergency action)

| Risk | Condition | Meaning |
|---|---|---|
| CRITICAL | Days of Supply <= Lead Time | Stockout before next delivery |
| HIGH | <= Lead Time x 1.5 | Must order now |
| MEDIUM | <= Lead Time x 2.0 | Monitor closely |
| LOW | > Lead Time x 2.0 | Healthy buffer |

## Stack
- **Backend:** FastAPI, SQLite (local) / Azure SQL (prod), Azure OpenAI, JWT auth
- **Frontend:** React 18 (Vite) + Tailwind CSS + Recharts
- **Security:** JWT login, per-tenant data scoping, env-driven CORS allow-list, per-IP rate limiting

## Quick start (local, no Azure required)

Anyone can run the full app in about 5 minutes. You only need **Python 3.11+** and
**Node.js 18+** installed. No cloud account, database server, or paid service is
required — it runs on a local SQLite file, and the AI features fall back to built-in
logic when no AI key is present.

> New to the project? Follow the step-by-step [Getting Started guide](docs/getting-started.md).

```bash
# 1. Backend — open a terminal
cd backend
pip install fastapi uvicorn python-dotenv pydantic numpy openpyxl python-multipart PyJWT
python data/seed_risk.py        # supplier + SKU risk data
python inventory/seed_parts.py  # 120 sample parts
python data/seed_users.py       # creates the demo login
uvicorn main:app --reload --port 8000

# 2. Frontend — open a SECOND terminal (leave the backend running)
cd frontend
npm install
npm run dev                     # opens http://localhost:5173
```

Open <http://localhost:5173> and log in:

**Demo login:** `admin@supplylens.io` / `demo1234`

### Optional: enable live AI
Create `backend/.env` from `.env.example` and set your Azure OpenAI values:
```
AZURE_OPENAI_ENDPOINT=https://<resource>.services.ai.azure.com
AZURE_OPENAI_API_KEY=<key>
AZURE_OPENAI_DEPLOYMENT=gpt-5-mini
AZURE_OPENAI_API_VERSION=preview
```
Without a key, the AI features degrade gracefully to deterministic summaries.

## Use your own data

SupplyLens comes preloaded with realistic sample data. To load **your** suppliers,
inventory, and parts, there are three ways — full details in the
**[Using Your Own Data guide](docs/data-guide.md)**:

1. **Import a file (no code)** — go to **Inventory → Parts → Import** and upload a
   CSV or XLSX of your parts master. The 52-week simulation recalculates instantly.
2. **Edit the seed scripts** — change the `SUPPLIERS` / `SKUS` lists in
   [backend/data/seed_risk.py](backend/data/seed_risk.py) (and the login in
   [backend/data/seed_users.py](backend/data/seed_users.py)), then re-run them.
3. **Load CSVs into Azure SQL** — drop your CSVs in `backend/data/` and run
   `python data/import_data.py` for production.

The parts import expects these columns (only `part_number` is required):
`part_number, description, vendor, vendor_name, lead_time_weeks, abc_group, on_hand,
on_order, forecast, last_year_usage, unit_price, product_per_case, cases_per_pallet,
eoq, safety_stock`.

## Documentation

Full docs live in [`docs/`](docs/README.md):

| Guide | What it covers |
|---|---|
| [Getting Started](docs/getting-started.md) | Install & run locally in ~5 minutes |
| [Features & Purpose](docs/features.md) | What each screen does and why |
| [Using Your Own Data](docs/data-guide.md) | Load your own suppliers, inventory, parts |
| [Architecture](docs/architecture.md) | How it fits together + AI grounding |
| [API Reference](docs/api-reference.md) | Every HTTP endpoint |
| [Configuration](docs/configuration.md) | Every environment variable |
| [Deployment](docs/deployment.md) | Docker & Azure production setup |

## Production (Azure)
Set `DB_BACKEND=azure` and provide Azure SQL credentials in `.env`, then run `backend/schema.sql` against the database and `python data/import_data.py` to load CSVs. Install `pyodbc` (needs ODBC Driver 18) and `openai`. Lock CORS via `ALLOWED_ORIGINS` and set a strong `JWT_SECRET`. See the [Deployment guide](docs/deployment.md) for Docker Compose.


## Configuration (`backend/.env`)
| Var | Purpose |
|---|---|
| `DB_BACKEND` | `sqlite` (default) or `azure` |
| `JWT_SECRET` / `JWT_TTL_HOURS` | Auth token signing + lifetime |
| `AZURE_OPENAI_*` | Live AI (optional) |
| `AZURE_OPENAI_REASONING_EFFORT` | `minimal` (fast) .. `high` |
| `ALLOWED_ORIGINS` | Comma-separated CORS allow-list |
| `RATE_LIMIT_PER_MIN` | Per-IP request cap (default 240) |

## Testing
```bash
cd backend && python -m pytest -q     # 23 tests: engines, AI fallback, auth
```

## Key API endpoints
All `/api/*` data routes require a bearer token (`POST /api/auth/login`).
- `GET /api/today` - daily risk summary
- `GET /api/ai/briefing` / `POST /api/ai/ask` / `GET /api/ai/explain` - AI copilot
- `GET /api/risk-summary` / `top-risks` / `risk-by-site` / `suppliers` - risk intelligence
- `GET /api/inventory/parts` / `part/{id}` / `part/{id}/demand` / `worst` - inventory engine
- `GET /api/hedging/scenario` / `forecast` - hedging planner
- `POST /api/actions/create-po` / `transfer` ; `GET /api/actions/status` - execution
