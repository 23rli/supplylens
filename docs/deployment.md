# Deployment

SupplyLens ships with Docker support for both the backend and frontend, plus a
`docker-compose.yml` that wires them together. For local development you usually
don't need any of this — see [Getting Started](getting-started.md). Use this guide
when you want a production-style deployment.

---

## Option 1 — Docker Compose (recommended)

From the project root:

```bash
docker compose up --build
```

This builds and runs two services:

| Service | Image | Port |
|---|---|---|
| `backend` | FastAPI + uvicorn | internal `8000` |
| `frontend` | Vite build served by nginx | `8080` → host |

Then open <http://localhost:8080>. The nginx frontend reverse-proxies `/api/*` to
the backend, so the browser talks to a single origin (no CORS issues).

### Before you deploy

1. Provide `backend/.env` (compose loads it via `env_file`). At minimum set a strong
   `JWT_SECRET` and `ENV=production`. For Azure SQL, set `DB_BACKEND=azure` and the
   `AZURE_SQL_*` values. See [Configuration](configuration.md).
2. The backend image already includes ODBC Driver 18, so `pyodbc` / Azure SQL works
   out of the box.

---

## Option 2 — Build the images individually

### Backend

```bash
cd backend
docker build -t supplylens-backend .
docker run --env-file .env -p 8000:8000 supplylens-backend
```

The image is based on `python:3.11-slim`, installs ODBC Driver 18 for Azure SQL,
and starts `uvicorn main:app` on port 8000.

### Frontend

```bash
cd frontend
docker build -t supplylens-frontend .
docker run -p 8080:80 supplylens-frontend
```

This is a multi-stage build: Node builds the static site, then `nginx:alpine` serves
it with SPA routing and the `/api` reverse proxy (`frontend/nginx.conf`).

---

## Option 3 — Run without Docker (bare metal / VM)

**Backend**
```bash
cd backend
pip install -r requirements.txt
# set environment variables / .env for production
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Frontend**
```bash
cd frontend
npm ci
npm run build           # outputs to frontend/dist
# serve frontend/dist with any static host (nginx, Caddy, S3+CloudFront, ...)
```

> `prophet` is optional and **not** installed by `requirements.txt` (the numpy
> forecast fallback is used otherwise). Install it separately only if you want
> Prophet-based forecasting.

---

## Production setup with Azure SQL

1. Create the schema: run `backend/schema.sql` against your Azure SQL database.
2. Load data: put your CSVs in `backend/data/` and run `python data/import_data.py`
   (see [Using Your Own Data → Method C](data-guide.md#method-c--load-csvs-into-azure-sql-production)).
3. Set `DB_BACKEND=azure` and the `AZURE_SQL_*` credentials in the backend
   environment.

---

## Production hardening checklist

- [ ] Strong, unique `JWT_SECRET` (and `ENV=production` to enforce it)
- [ ] `ALLOWED_ORIGINS` locked to your real domain(s)
- [ ] HTTPS terminated at your load balancer / reverse proxy
- [ ] `RATE_LIMIT_PER_MIN` tuned for expected traffic
- [ ] Database backups configured (Azure SQL automated backups)
- [ ] Secrets injected via your platform's secret manager, not committed to git
- [ ] Run the test suite in CI: `cd backend && python -m pytest -q`
</content>
