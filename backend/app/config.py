"""Application configuration."""

from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    APP_NAME: str = "Learning Coding Agent"
    DEBUG: bool = False

    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    AI_API_KEY: str | None = None
    AI_BASE_URL: str = "https://ark.cn-beijing.volces.com/api/coding/v3"
    AI_MODEL: str = "kimi-k2.6"

    KIMI_API_KEY: str | None = None
    KIMI_BASE_URL: str | None = None
    KIMI_MODEL: str | None = None

    DOCKER_TIMEOUT: int = 30
    DOCKER_MEMORY_LIMIT: str = "512m"
    DOCKER_CPU_LIMIT: float = 1.0

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: list[str] | str) -> list[str]:
        """Parse CORS origins from a list, JSON value, or comma-separated string."""
        if isinstance(value, list):
            return value
        if value == "*":
            return ["*"]
        return [origin.strip() for origin in value.split(",") if origin.strip()]

    @property
    def resolved_ai_api_key(self) -> str | None:
        """Return the configured AI API key, with KIMI_API_KEY as a legacy fallback."""
        return self.AI_API_KEY or self.KIMI_API_KEY

    @property
    def resolved_ai_base_url(self) -> str:
        """Return the configured AI base URL, with KIMI_BASE_URL as a legacy fallback."""
        return self.AI_BASE_URL or self.KIMI_BASE_URL or Settings.model_fields["AI_BASE_URL"].default

    @property
    def resolved_ai_model(self) -> str:
        """Return the configured AI model, with KIMI_MODEL as a legacy fallback."""
        return self.AI_MODEL or self.KIMI_MODEL or Settings.model_fields["AI_MODEL"].default

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
