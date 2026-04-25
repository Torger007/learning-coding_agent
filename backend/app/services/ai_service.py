"""Kimi K2.5 AI service adapter with streaming support."""

import uuid
from collections.abc import AsyncGenerator

import httpx

from app.config import settings
from app.core.exceptions import ExternalServiceError, ValidationError
from app.schemas.chat import ChatMessage

SYSTEM_PROMPT_CODE = (
    "You are an expert programming tutor. "
    "Generate clean, well-commented code based on the user's request. "
    "Always wrap code blocks in triple backticks with the language identifier. "
    "Explain key concepts briefly after the code."
)

SYSTEM_PROMPT_EXPLAIN = (
    "You are a patient programming tutor for beginners. "
    "Explain code in simple terms. Use analogies where helpful. "
    "Break down complex logic step by step. "
    "If the user asks about a specific code snippet, focus your explanation on that snippet."
)


class AIService:
    """Adapter for Kimi K2.5 API."""

    def __init__(self) -> None:
        self.api_key = settings.KIMI_API_KEY
        self.base_url = settings.KIMI_BASE_URL
        self.model = settings.KIMI_MODEL
        self.client = httpx.AsyncClient(timeout=60.0)

    async def generate_code(
        self,
        prompt: str,
        history: list[dict] | None = None,
        stream: bool = False,
        api_key: str | None = None,
    ) -> str | AsyncGenerator[str, None]:
        """Generate code from a user prompt."""
        return await self._chat(
            system=SYSTEM_PROMPT_CODE,
            prompt=prompt,
            history=history,
            stream=stream,
            api_key=api_key,
        )

    async def explain(
        self,
        prompt: str,
        code_snippet: str | None = None,
        history: list[dict] | None = None,
        stream: bool = False,
        api_key: str | None = None,
    ) -> str | AsyncGenerator[str, None]:
        """Explain code or answer a programming question."""
        full_prompt = prompt
        if code_snippet:
            full_prompt = f"Here is the code snippet:\n```\n{code_snippet}\n```\n\nQuestion: {prompt}"
        return await self._chat(
            system=SYSTEM_PROMPT_EXPLAIN,
            prompt=full_prompt,
            history=history,
            stream=stream,
            api_key=api_key,
        )

    async def _chat(
        self,
        system: str,
        prompt: str,
        history: list[dict] | None = None,
        stream: bool = False,
        api_key: str | None = None,
    ) -> str | AsyncGenerator[str, None]:
        """Send a chat completion request to Kimi API."""
        resolved_api_key = api_key or self.api_key
        if not resolved_api_key:
            raise ValidationError("KIMI_API_KEY is not configured")

        messages: list[dict] = [{"role": "system", "content": system}]
        if history:
            messages.extend(history[-10:])  # Keep last 10 messages for context
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "temperature": 0.3,
        }

        headers = {
            "Authorization": f"Bearer {resolved_api_key}",
            "Content-Type": "application/json",
        }

        url = f"{self.base_url}/chat/completions"

        if stream:
            return self._stream_response(url, headers, payload)

        response = await self.client.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            raise ExternalServiceError(f"Kimi API error: {response.status_code} {response.text}")

        data = response.json()
        return data["choices"][0]["message"]["content"]

    async def _stream_response(
        self,
        url: str,
        headers: dict,
        payload: dict,
    ) -> AsyncGenerator[str, None]:
        """Stream response chunks from Kimi API."""
        async with self.client.stream(
            "POST", url, headers=headers, json=payload
        ) as response:
            if response.status_code != 200:
                text = await response.aread()
                raise ExternalServiceError(
                    f"Kimi API error: {response.status_code} {text.decode()}"
                )
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    import json

                    try:
                        chunk = json.loads(data)
                        delta = chunk["choices"][0]["delta"].get("content", "")
                        if delta:
                            yield delta
                    except (json.JSONDecodeError, KeyError):
                        continue


ai_service = AIService()
