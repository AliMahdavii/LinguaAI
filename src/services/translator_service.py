from .gemini_service import GeminiService


class TranslatorService:
    def __init__(self):
        self.gemini = GeminiService()

    def translate(self, text: str, target_language: str) -> str:
        prompt = f"""
Translate the following text into {target_language}.

Rules:
- Preserve the original meaning.
- Do not add explanations.
- Do not add extra information.
- Return only the translated text.

Text:
{text}
"""

        return self.gemini.generate(prompt)