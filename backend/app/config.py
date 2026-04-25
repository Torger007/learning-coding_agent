"""Application configuration."""

from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    APP_NAME: str = "Learning Coding Agent"
    DEBUG: bool = False

    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    KIMI_API_KEY: str | None = None
    KIMI_BASE_URL: str = "https://api.moonshot.cn/v1"
    KIMI_MODEL: str = "kimi-k2-5"

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

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
