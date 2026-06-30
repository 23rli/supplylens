# Configuration

All backend configuration is read from environment variables, typically placed in
`backend/.env`. Copy the template to get started:

```bash
cd backend
cp .env.example .env      # Windows: copy .env.example .env
```

The app runs with **zero configuration** out of the box (SQLite + deterministic AI
fallback). Everything below is optional until you go to production or enable live AI.

---

## Database

| Variable | Default | Purpose |
|---|---|---|
| `DB_BACKEND` | `sqlite` | `sqlite` for local, `azure` for Azure SQL |
| `SQLITE_PATH` | `backend/supplylens.db` | Location of the local database file |
| `AZURE_SQL_SERVER` | — | Azure SQL server host (when `DB_BACKEND=azure`) |
| `AZURE_SQL_DATABASE` | `supplylens` | Database name |
| `AZURE_SQL_USER` | — | SQL admin user |
| `AZURE_SQL_PASSWORD` | — | SQL admin password |
| `AZURE_SQL_DRIVER` | `ODBC Driver 18 for SQL Server` | ODBC driver name |

---

## Authentication

| Variable | Default | Purpose |
|---|---|---|
| `JWT_SECRET` | `dev-insecure-change-me` | Token signing key — **must** be a long random string in production |
| `JWT_TTL_HOURS` | `12` | Token lifetime in hours |
| `ENV` | — | Set to `production` to enforce the `JWT_SECRET` guard (app refuses to start with the default secret) |

> Generate a strong secret, e.g. `python -c "import secrets; print(secrets.token_urlsafe(48))"`.

---

## AI (Azure OpenAI)

Leave these unset to run with the deterministic fallback. Set them to enable the
live model.

| Variable | Default | Purpose |
|---|---|---|
| `AZURE_OPENAI_ENDPOINT` | — | e.g. `https://<resource>.services.ai.azure.com` |
| `AZURE_OPENAI_API_KEY` | — | Your Azure OpenAI key |
| `AZURE_OPENAI_DEPLOYMENT` | `gpt-5-mini` | Deployment / model name |
| `AZURE_OPENAI_API_VERSION` | `preview` | API version |
| `AZURE_OPENAI_REASONING_EFFORT` | `minimal` | `minimal` (fast) … `high` (more thorough, slower) |
| `AZURE_OPENAI_TIMEOUT` | `45` | Request timeout in seconds |

> **gpt-5 note:** these models use `max_completion_tokens` (handled internally) and
> charge for hidden reasoning tokens. `reasoning_effort=minimal` keeps the short,
> factual tasks here fast and cheap.

---

## Security & ops

| Variable | Default | Purpose |
|---|---|---|
| `ALLOWED_ORIGINS` | `http://localhost:5173,http://localhost:3000` | Comma-separated CORS allow-list. Lock this to your real domain(s) in production |
| `RATE_LIMIT_PER_MIN` | `240` | Max requests per IP per minute before `429` |

---

## Frontend

The frontend reads one build-time variable (Vite):

| Variable | Default | Purpose |
|---|---|---|
| `VITE_API_URL` | `http://localhost:8000/api` | Backend API base URL |

- Local dev override: `frontend/.env.local`
- Production build: `frontend/.env.production` (ships with `VITE_API_URL=/api`, so
  nginx serves the API same-origin behind a reverse proxy — see
  [Deployment](deployment.md)).

---

## Minimal production checklist

1. `DB_BACKEND=azure` with valid Azure SQL credentials.
2. A strong `JWT_SECRET` and `ENV=production`.
3. `ALLOWED_ORIGINS` set to your real frontend domain(s).
4. (Optional) Azure OpenAI keys for live AI.
</content>
