from fastapi import APIRouter

from models.schemas import AIResponse, QARequest
from routes._guards import enforce_max_length
from services.ai_client import ask_ai

router = APIRouter()

SYSTEM_PROMPT = (
    "You are a careful question-answering assistant. Answer the user's question "
    "using only the provided context. If the context does not contain enough "
    "information to answer confidently, say so plainly instead of guessing. "
    "Keep answers direct and well-organized."
)


@router.post("/qa", response_model=AIResponse)
def question_answer(payload: QARequest) -> AIResponse:
    enforce_max_length(payload.context, field_name="context")
    enforce_max_length(payload.question, field_name="question")

    user_message = (
        f"Context:\n---\n{payload.context}\n---\n\n"
        f"Question: {payload.question}"
    )
    result = ask_ai(SYSTEM_PROMPT, user_message)
    return AIResponse(**result)
