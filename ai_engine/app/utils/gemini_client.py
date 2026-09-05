"""
Shared Gemini client wrapper.
All Gemini API calls in this project should go through call_gemini(),
so error handling, retries, and model selection stay in one place.
"""

import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

_client = None


def get_client():
    """Returns a cached Gemini client, creating it once if needed."""
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not found in .env")
        _client = genai.Client(api_key=api_key)
    return _client


def call_gemini(prompt: str, model: str = "gemini-flash-latest", max_retries: int = 3) -> str:
    """
    Sends a prompt to Gemini and returns the raw text response.
    Retries automatically on temporary server errors (like 503 high demand),
    with a short increasing delay between attempts.
    Raises an exception only after all retries are exhausted -
    callers must still handle that and fall back.
    """
    client = get_client()
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )
            return response.text
        except Exception as e:
            last_error = e
            if attempt < max_retries:
                time.sleep(1.5 * attempt)  # 1.5s, then 3s, then would be 4.5s
            continue

    raise last_error