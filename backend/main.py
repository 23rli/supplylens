"""
FastAPI application entry point.
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import risk, suppliers, dashboard, chat, inventory, hedging, actions, ai, auth
from auth.store import require_auth

app = FastAPI(
    title="SupplyLens API",
    description="Supply Chain Risk Intelligence Platform",
    version="1.0.0"
)

# CORS — allow React dev server and production frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite dev server
        "http://localhost:3000",   # CRA dev server (fallback)
        "https://supplylens.vercel.app",  # Production (update with real URL)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")  # open: login + me

# All data routers require a valid bearer token.
_secure = [Depends(require_auth)]
app.include_router(risk.router, prefix="/api", dependencies=_secure)
app.include_router(suppliers.router, prefix="/api", dependencies=_secure)
app.include_router(dashboard.router, prefix="/api", dependencies=_secure)
app.include_router(chat.router, prefix="/api", dependencies=_secure)
app.include_router(inventory.router, prefix="/api", dependencies=_secure)
app.include_router(hedging.router, prefix="/api", dependencies=_secure)
app.include_router(actions.router, prefix="/api", dependencies=_secure)
app.include_router(ai.router, prefix="/api", dependencies=_secure)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "SupplyLens API"}
