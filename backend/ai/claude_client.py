"""
Wrapper kept for backwards compatibility with routers/chat.py.
Delegates to ai.llm (Foundry v1 endpoint). Raises on failure so the caller
returns a graceful error.
"""
from ai.llm import chat


def call_claude(system_prompt: str, messages: list[dict]) -> str:
    """Calls the configured model with a system prompt + conversation history."""
    full = [{"role": "system", "content": system_prompt}] + messages
    return chat(full, max_tokens=1500)
