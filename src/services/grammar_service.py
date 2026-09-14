from .gemini_service import GeminiService


class GrammarService:
    def __init__(self):
        self.gemini = GeminiService()

    def check(self, text: str) -> dict:
        prompt = f"""
You are a grammar correction assistant.

Analyze the following text.

Return ONLY valid JSON using exactly this structure:

{{
    "has_errors": true,
    "corrected_text": "...",
    "explanation": "..."
}}

Rules:

- Detect grammar mistakes in the text.
- If there are no grammar mistakes:
  - set "has_errors" to false
  - keep "corrected_text" identical to the original text
  - set "explanation" to null
- If there are mistakes:
  - set "has_errors" to true
  - provide the corrected version
  - briefly explain the important corrections
- Do not change the meaning.
- Do not change the style unnecessarily.
- Return ONLY valid JSON.
- Do not use Markdown.

Text:
{text}
"""

        response = self.gemini.generate(prompt)

        return response
