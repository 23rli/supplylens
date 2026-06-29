# SupplyLens

Supply Chain Risk Intelligence Platform for medical device distribution. SKU-level stockout risk, supplier reliability scores, and an AI analyst (Claude) grounded on live MySQL data.

## Stack
- **Backend:** FastAPI + MySQL + Anthropic Claude
- **Frontend:** React 18 (Vite) + Tailwind CSS + Recharts

## Setup

### 1. Database
```bash
mysql -u root -p < backend/schema.sql
```

### 2. Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # fill in ANTHROPIC_API_KEY and MySQL credentials
uvicorn main:app --reload --port 8000
```

### 3. Seed data (first time)
```bash
cd backend/data
python seed_data.py     # generates CSVs
python import_data.py    # imports into MySQL
```

### 4. Frontend
```bash
cd frontend
npm install
npm run dev              # http://localhost:5173
```

Health check: `curl http://localhost:8000/api/dashboard-stats`
