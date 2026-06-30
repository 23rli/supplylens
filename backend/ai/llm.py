"""
LLM client for the AI copilot. Targets the Azure AI Foundry v1 chat-completions
endpoint, which is what gpt-5 deployments use. Pure stdlib HTTP. Falls back
gracefully when not configured or unreachable.

Performance: gpt-5 reasoning models default to heavy hidden reasoning (slow). For
the short, factual tasks here we set reasoning_effort=minimal, which cuts latency
~2-3x and avoids wasted reasoning tokens.
"""
import json
import os
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MAX_TOKENS = 1200
DEFAULT_REASONING = os.getenv("AZURE_OPENAI_REASONING_EFFORT", "minimal")
TIMEOUT = int(os.getenv("AZURE_OPENAI_TIMEOUT", "45"))


def is_configured() -> bool:
    key = os.getenv("AZURE_OPENAI_API_KEY", "")
    return bool(os.getenv("AZURE_OPENAI_ENDPOINT")) and bool(key) and key != "PASTE_YOUR_KEY_HERE"


def _url() -> str:
    base = (os.getenv("AZURE_OPENAI_ENDPOINT") or "").rstrip("/")
    if "/openai/v1" in base:
        base = base.split("/openai/v1")[0]
    return f"{base}/openai/v1/chat/completions"


class LLMError(RuntimeError):
    pass


def chat(messages: list[dict], max_tokens: int = DEFAULT_MAX_TOKENS,
         temperature: float | None = None, reasoning_effort: str | None = DEFAULT_REASONING) -> str:
    if not is_configured():
        raise LLMError("Azure OpenAI not configured")
    payload = {
        "model": os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5-mini"),
        "messages": messages,
        "max_completion_tokens": max_tokens,
    }
    if reasoning_effort:
        payload["reasoning_effort"] = reasoning_effort
    if temperature is not None:
        payload["temperature"] = temperature
    req = urllib.request.Request(
        _url(), data=json.dumps(payload).encode(),
        headers={"api-key": os.getenv("AZURE_OPENAI_API_KEY"), "Content-Type": "application/json"},
    )
    try:
        r = json.load(urllib.request.urlopen(req, timeout=TIMEOUT))
        content = (r["choices"][0]["message"]["content"] or "").strip()
        if not content:
            raise LLMError("empty completion")
        return content
    except urllib.error.HTTPError as e:
        raise LLMError(f"HTTP {e.code}: {e.read().decode()[:200]}")
    except LLMError:
        raise
    except Exception as e:
        raise LLMError(f"{type(e).__name__}: {e}")


def chat_json(system: str, user: str, max_tokens: int = DEFAULT_MAX_TOKENS) -> dict:
    out = chat(
        [{"role": "system", "content": system + " Respond with ONLY valid minified JSON, no markdown."},
         {"role": "user", "content": user}],
        max_tokens=max_tokens,
    )
    s = out.strip()
    if s.startswith("```"):
        s = s.strip("`")
        s = s[s.find("{"): s.rfind("}") + 1]
    return json.loads(s)
