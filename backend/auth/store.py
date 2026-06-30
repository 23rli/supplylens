"""User store + FastAPI auth dependency."""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from db import fetch_one
from auth.security import decode_token

_bearer = HTTPBearer(auto_error=False)


def get_user_by_email(email: str) -> dict | None:
    return fetch_one("SELECT * FROM users WHERE email = ?", (email.lower().strip(),))


def require_auth(cred: HTTPAuthorizationCredentials = Depends(_bearer)) -> dict:
    """Validates the bearer token; returns the claims. Raises 401 otherwise."""
    if cred is None or not cred.credentials:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authenticated",
                            headers={"WWW-Authenticate": "Bearer"})
    try:
        claims = decode_token(cred.credentials)
    except Exception:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token",
                            headers={"WWW-Authenticate": "Bearer"})
    return claims
