"""
Application configuration.

Loads settings from environment variables (via a local .env file in
development). Never hardcode secrets here — the API key must always
come from the environment.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    MAX_TOKENS: int = int(os.getenv("GEMINI_MAX_TOKENS", "2048"))
    ALLOWED_ORIGINS: list[str] = os.getenv(
        "ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
    ).split(",")
    MAX_INPUT_CHARS: int = int(os.getenv("MAX_INPUT_CHARS", "20000"))

    def validate(self) -> None:
        if not self.GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Copy backend/.env.example to "
                "backend/.env and add your free key from https://aistudio.google.com/apikey "
                "before starting the server."
            )


settings = Settings()
