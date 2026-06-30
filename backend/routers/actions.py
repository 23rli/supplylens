from fastapi import APIRouter, Query, HTTPException, Depends
from pydantic import BaseModel
from decision.store import explain, today
from decision.execution import create_po, transfer_stock, list_actions
from auth.store import require_auth

router = APIRouter()

@router.get("/today")
def today_brief():
    return today()

@router.get("/explain-decision")
def explain_decision(sku: str = Query(...), site: str = Query(...)):
    r = explain(sku, site)
    if not r:
        raise HTTPException(404, "SKU/site not found")
    return r

class ExecReq(BaseModel):
    sku: str; site: str; label: str = ""; cost: float = 0; benefit: float = 0

@router.post("/actions/create-po")
def po(r: ExecReq, claims: dict = Depends(require_auth)):
    return create_po(claims.get("tenant_id"), r.sku, r.site, r.label or "Expedite PO", r.cost, r.benefit)

@router.post("/actions/transfer")
def transfer(r: ExecReq, claims: dict = Depends(require_auth)):
    return transfer_stock(claims.get("tenant_id"), r.sku, r.site, r.label or "Transfer", r.cost, r.benefit)

@router.get("/actions/status")
def status(claims: dict = Depends(require_auth)):
    return list_actions(claims.get("tenant_id"))
