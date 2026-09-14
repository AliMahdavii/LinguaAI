import json

from .gemini_service import GeminiService
from ..models import TranslationResult


class TranslatorService:
    def __init__(self):
        self.gemini = GeminiService()

    def translate(
        self,
        text: str,
        target_language: str
    ) -> TranslationResult:

        prompt = f"""
You are an AI translation assistant.

Translate the user's text into {target_language}.

Your response MUST be valid JSON.

Use exactly this structure:

{{
    "source_language": "...",
    "translation": "...",
    "expression": null,
    "expression_meaning": null
}}

Rules:

- Detect the source language automatically.
- Preserve the original meaning.
- Preserve the tone and context.
- If the text contains an idiom, slang, or important expression,
  put the expression in "expression".
- Explain that expression briefly in "expression_meaning".
- If there is no important expression, use null.
- Return ONLY valid JSON.
- Do not use Markdown.
- Do not add any explanation outside the JSON.

Text:
{text}
"""

        response = self.gemini.generate(prompt)

        data = json.loads(response)

        return TranslationResult(
            source_language=data["source_language"],
            translation=data["translation"],
            expression=data.get("expression"),
            expression_meaning=data.get("expression_meaning")
        )