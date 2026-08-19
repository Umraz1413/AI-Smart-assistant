"""
Thin wrapper around the Google Gemini API (google-genai SDK).

Centralizing the API call here means every route gets the same
error-handling behavior for free, and the API key only ever gets
read in one place. Swapped in place of the original Anthropic
client so the app can run entirely on Google AI Studio's free tier
(no credit card required).
"""
import logging

from fastapi import HTTPException
from google import genai
from google.genai import errors as genai_errors
from google.genai import types as genai_types

from config import settings

logger = logging.getLogger("ai_assistant.ai_client")

_client: genai.Client | None = None


def get_client() -> genai.Client:
    global _client
    if _client is None:
        settings.validate()
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


def ask_ai(system_prompt: str, user_message: str, max_tokens: int | None = None) -> dict:
    """
    Send a single-turn request to Gemini and return the text result
    plus token usage. Raises HTTPException with an appropriate status
    code on any failure so routes don't need to repeat error handling.
    """
    client = get_client()

    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=user_message,
            config=genai_types.GenerateContentConfig(
                system_instruction=system_prompt,
                max_output_tokens=max_tokens or settings.MAX_TOKENS,
            ),
        )
    except genai_errors.ClientError as exc:
        status = getattr(exc, "code", None)
        logger.warning("Gemini API client error (status %s): %s", status, exc)
        if status == 429:
            raise HTTPException(
                status_code=429,
                detail=(
                    "You've hit the free-tier rate limit for Gemini. Wait a bit "
                    "(usually under a minute) and try again."
                ),
            ) from exc
        if status in (401, 403):
            raise HTTPException(
                status_code=500,
                detail="Server is misconfigured: the Gemini API key is invalid or missing permissions.",
            ) from exc
        raise HTTPException(
            status_code=400, detail=f"The AI service rejected the request: {exc}"
        ) from exc
    except genai_errors.ServerError as exc:
        logger.error("Gemini API server error: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="Google's AI service is temporarily unavailable. Please try again shortly.",
        ) from exc
    except Exception as exc:  # noqa: BLE001 - last-resort guard, always logged
        logger.exception("Unexpected error calling Gemini API")
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred while contacting the AI service."
        ) from exc

    result_text = (response.text or "").strip()

    if not result_text:
        raise HTTPException(status_code=502, detail="The AI service returned an empty response.")

    usage = getattr(response, "usage_metadata", None)

    return {
        "result": result_text,
        "model": settings.GEMINI_MODEL,
        "input_tokens": getattr(usage, "prompt_token_count", None) if usage else None,
        "output_tokens": getattr(usage, "candidates_token_count", None) if usage else None,
    }
