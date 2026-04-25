"""Code execution API routes."""

import uuid

from fastapi import APIRouter

from app.core.exceptions import ValidationError
from app.schemas.chat import CodeExecutionRequest, UnifiedResponse
from app.services.code_execution import code_execution_service

router = APIRouter(tags=["code"])


def _build_meta() -> dict:
    return {"request_id": str(uuid.uuid4()), "timestamp": __import__("datetime").datetime.now().isoformat()}


@router.post("/code/execute", response_model=UnifiedResponse)
async def execute_code(request: CodeExecutionRequest) -> dict:
    """Execute Python code in a Docker sandbox."""
    if not request.code.strip():
        raise ValidationError("Code cannot be empty")

    result = await code_execution_service.execute(request.code)

    return {
        "success": result["success"],
        "data": result if result["success"] else None,
        "error": None if result["success"] else {"code": "EXECUTION_ERROR", "message": result["error"], "details": []},
        "meta": _build_meta(),
    }
