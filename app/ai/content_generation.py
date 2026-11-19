import json
import re
from typing import Any

from app.ai.prompts import (
    FLASHCARD_INSTRUCTIONS,
    IMPORTANT_QUESTION_INSTRUCTIONS,
    QUIZ_INSTRUCTIONS,
)
from app.ai.providers.base import LLMProvider


def _parse_json(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return json.loads(cleaned)


def generate_quiz(
    provider: LLMProvider,
    *,
    context: str,
    count: int = 5,
) -> list[dict[str, Any]]:
    count = max(1, min(count, 20))
    raw = provider.generate(
        QUIZ_INSTRUCTIONS,
        f"Generate exactly {count} questions from this academic context:\n\n{context}",
    )
    return list(_parse_json(raw).get("questions") or [])


def generate_flashcards(
    provider: LLMProvider,
    *,
    context: str,
    count: int = 8,
) -> list[dict[str, Any]]:
    count = max(1, min(count, 30))
    raw = provider.generate(
        FLASHCARD_INSTRUCTIONS,
        f"Generate exactly {count} flashcards from this academic context:\n\n{context}",
    )
    return list(_parse_json(raw).get("cards") or [])


def generate_important_questions(
    provider: LLMProvider,
    *,
    context: str,
    count: int = 8,
) -> list[dict[str, Any]]:
    count = max(1, min(count, 20))
    raw = provider.generate(
        IMPORTANT_QUESTION_INSTRUCTIONS,
        f"Generate up to {count} high-priority revision questions from:\n\n{context}",
    )
    return list(_parse_json(raw).get("questions") or [])
