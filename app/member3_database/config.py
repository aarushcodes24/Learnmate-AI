
"""Configuration for Member 3's PostgreSQL module."""
from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

# Locate the .env file in the main Learnmate-AI folder.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def database_url() -> str:
    """Return the configured PostgreSQL URL."""
    value = os.getenv("DATABASE_URL", "").strip()

    if not value:
        raise RuntimeError(
            "DATABASE_URL is not configured. Check your .env file."
        )

    return value
