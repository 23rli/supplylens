# Getting Started

This guide gets the entire SupplyLens app running on your computer. You do **not**
need an Azure account, a database server, or any paid service. Everything runs
locally on a built-in SQLite file, and the AI features fall back to deterministic
logic when no AI key is present.

Total time: about 5 minutes.

---

## 1. What you need first

Install these two things if you don't already have them:

| Tool | Why | Check it's installed |
|---|---|---|
| **Python 3.11+** | Runs the backend API | `python --version` |
| **Node.js 18+** | Runs the web frontend | `node --version` |

> On Windows, if `python` isn't found, try `py` instead. On macOS/Linux you may
> need `python3` and `pip3`.

---

## 2. Start the backend (the API + data)

Open a terminal and run these commands one at a time:

```bash
# Go into the backend folder
cd backend

# Install the Python libraries the app needs
pip install fastapi uvicorn python-dotenv pydantic numpy openpyxl python-multipart PyJWT

# Create the local database and fill it with realistic sample data
python data/seed_risk.py        # supplier + SKU risk data
python inventory/seed_parts.py  # ~120 sample parts for the inventory engine
python data/seed_users.py       # creates the demo login account

# Start the API server
uvicorn main:app --reload --port 8000
```

When it's working you'll see `Uvicorn running on http://127.0.0.1:8000`.
Leave this terminal open — the server needs to keep running.

> **Sanity check:** open <http://localhost:8000> in a browser. You should see
> `{"status":"ok","service":"SupplyLens API"}`.

---

## 3. Start the frontend (the website)

Open a **second** terminal (leave the backend running in the first one):

```bash
cd frontend
npm install      # downloads the web libraries (first time only)
npm run dev      # starts the website
```

Then open the address it prints — usually <http://localhost:5173>.

---

## 4. Log in

Use the demo account that the seed script created:

- **Email:** `admin@supplylens.io`
- **Password:** `demo1234`

You're in. Start on the **Today** page for the daily risk briefing, then explore
Risk Intelligence, Inventory, and the Hedging Planner.

---

## 5. (Optional) Turn on the live AI

The app works fully without this — AI panels just use built-in deterministic
summaries. To get real generative answers from Azure OpenAI:

1. Copy the example config:
   ```bash
   cd backend
   cp .env.example .env      # on Windows: copy .env.example .env
   ```
2. Open `backend/.env` and fill in your Azure OpenAI values:
   ```
   AZURE_OPENAI_ENDPOINT=https://<your-resource>.services.ai.azure.com
   AZURE_OPENAI_API_KEY=<your-key>
   AZURE_OPENAI_DEPLOYMENT=gpt-5-mini
   AZURE_OPENAI_API_VERSION=preview
   ```
3. Restart the backend (`Ctrl+C`, then `uvicorn main:app --reload --port 8000`).

That's it — the AI briefing, "Ask AI" box, and chat now use the live model.
See [Configuration](configuration.md) for every available setting.

---

## Common problems

| Symptom | Fix |
|---|---|
| `ModuleNotFoundError` | Re-run the `pip install ...` line from step 2. |
| Login fails | You skipped `python data/seed_users.py`. Run it, then log in again. |
| Frontend loads but no data | The backend isn't running, or it's not on port 8000. Restart step 2. |
| Port 8000 already in use | Stop the other process, or run on another port and update `frontend/.env.local`. |
| AI panels say "AI is offline" | Expected without an Azure key — add one (step 5) to enable live AI. |

---

## What's next?

- Want to load **your own** suppliers and inventory? See [Using Your Own Data](data-guide.md).
- Want to understand each screen? See [Features & Purpose](features.md).
- Want to run the tests? `cd backend && python -m pytest -q`
</content>
