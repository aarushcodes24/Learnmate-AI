from app.ai.providers.base import LLMProvider
from app.ai.rag.chunker import TextChunk, chunk_text
from app.ai.rag.retriever import InMemoryRetriever, RetrievedChunk


class RAGPipeline:
    """Upload -> clean -> chunk -> embed -> retrieve -> generate."""

    def __init__(
        self,
        provider: LLMProvider,
        retriever: InMemoryRetriever,
        *,
        chunk_size: int = 900,
        chunk_overlap: int = 120,
        top_k: int = 5,
        min_similarity: float = 0.20,
    ):
        self.provider = provider
        self.retriever = retriever
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k
        self.min_similarity = min_similarity

    def ingest_text(self, text: str, metadata: dict | None = None) -> list[TextChunk]:
        chunks = chunk_text(
            text,
            chunk_size=self.chunk_size,
            overlap=self.chunk_overlap,
            metadata=metadata,
        )
        if not chunks:
            return []

        embeddings = self.provider.embed([chunk.text for chunk in chunks])
        self.retriever.add(
            [chunk.text for chunk in chunks],
            embeddings,
            [chunk.metadata for chunk in chunks],
        )
        return chunks

    def retrieve(
        self,
        query: str,
        *,
        metadata_filter: dict | None = None,
    ) -> list[RetrievedChunk]:
        query_embedding = self.provider.embed([query])[0]
        return self.retriever.search(
            query_embedding,
            top_k=self.top_k,
            min_similarity=self.min_similarity,
            metadata_filter=metadata_filter,
        )

    def build_context(self, results: list[RetrievedChunk]) -> str:
        if not results:
            return "No relevant academic material was retrieved."

        blocks = []
        for index, result in enumerate(results, start=1):
            source = result.metadata.get("document_name", "unknown document")
            topic = result.metadata.get("topic", "unknown topic")
            blocks.append(
                f"[Source {index} | {source} | topic={topic} | "
                f"similarity={result.score:.3f}]\n{result.text}"
            )
        return "\n\n".join(blocks)
