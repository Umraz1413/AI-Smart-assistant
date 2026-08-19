"""Pydantic models shared by all routes."""
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class SummaryLength(str, Enum):
    short = "short"
    medium = "medium"
    detailed = "detailed"


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to summarize")
    length: SummaryLength = SummaryLength.medium

    @field_validator("text")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("text must not be blank")
        return v


class QARequest(BaseModel):
    context: str = Field(..., min_length=1, description="Source material to answer from")
    question: str = Field(..., min_length=1)


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="What to write")
    content_type: str = Field(
        default="general",
        description="email | blog_post | social_post | outline | general",
    )
    tone: str = Field(default="neutral", description="e.g. professional, casual, friendly")


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1)


class SuggestRequest(BaseModel):
    context: str = Field(
        ..., min_length=1, description="Notes, task list, or situation to get suggestions for"
    )


class AIResponse(BaseModel):
    result: str
    model: str
    input_tokens: int | None = None
    output_tokens: int | None = None


class ErrorResponse(BaseModel):
    error: str
    detail: str | None = None
