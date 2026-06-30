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
The platform runs entirely on SQLite with a deterministic AI fallback.

```bash
# 1. Backend
cd backend
pip install fastapi uvicorn python-dotenv pydantic numpy openpyxl python-multipart PyJWT
python data/seed_risk.py        # commodity/manufacturing risk + decision data
python inventory/seed_parts.py  # 120 sample parts
python data/seed_users.py       # demo login
uvicorn main:app --reload --port 8000

# 2. Frontend (new terminal)
cd frontend
npm install
npm run dev                     # http://localhost:5173
```

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

## Production (Azure)
Set `DB_BACKEND=azure` and provide Azure SQL credentials in `.env`, then run `backend/schema.sql` against the database and `python data/import_data.py` to load CSVs. Install `pyodbc` (needs ODBC Driver 18) and `openai`. Lock CORS via `ALLOWED_ORIGINS` and set a strong `JWT_SECRET`.

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
