from dataclasses import dataclass


@dataclass
class TranslationResult:
    source_language: str
    translation: str

    expression: str | None = None
    expression_meaning: str | None = None

    grammar_correction: str | None = None
    grammar_explanation: str | None = None
