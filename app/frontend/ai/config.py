import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class AIConfig:
    """Configuration for the AI engine.

    Secrets are read from environment variables and never hard-coded.
    """

    api_key: str | None = os.getenv("OPENAI_API_KEY")
    model: str = os.getenv("OPENAI_MODEL", "gpt-5-mini")
    embedding_model: str = os.getenv(
        "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
    )
    embedding_dimensions: int = int(
        os.getenv("OPENAI_EMBEDDING_DIMENSIONS", "1536")
    )
    top_k: int = int(os.getenv("RAG_TOP_K", "5"))
    chunk_size: int = int(os.getenv("RAG_CHUNK_SIZE", "900"))
    chunk_overlap: int = int(os.getenv("RAG_CHUNK_OVERLAP", "120"))
    min_similarity: float = float(os.getenv("RAG_MIN_SIMILARITY", "0.20"))


def get_ai_config() -> AIConfig:
    return AIConfig()
