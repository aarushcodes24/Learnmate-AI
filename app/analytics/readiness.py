"""Exam-readiness estimation from syllabus coverage and topic mastery."""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite
from typing import Mapping


@dataclass(frozen=True)
class ReadinessResult:
    readiness_score: float
    coverage_percent: float
    assessed_topics: int
    total_topics: int
    band: str
    unassessed_topics: tuple[str, ...]


def calculate_exam_readiness(
    topic_mastery: Mapping[str, float | None],
    *,
    topic_weights: Mapping[str, float] | None = None,
    coverage_weight: float = 0.25,
) -> ReadinessResult:
    """Estimate readiness as 75% weighted mastery + 25% syllabus coverage.

    ``None`` mastery means unassessed. Such topics contribute zero mastery and
    zero coverage, preventing a high score on a few topics from hiding gaps.
    Optional positive topic weights can represent syllabus importance.
    """
    if not 0 <= coverage_weight <= 1:
        raise ValueError("coverage_weight must be between 0 and 1")
    names = list(topic_mastery)
    if not names:
        return ReadinessResult(0.0, 0.0, 0, 0, "not_assessed", ())
    weights = topic_weights or {}
    weighted_sum = total_weight = 0.0
    assessed = 0
    unassessed = []
    for name, value in topic_mastery.items():
        weight = float(weights.get(name, 1.0))
        if not isfinite(weight) or weight <= 0:
            raise ValueError(f"topic weight for {name!r} must be positive")
        total_weight += weight
        if value is None:
            unassessed.append(name)
            continue
        score = float(value)
        if not isfinite(score) or not 0 <= score <= 100:
            raise ValueError(f"mastery for {name!r} must be between 0 and 100")
        assessed += 1
        weighted_sum += score * weight
    coverage = 100 * assessed / len(names)
    weighted_mastery = weighted_sum / total_weight
    readiness = round((1 - coverage_weight) * weighted_mastery + coverage_weight * coverage, 1)
    band = "exam_ready" if readiness >= 80 and not unassessed else "on_track" if readiness >= 60 else "needs_preparation"
    return ReadinessResult(round(readiness, 1), round(coverage, 1), assessed, len(names), band, tuple(unassessed))
