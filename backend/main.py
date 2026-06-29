"""
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import risk, suppliers, dashboard, chat, inventory, hedging, actions, ai

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

app.include_router(risk.router, prefix="/api")
app.include_router(suppliers.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(inventory.router, prefix="/api")
app.include_router(hedging.router, prefix="/api")
app.include_router(actions.router, prefix="/api")
app.include_router(ai.router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "ok", "service": "SupplyLens API"}
