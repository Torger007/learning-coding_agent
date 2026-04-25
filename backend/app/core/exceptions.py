"""Application exceptions and error responses."""

from fastapi import Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    """Base application exception."""

    def __init__(self, code: str, message: str, status_code: int = 400) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class ValidationError(AppException):
    """Validation error."""

    def __init__(self, message: str) -> None:
        super().__init__("VALIDATION_ERROR", message, 400)


class ExternalServiceError(AppException):
    """External service error."""

    def __init__(self, message: str) -> None:
        super().__init__("EXTERNAL_SERVICE_ERROR", message, 502)


class SandboxError(AppException):
    """Code sandbox execution error."""

    def __init__(self, message: str) -> None:
        super().__init__("SANDBOX_ERROR", message, 400)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle application exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "data": None,
            "error": {"code": exc.code, "message": exc.message, "details": []},
            "meta": {"request_id": getattr(request.state, "request_id", "")},
        },
    )
