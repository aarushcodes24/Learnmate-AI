import json
import re
from dataclasses import dataclass

from app.ai.prompts import DIAGNOSTIC_INSTRUCTIONS
from app.ai.providers.base import LLMProvider


@dataclass(frozen=True)
class StudentAnalysis:
    topic: str
    concepts_demonstrated: list[str]
    concepts_missing: list[str]
    misconceptions: list[str]
    terminology_score: int
    reasoning_score: int
    conceptual_depth_score: int
    confidence_estimate: int
    overall_understanding: str
    recommended_next_action: str


def _parse_json(text: str) -> dict:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return json.loads(cleaned)


def _bounded_score(value: object) -> int:
    try:
        return max(0, min(100, int(value)))
    except (TypeError, ValueError):
        return 0


def analyse_student_response(
    provider: LLMProvider,
    *,
    topic: str,
    question: str,
    student_answer: str,
    expected_context: str,
) -> StudentAnalysis:
    if not student_answer.strip():
        raise ValueError("student_answer cannot be empty.")

    user_input = f"""
Topic: {topic}

Question:
{question}

Academic context:
{expected_context}

Student answer:
{student_answer}

Evaluate the answer against the academic context. Focus on conceptual
understanding rather than writing quality.
""".strip()

    raw = provider.generate(DIAGNOSTIC_INSTRUCTIONS, user_input)
    data = _parse_json(raw)

    return StudentAnalysis(
        topic=str(data.get("topic") or topic),
        concepts_demonstrated=list(data.get("concepts_demonstrated") or []),
        concepts_missing=list(data.get("concepts_missing") or []),
        misconceptions=list(data.get("misconceptions") or []),
        terminology_score=_bounded_score(data.get("terminology_score")),
        reasoning_score=_bounded_score(data.get("reasoning_score")),
        conceptual_depth_score=_bounded_score(data.get("conceptual_depth_score")),
        confidence_estimate=_bounded_score(data.get("confidence_estimate")),
        overall_understanding=str(
            data.get("overall_understanding") or "weak"
        ),
        recommended_next_action=str(
            data.get("recommended_next_action") or "clarify"
        ),
    )
