from dataclasses import dataclass

from app.ai.providers.base import LLMProvider


@dataclass(frozen=True)
class EvaluationCase:
    question: str
    expected_keywords: tuple[str, ...]


def evaluate_grounding(answer: str, expected_keywords: tuple[str, ...]) -> float:
    """Simple deterministic smoke metric for development.

    This is not a replacement for a full LLM-as-judge evaluation suite.
    """
    if not expected_keywords:
        return 1.0

    lowered = answer.lower()
    hits = sum(keyword.lower() in lowered for keyword in expected_keywords)
    return hits / len(expected_keywords)


def run_smoke_evaluation(
    provider: LLMProvider,
    cases: list[EvaluationCase],
) -> dict[str, float]:
    """Basic provider health check without requiring a database."""
    results = {}
    for index, case in enumerate(cases, start=1):
        answer = provider.generate(
            "Answer briefly and accurately using only the supplied context.",
            f"Context keywords: {', '.join(case.expected_keywords)}\n"
            f"Question: {case.question}",
        )
        results[f"case_{index}"] = evaluate_grounding(
            answer, case.expected_keywords
        )
    return results
