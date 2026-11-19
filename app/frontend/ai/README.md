# Member 2 — AI Engine

This package owns the AI layer of LearnMate AI.

## Responsibilities

- LLM/provider abstraction
- syllabus-grounded tutor responses
- RAG chunking, embeddings and retrieval
- student-response diagnostics
- adaptive teaching decision data
- quiz generation
- flashcard generation
- important-question generation
- AI evaluation/smoke tests

## Integration contract

Member 1 should use:

```python
from app.ai.service import LearnMateAI

ai = LearnMateAI()

ai.ingest_text(
    document_text,
    metadata={
        "user_id": "...",
        "course_id": "...",
        "subject": "Python Programming",
        "topic": "Functions",
        "document_name": "teacher_notes.pdf",
        "document_type": "teacher_notes",
    },
)

response = ai.ask(
    "Explain recursion simply.",
    subject="Python Programming",
    topic="Functions",
)
print(response.answer)
```

Do not import `OpenAIProvider`, prompts, or the retriever from Streamlit pages.
The service facade is the boundary.

## Current persistence adapter

`InMemoryRetriever` is intentionally temporary. It proves the AI/RAG pipeline
without taking over Member 3's PostgreSQL/pgvector responsibility.

Member 3 should later implement a persistent retriever that preserves the
metadata and search contract.

## Environment

Add:

- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `OPENAI_EMBEDDING_MODEL`
- `OPENAI_EMBEDDING_DIMENSIONS`
- `RAG_TOP_K`
- `RAG_CHUNK_SIZE`
- `RAG_CHUNK_OVERLAP`
- `RAG_MIN_SIMILARITY`

Never commit the real API key.
