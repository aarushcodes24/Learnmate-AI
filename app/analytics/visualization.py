"""Reusable Plotly figures for the Student analytics dashboard."""
from __future__ import annotations
import pandas as pd
import plotly.express as px


def topic_mastery_chart(topic_frame: pd.DataFrame):
    """Build a horizontal topic mastery bar chart from build_topic_dataframe."""
    if topic_frame.empty:
        return None
    fig = px.bar(topic_frame, x="mastery_score", y="topic", color="subject", orientation="h",
                 range_x=[0, 100], labels={"mastery_score": "Mastery (%)", "topic": "Topic"},
                 hover_data=["confidence_score", "evidence_count", "status"])
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, legend_title_text="Subject")
    return fig


def progress_chart(progress_frame: pd.DataFrame):
    """Build a mastery-over-time line chart from build_progress_series."""
    if progress_frame.empty:
        return None
    fig = px.line(progress_frame, x="date", y="mastery", markers=True,
                   range_y=[0, 100], labels={"date": "Date", "mastery": "Mastery (%)"})
    return fig
