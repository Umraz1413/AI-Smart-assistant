from fastapi import APIRouter

from models.schemas import AIResponse, GenerateRequest
from routes._guards import enforce_max_length
from services.ai_client import ask_ai

router = APIRouter()

_TYPE_GUIDANCE = {
    "email": "a clear, well-structured email with an appropriate subject line",
    "blog_post": "an engaging blog post with a strong opening and clear sections",
    "social_post": "a concise, attention-grabbing social media post",
    "outline": "a structured outline with headings and sub-points",
    "general": "well-organized written content",
}

SYSTEM_PROMPT = (
    "You are a skilled writing assistant. Produce polished, ready-to-use content "
    "based on the user's request. Match the requested content type and tone. "
    "Do not include meta-commentary about what you produced — output only the content itself."
)


@router.post("/generate", response_model=AIResponse)
def generate(payload: GenerateRequest) -> AIResponse:
    enforce_max_length(payload.prompt, field_name="prompt")

    guidance = _TYPE_GUIDANCE.get(payload.content_type, _TYPE_GUIDANCE["general"])
    user_message = (
        f"Write {guidance} in a {payload.tone} tone, based on this request:\n\n"
        f"{payload.prompt}"
    )
    result = ask_ai(SYSTEM_PROMPT, user_message)
    return AIResponse(**result)
