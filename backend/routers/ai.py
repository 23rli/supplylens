from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from ai.copilot import briefing, explain_decision, ask

router = APIRouter()

@router.get("/ai/briefing")
def ai_briefing():
    return briefing()

@router.get("/ai/explain")
def ai_explain(sku: str = Query(...), site: str = Query(...)):
    r = explain_decision(sku, site)
    if not r:
        raise HTTPException(404, "SKU/site not found")
    return r

class AskReq(BaseModel):
    question: str

@router.post("/ai/ask")
def ai_ask(req: AskReq):
    return ask(req.question)
