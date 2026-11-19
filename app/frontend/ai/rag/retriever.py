from dataclasses import dataclass
import math


@dataclass(frozen=True)
class RetrievedChunk:
    text: str
    score: float
    metadata: dict


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Embedding vectors must have the same dimensions.")

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class InMemoryRetriever:
    """Temporary vector retriever.

    This is an integration adapter for the current project state. Member 3
    can replace it with PostgreSQL + pgvector without changing the AI service
    contract.
    """

    def __init__(self, chunks: list[tuple[str, list[float], dict]] | None = None):
        self._chunks = chunks or []

    def add(
        self,
        texts: list[str],
        embeddings: list[list[float]],
        metadata: list[dict],
    ) -> None:
        if not (len(texts) == len(embeddings) == len(metadata)):
            raise ValueError("texts, embeddings and metadata must have equal lengths.")
        self._chunks.extend(zip(texts, embeddings, metadata))

    def search(
        self,
        query_embedding: list[float],
        *,
        top_k: int = 5,
        min_similarity: float = 0.20,
        metadata_filter: dict | None = None,
    ) -> list[RetrievedChunk]:
        results: list[RetrievedChunk] = []

        for text, embedding, metadata in self._chunks:
            if metadata_filter and any(
                metadata.get(key) != value
                for key, value in metadata_filter.items()
            ):
                continue

            score = cosine_similarity(query_embedding, embedding)
            if score >= min_similarity:
                results.append(
                    RetrievedChunk(text=text, score=score, metadata=dict(metadata))
                )

        results.sort(key=lambda item: item.score, reverse=True)
        return results[:top_k]
