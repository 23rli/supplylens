from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel

from auth.security import verify_password, create_token
from auth.store import get_user_by_email, require_auth

router = APIRouter()


class LoginReq(BaseModel):
    email: str
    password: str


@router.post("/auth/login")
def login(req: LoginReq):
    user = get_user_by_email(req.email)
    if not user or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password")
    safe = {"id": user["id"], "email": user["email"], "name": user["name"],
            "role": user["role"], "tenant_id": user["tenant_id"]}
    return {"token": create_token(user), "user": safe}


@router.get("/auth/me")
def me(claims: dict = Depends(require_auth)):
    return {"email": claims["sub"], "role": claims.get("role"),
            "tenant_id": claims.get("tenant_id")}
