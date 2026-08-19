from fastapi import APIRouter

from models.schemas import AIResponse, SuggestRequest
from routes._guards import enforce_max_length
from services.ai_client import ask_ai

router = APIRouter()

SYSTEM_PROMPT = (
    "You are a productivity coach. Given the user's notes, task list, or "
    "description of their situation, suggest concrete next actions. Prioritize "
    "by urgency and impact, flag anything that looks blocked or time-sensitive, "
    "and keep suggestions specific and actionable rather than generic advice. "
    "Return a short prioritized list (max 7 items), each with a one-line reason."
)


@router.post("/suggest", response_model=AIResponse)
def suggest(payload: SuggestRequest) -> AIResponse:
    enforce_max_length(payload.context)

    user_message = f"Here is my current context:\n\n---\n{payload.context}\n---"
    result = ask_ai(SYSTEM_PROMPT, user_message)
    return AIResponse(**result)
