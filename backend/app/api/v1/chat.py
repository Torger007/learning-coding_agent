"""Chat API routes for code generation and explanation."""

import uuid

from fastapi import APIRouter

from app.core.exceptions import ValidationError
from app.schemas.chat import (
    CodeExplanationRequest,
    CodeGenerationRequest,
    UnifiedResponse,
)
from app.services.ai_service import ai_service
from app.services.chat_service import chat_service

router = APIRouter(tags=["chat"])


def _build_meta() -> dict:
    return {"request_id": str(uuid.uuid4()), "timestamp": __import__("datetime").datetime.now().isoformat()}


@router.post("/chat/code", response_model=UnifiedResponse)
async def generate_code(request: CodeGenerationRequest) -> dict:
    """Generate code from a user prompt."""
    if not request.content.strip():
        raise ValidationError("Content cannot be empty")

    session_id = request.session_id or str(uuid.uuid4())
    history = chat_service.get_history(session_id)

    result = await ai_service.generate_code(
        prompt=request.content,
        history=history,
        stream=False,
        api_key=request.api_key,
    )

    chat_service.append_message(session_id, {"role": "user", "content": request.content})
    chat_service.append_message(session_id, {"role": "assistant", "content": result})

    return {
        "success": True,
        "data": {"content": result, "session_id": session_id},
        "error": None,
        "meta": _build_meta(),
    }


@router.post("/chat/explain", response_model=UnifiedResponse)
async def explain_code(request: CodeExplanationRequest) -> dict:
    """Explain code or answer a programming question."""
    if not request.content.strip():
        raise ValidationError("Content cannot be empty")

    session_id = request.session_id or str(uuid.uuid4())
    history = chat_service.get_history(session_id)

    result = await ai_service.explain(
        prompt=request.content,
        code_snippet=request.code_snippet,
        history=history,
        stream=False,
        api_key=request.api_key,
    )

    chat_service.append_message(session_id, {"role": "user", "content": request.content})
    chat_service.append_message(session_id, {"role": "assistant", "content": result})

    return {
        "success": True,
        "data": {"content": result, "session_id": session_id},
        "error": None,
        "meta": _build_meta(),
    }
