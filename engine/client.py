"""
OpenAI-compatible client wrapper for Ollama local endpoints.
"""

from openai import OpenAI

DEFAULT_BASE_URL = "http://localhost:11434/v1"
DEFAULT_MODEL = "llama3.2:1b"


def get_client(base_url: str = DEFAULT_BASE_URL, api_key: str = "ollama") -> OpenAI:
    """Create and return an OpenAI SDK client pointed at a local Ollama instance."""
    return OpenAI(base_url=base_url, api_key=api_key)


def ask_llm(
    prompt: str,
    model: str = DEFAULT_MODEL,
    system_prompt: str = "You are a helpful assistant",
    base_url: str = DEFAULT_BASE_URL,
) -> str:
    """Send a prompt using the OpenAI completions endpoint format."""
    client = get_client(base_url=base_url)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content

