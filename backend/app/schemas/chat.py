"""Pydantic schemas for chat and code endpoints."""

from pydantic import BaseModel, Field


class CodeGenerationRequest(BaseModel):
    """Request schema for code generation."""

    content: str = Field(..., description="User prompt for code generation")
    session_id: str | None = Field(default=None, description="Session ID for multi-turn context")
    model: str = Field(default="kimi-k2-5", description="AI model to use")
    api_key: str | None = Field(default=None, description="Optional request-scoped Kimi API key")


class CodeExplanationRequest(BaseModel):
    """Request schema for code explanation."""

    content: str = Field(..., description="User question or explanation request")
    code_snippet: str | None = Field(default=None, description="Selected code snippet to explain")
    session_id: str | None = Field(default=None, description="Session ID for context")
    model: str = Field(default="kimi-k2-5", description="AI model to use")
    api_key: str | None = Field(default=None, description="Optional request-scoped Kimi API key")


class CodeExecutionRequest(BaseModel):
    """Request schema for code execution."""

    code: str = Field(..., description="Python code to execute")


class ChatMessage(BaseModel):
    """Individual chat message."""

    role: str = Field(..., description="Message role: user, assistant, system")
    content: str = Field(..., description="Message content")


class UnifiedResponse(BaseModel):
    """Unified API response wrapper."""

    success: bool
    data: dict | None
    error: dict | None
    meta: dict
