# SupplyLens

Supply Chain Risk Intelligence Platform for medical device distribution. SKU-level stockout risk, supplier reliability scores, and an AI analyst grounded on live data — powered by **Azure SQL Database** and **Azure OpenAI**.

The AI layer never answers from general knowledge alone: every chat request pulls live inventory, supplier, and incident data from Azure SQL and injects it into the system prompt before calling Azure OpenAI.

## Stack
- **Backend:** FastAPI + Azure SQL Database (pyodbc) + Azure OpenAI
- **Frontend:** React 18 (Vite) + Tailwind CSS + Recharts
- **Domain:** 3 sites (Boston, Chicago, Seattle), 30 SKUs, 8 suppliers

## Prerequisites
- Python 3.11+
- Node.js 18+
- [ODBC Driver 18 for SQL Server](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)
- An Azure SQL Database instance
- An Azure OpenAI resource with a deployed model (e.g. `gpt-4o`)

## Setup

### 1. Database — Azure SQL
Create the schema against your Azure SQL Database (server admin login):
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
