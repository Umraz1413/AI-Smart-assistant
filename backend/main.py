"""
AI Smart Assistant — FastAPI backend.

Run with:
    uvicorn main:app --reload
"""
import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from config import settings
from routes import analyze, generate, qa, suggest, summarize

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("ai_assistant")

app = FastAPI(
    title="AI Smart Assistant API",
    description="Backend for a productivity assistant powered by Claude.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.on_event("startup")
def check_config() -> None:
    try:
        settings.validate()
        logger.info("Configuration OK. Using model: %s", settings.GEMINI_MODEL)
    except RuntimeError as exc:
        # Don't crash the whole server on startup — surface the problem on
        # every request instead so the frontend can show a clear message.
        logger.warning("Startup config check failed: %s", exc)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"error": "Invalid request.", "detail": str(exc)})


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception on %s", request.url.path)
    return JSONResponse(status_code=500, content={"error": "Internal server error."})


@app.get("/api/health")
def health_check() -> dict:
    """Lets the frontend confirm the backend is reachable and configured."""
    configured = bool(settings.GEMINI_API_KEY)
    return {
        "status": "ok" if configured else "misconfigured",
        "api_key_configured": configured,
        "model": settings.GEMINI_MODEL,
    }


app.include_router(summarize.router, prefix="/api", tags=["Summarize"])
app.include_router(qa.router, prefix="/api", tags=["Question Answering"])
app.include_router(generate.router, prefix="/api", tags=["Content Generation"])
app.include_router(analyze.router, prefix="/api", tags=["Document Analysis"])
app.include_router(suggest.router, prefix="/api", tags=["Suggestions"])
