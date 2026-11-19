
import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class AIConfig:
    """Configuration for the LearnMate AI engine."""

    api_key: str | None = os.getenv("GEMINI_API_KEY")

    model: str = os.getenv(
        "GEMINI_MODEL", "gemini-2.5-flash"
    )

    embedding_model: str = os.getenv(
        "GEMINI_EMBEDDING_MODEL", "gemini-embedding-001"
    )

    embedding_dimensions: int = int(
        os.getenv("GEMINI_EMBEDDING_DIMENSIONS", "768")
    )

    top_k: int = int(os.getenv("RAG_TOP_K", "5"))
    chunk_size: int = int(os.getenv("RAG_CHUNK_SIZE", "900"))
    chunk_overlap: int = int(os.getenv("RAG_CHUNK_OVERLAP", "120"))
    min_similarity: float = float(
        os.getenv("RAG_MIN_SIMILARITY", "0.20")
    )


def get_ai_config() -> AIConfig:
    return AIConfig()
