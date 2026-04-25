"""Tests for AI service adapter."""

import pytest
from httpx import Response

from app.core.exceptions import ExternalServiceError, ValidationError
from app.services.ai_service import AIService


class TestAIService:
    """Test suite for AIService."""

    @pytest.fixture
    def service(self, monkeypatch):
        """Create an AIService with a dummy API key."""
        monkeypatch.setenv("KIMI_API_KEY", "test-key")
        svc = AIService()
        svc.api_key = "test-key"
        return svc

    @pytest.mark.asyncio
    async def test_generate_code_without_api_key_raises(self):
        """Test that missing API key raises ValidationError."""
        svc = AIService()
        svc.api_key = None
        with pytest.raises(ValidationError):
            await svc.generate_code("hello")

    @pytest.mark.asyncio
    async def test_generate_code_api_failure(self, service, monkeypatch):
        """Test that API failure raises ExternalServiceError."""

        async def mock_post(*args, **kwargs):
            return Response(status_code=500, text="Internal Server Error")

        monkeypatch.setattr(service.client, "post", mock_post)

        with pytest.raises(ExternalServiceError):
            await service.generate_code("hello")

    @pytest.mark.asyncio
    async def test_explain_with_code_snippet(self, service, monkeypatch):
        """Test explanation includes code snippet in prompt."""
        called_with = {}

        async def mock_post(url, headers, json):
            called_with["payload"] = json
            return Response(
                status_code=200,
                json={
                    "choices": [{"message": {"content": "Explanation here"}}]
                },
            )

        monkeypatch.setattr(service.client, "post", mock_post)

        result = await service.explain("Why?", code_snippet="print('hi')")

        assert result == "Explanation here"
        messages = called_with["payload"]["messages"]
        assert any("print('hi')" in m["content"] for m in messages)

    @pytest.mark.asyncio
    async def test_request_scoped_api_key_overrides_environment_key(self, service, monkeypatch):
        """Test request-scoped API key is used for outbound calls."""
        called_with = {}

        async def mock_post(url, headers, json):
            called_with["headers"] = headers
            return Response(
                status_code=200,
                json={"choices": [{"message": {"content": "Code here"}}]},
            )

        monkeypatch.setattr(service.client, "post", mock_post)

        result = await service.generate_code("hello", api_key="request-key")

        assert result == "Code here"
        assert called_with["headers"]["Authorization"] == "Bearer request-key"
