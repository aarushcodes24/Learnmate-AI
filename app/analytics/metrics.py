"""Tabular analytics transformations for dashboards and charts."""
from __future__ import annotations
from typing import Iterable, Mapping, Any
import pandas as pd


def build_topic_dataframe(topic_rows: Iterable[Mapping[str, Any]]) -> pd.DataFrame:
    """Normalize topic records into dashboard-ready columns.

    Expected fields: subject, topic, mastery_score; optional confidence_score,
    evidence_count, status. Missing optional values remain missing in the frame.
    """
    frame = pd.DataFrame(list(topic_rows))
    columns = ["subject", "topic", "mastery_score", "confidence_score", "evidence_count", "status"]
    if frame.empty:
        return pd.DataFrame(columns=columns)
    required = {"topic", "mastery_score"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"topic rows missing required fields: {', '.join(sorted(missing))}")
    if "subject" not in frame:
        frame["subject"] = "Unassigned"
    for column in columns:
        if column not in frame:
            frame[column] = pd.NA
    frame["mastery_score"] = pd.to_numeric(frame["mastery_score"], errors="raise")
    if not frame["mastery_score"].between(0, 100).all():
        raise ValueError("mastery_score values must be between 0 and 100")
    frame["confidence_score"] = pd.to_numeric(frame["confidence_score"], errors="coerce")
    frame["evidence_count"] = pd.to_numeric(frame["evidence_count"], errors="coerce")
    return frame[columns].sort_values(["subject", "mastery_score", "topic"], ascending=[True, True, True]).reset_index(drop=True)


def build_progress_series(events: Iterable[Mapping[str, Any]]) -> pd.DataFrame:
    """Aggregate dated mastery snapshots to one mean per day.

    Each event contains ``date`` and ``mastery_score`` (0-100). Duplicate
    snapshots on a day are averaged. Returns columns ``date`` and ``mastery``.
    """
    frame = pd.DataFrame(list(events))
    if frame.empty:
        return pd.DataFrame(columns=["date", "mastery"])
    if not {"date", "mastery_score"}.issubset(frame.columns):
        raise ValueError("events require date and mastery_score fields")
    frame["date"] = pd.to_datetime(frame["date"], errors="raise", utc=True).dt.date
    frame["mastery_score"] = pd.to_numeric(frame["mastery_score"], errors="raise")
    if not frame["mastery_score"].between(0, 100).all():
        raise ValueError("mastery_score values must be between 0 and 100")
    return (frame.groupby("date", as_index=False)["mastery_score"].mean()
            .rename(columns={"mastery_score": "mastery"}).sort_values("date").reset_index(drop=True))
