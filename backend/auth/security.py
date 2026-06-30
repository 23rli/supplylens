"""
Authentication primitives: PBKDF2 password hashing (stdlib) + JWT (PyJWT).
No native deps. Secrets come from env.
"""
import hashlib
import hmac
import os
import secrets
from datetime import datetime, timedelta, timezone

import jwt

_DEFAULT_SECRET = "dev-insecure-change-me"
JWT_SECRET = os.getenv("JWT_SECRET", _DEFAULT_SECRET)
JWT_ALG = "HS256"
JWT_TTL_HOURS = int(os.getenv("JWT_TTL_HOURS", "12"))
_PBKDF2_ROUNDS = 200000

# Fail fast in production if the signing secret was never overridden.
if JWT_SECRET == _DEFAULT_SECRET and os.getenv("ENV", "").lower() in ("prod", "production"):
    raise RuntimeError(
        "JWT_SECRET is set to the insecure default in a production environment. "
        "Set a strong JWT_SECRET environment variable before starting the server."
    )


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), _PBKDF2_ROUNDS)
    return f"pbkdf2_sha256${_PBKDF2_ROUNDS}${salt}${dk.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        _, rounds, salt, digest = stored.split("$")
        dk = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), int(rounds))
        return hmac.compare_digest(dk.hex(), digest)
    except Exception:
        return False


def create_token(user: dict) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user["email"],
        "uid": user["id"],
        "tenant_id": user.get("tenant_id"),
        "role": user.get("role", "member"),
        "iat": now,
        "exp": now + timedelta(hours=JWT_TTL_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
