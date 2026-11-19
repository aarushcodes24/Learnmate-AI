from app.ai.rag.chunker import chunk_text
from app.ai.rag.retriever import InMemoryRetriever, cosine_similarity


def test_chunk_text_has_overlap_and_metadata():
    text = "A" * 1500
    chunks = chunk_text(text, chunk_size=500, overlap=100, metadata={"topic": "X"})

    assert len(chunks) >= 3
    assert chunks[0].metadata["topic"] == "X"
    assert chunks[0].metadata["chunk_index"] == 0


def test_cosine_similarity():
    assert cosine_similarity([1.0, 0.0], [1.0, 0.0]) == 1.0
    assert cosine_similarity([1.0, 0.0], [0.0, 1.0]) == 0.0


def test_retriever_filters_and_ranks():
    retriever = InMemoryRetriever()
    retriever.add(
        ["python loop", "matrix algebra"],
        [[1.0, 0.0], [0.0, 1.0]],
        [{"subject": "Python"}, {"subject": "Math"}],
    )

    results = retriever.search(
        [1.0, 0.0],
        top_k=1,
        min_similarity=0.1,
        metadata_filter={"subject": "Python"},
    )

    assert len(results) == 1
    assert results[0].text == "python loop"
