"""
FastAPI application entry point.
"""
import os
import time
from collections import defaultdict, deque

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from routers import risk, suppliers, dashboard, chat, inventory, hedging, actions, ai, auth
from auth.store import require_auth

app = FastAPI(
    title="SupplyLens API",
    description="Supply Chain Risk Intelligence Platform",
    version="1.0.0",
)

# ── Rate limiting: per-IP sliding window (cost/DoS protection) ───────────────
RATE_LIMIT = int(os.getenv("RATE_LIMIT_PER_MIN", "240"))
_WINDOW = 60.0
_hits: dict[str, deque] = defaultdict(deque)


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.method == "OPTIONS" or request.url.path == "/":
            return await call_next(request)
        ip = request.client.host if request.client else "unknown"
        now = time.time()
        q = _hits[ip]
        while q and now - q[0] > _WINDOW:
            q.popleft()
        if len(q) >= RATE_LIMIT:
            return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded. Please slow down."})
        q.append(now)
        return await call_next(request)


# Added first -> innermost. CORS added last -> outermost, so even 429s carry CORS headers.
app.add_middleware(RateLimitMiddleware)

# ── CORS: explicit allow-list from env (no wildcards in prod) ────────────────
_DEFAULT_ORIGINS = "http://localhost:5173,http://localhost:3000"
ALLOWED_ORIGINS = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", _DEFAULT_ORIGINS).split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
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
