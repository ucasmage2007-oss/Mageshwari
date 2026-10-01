from __future__ import annotations

from typing import Any

from google import genai
from google.genai import types

from config import settings


class GeminiService:
    def __init__(self) -> None:
        if not settings.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured. "
                "Add it to the .env file."
            )

        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_model

    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.3,
        max_output_tokens: int = 1000,
        response_mime_type: str | None = None,
        json_schema: dict[str, Any] | None = None,
    ) -> str:
        config_kwargs: dict[str, Any] = {
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
        }

        if response_mime_type:
            config_kwargs["response_mime_type"] = response_mime_type

        if json_schema:
            config_kwargs["response_schema"] = json_schema

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(**config_kwargs),
        )

        text = response.text

        if not text:
            raise RuntimeError("Gemini returned an empty response.")

        return text.strip()


_gemini_service: GeminiService | None = None


def get_gemini() -> GeminiService:
    global _gemini_service

    if _gemini_service is None:
        _gemini_service = GeminiService()

    return _gemini_service