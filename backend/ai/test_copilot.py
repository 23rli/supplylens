"""Resilience: copilot must always return usable output, even with the LLM off."""
import ai.copilot as copilot
import ai.llm as llm


def test_briefing_fallback_without_ai(monkeypatch):
    monkeypatch.setattr(llm, "is_configured", lambda: False)
    monkeypatch.setattr(copilot, "is_configured", lambda: False)
    b = copilot.briefing()
    assert b["headline"] and "CRITICAL" in b["headline"]
    assert b["ai"] is False


def test_ask_fallback_without_ai(monkeypatch):
    monkeypatch.setattr(copilot, "is_configured", lambda: False)
    r = copilot.ask("what now?")
    assert r["answer"] and r["ai"] is False
