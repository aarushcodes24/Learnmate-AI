"""Transparent mastery calculations from quiz and diagnostic evidence.

Inputs are records supplied by the caller; this module deliberately does not
own persistence. Scores use a 0-100 scale. Recent evidence receives more weight.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable, Mapping, Any


def _score(value: Any, name: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a number from 0 to 100") from exc
    if not isfinite(result) or not 0 <= result <= 100:
        raise ValueError(f"{name} must be a number from 0 to 100")
    return result


@dataclass(frozen=True)
class MasteryResult:
    topic: str
    mastery_score: float
    confidence_score: float
    evidence_count: int
    status: str


def calculate_topic_mastery(
    topic: str,
    attempts: Iterable[Mapping[str, Any]],
    *,
    recency_decay: float = 0.85,
) -> MasteryResult:
    """Calculate topic mastery from attempts, newest first.

    Each attempt must contain ``score``. Optional ``confidence_estimate`` and
    ``conceptual_depth_score`` (the fields emitted by app.ai.student_analysis)
    refine the score. For each attempt the weighted score is 70% assessment,
    20% conceptual depth, and 10% confidence when those diagnostic fields exist;
    if absent, the assessment score alone is used. Weights decay by age.
    """
    if not topic or not topic.strip():
        raise ValueError("topic cannot be empty")
    if not 0 < recency_decay <= 1:
        raise ValueError("recency_decay must be greater than 0 and at most 1")
    rows = list(attempts)
    if not rows:
        return MasteryResult(topic.strip(), 0.0, 0.0, 0, "not_assessed")

    weighted_total = weight_total = confidence_total = confidence_weight = 0.0
    for index, row in enumerate(rows):
        assessment = _score(row.get("score"), "score")
        has_diagnostic = row.get("conceptual_depth_score") is not None or row.get("confidence_estimate") is not None
        if has_diagnostic:
            depth = _score(row.get("conceptual_depth_score", assessment), "conceptual_depth_score")
            confidence = _score(row.get("confidence_estimate", assessment), "confidence_estimate")
            evidence_score = 0.70 * assessment + 0.20 * depth + 0.10 * confidence
            confidence_total += confidence * (recency_decay ** index)
            confidence_weight += recency_decay ** index
        else:
            evidence_score = assessment
        weight = recency_decay ** index
        weighted_total += evidence_score * weight
        weight_total += weight

    mastery = round(weighted_total / weight_total, 1)
    confidence = round(confidence_total / confidence_weight, 1) if confidence_weight else mastery
    status = "strong" if mastery >= 80 else "developing" if mastery >= 60 else "needs_revision"
    return MasteryResult(topic.strip(), mastery, confidence, len(rows), status)


def aggregate_subject_mastery(topic_scores: Mapping[str, float]) -> float:
    """Return the simple mean of assessed topic mastery scores (0-100)."""
    if not topic_scores:
        return 0.0
    scores = [_score(v, f"topic_scores[{k!r}]") for k, v in topic_scores.items()]
    return round(sum(scores) / len(scores), 1)
