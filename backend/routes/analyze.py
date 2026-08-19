from fastapi import APIRouter

from models.schemas import AIResponse, AnalyzeRequest
from routes._guards import enforce_max_length
from services.ai_client import ask_ai

router = APIRouter()

SYSTEM_PROMPT = (
    "You are a document analysis assistant. Given a piece of text, produce a "
    "structured analysis with these sections: \n"
    "1. Overview (2-3 sentences)\n"
    "2. Key Points (bullet list)\n"
    "3. Tone & Style (brief note)\n"
    "4. Notable Entities (people, organizations, dates, figures mentioned, if any)\n"
    "5. Potential Issues or Gaps (contradictions, unclear claims, missing context — "
    "omit this section if none are found)\n"
    "Use clear markdown formatting."
)


@router.post("/analyze", response_model=AIResponse)
def analyze(payload: AnalyzeRequest) -> AIResponse:
    enforce_max_length(payload.text)

    user_message = f"Analyze the following text:\n\n---\n{payload.text}\n---"
    result = ask_ai(SYSTEM_PROMPT, user_message)
    return AIResponse(**result)
