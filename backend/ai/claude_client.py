"""
Wrapper for Azure OpenAI chat completions.
"""
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def call_claude(system_prompt: str, messages: list[dict]) -> str:
    """
    Calls Azure OpenAI. Name kept for backwards compatibility with routers.

    Args:
        system_prompt: The grounded system prompt with live data
        messages: List of {"role": "user"|"assistant", "content": "..."} dicts
                  representing the conversation history

    Returns:
        The assistant's response as a string.
    """
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01"),
    )

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
        max_tokens=1024,
        messages=[{"role": "system", "content": system_prompt}] + messages,
    )

    return response.choices[0].message.content
