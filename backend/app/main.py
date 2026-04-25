"""FastAPI application entry point."""

import asyncio
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import chat, code, ws
from app.config import settings
from app.core.exceptions import AppException, app_exception_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    yield


app = FastAPI(
    title="Learning Coding Agent API",
    description="AI-powered programming learning assistant backend.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials="*" not in settings.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppException, app_exception_handler)

app.include_router(chat.router, prefix="/api/v1")
app.include_router(code.router, prefix="/api/v1")
app.include_router(ws.router, prefix="/api/v1")


@app.get("/api/v1/health", tags=["health"])
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/health", tags=["health"])
async def root_health_check() -> dict:
    """Compatibility health check endpoint."""
    return {"status": "ok"}
