"""
Wrapper for Anthropic API calls.
"""
import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

def call_claude(system_prompt: str, messages: list[dict]) -> str:
    """
    Calls the Anthropic Claude API.

    Args:
        system_prompt: The grounded system prompt with live data
        messages: List of {"role": "user"|"assistant", "content": "..."} dicts
                  representing the conversation history

    Returns:
        The assistant's response as a string.
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=system_prompt,
        messages=messages,
    )

    return response.content[0].text
