from fastapi import APIRouter

from models.schemas import AIResponse, SummarizeRequest
from routes._guards import enforce_max_length
from services.ai_client import ask_ai

router = APIRouter()

_LENGTH_GUIDANCE = {
    "short": "in 1-2 tight sentences",
    "medium": "in a short paragraph (4-6 sentences)",
    "detailed": "as a structured summary with headings and bullet points covering all key points",
}

SYSTEM_PROMPT = (
    "You are a precise summarization assistant. Summarize only what is present "
    "in the provided text — never add outside facts or opinions. Preserve key "
    "names, numbers, and decisions exactly as given."
)


@router.post("/summarize", response_model=AIResponse)
def summarize(payload: SummarizeRequest) -> AIResponse:
    enforce_max_length(payload.text)

    guidance = _LENGTH_GUIDANCE[payload.length.value]
    user_message = (
        f"Summarize the following text {guidance}.\n\n"
        f"---\n{payload.text}\n---"
    )
    result = ask_ai(SYSTEM_PROMPT, user_message)
    return AIResponse(**result)
