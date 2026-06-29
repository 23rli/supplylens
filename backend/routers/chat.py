from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_ai_context
from ai.prompt_builder import build_system_prompt
from ai.claude_client import call_claude

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_history: list[dict] = []   # [{"role": "user"|"assistant", "content": "..."}]

class ChatResponse(BaseModel):
    response: str
    data_timestamp: str

@router.post("/chat")
def chat(request: ChatRequest) -> ChatResponse:
    """
    Core AI endpoint.
    1. Pulls live data from MySQL
    2. Builds grounded system prompt
    3. Calls Claude API with full conversation history
    4. Returns response
    """
    try:
        # Pull live data
        context = get_ai_context()

        # Build system prompt with live data injected
        system_prompt = build_system_prompt(context)

        # Build messages array: history + new user message
        messages = request.conversation_history + [
            {"role": "user", "content": request.message}
        ]

        # Call Claude
        response_text = call_claude(system_prompt, messages)

        from datetime import datetime
        return ChatResponse(
            response=response_text,
            data_timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        import logging
        logging.getLogger("supplylens").exception("chat endpoint failed")
        raise HTTPException(status_code=500, detail="AI request failed. Please try again.")
