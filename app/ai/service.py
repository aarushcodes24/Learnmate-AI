from dataclasses import dataclass

from app.ai.config import AIConfig, get_ai_config
from app.ai.content_generation import (
    generate_flashcards,
    generate_important_questions,
    generate_quiz,
)
from app.ai.prompts import TUTOR_INSTRUCTIONS
from app.ai.providers.gemini_provider import GeminiProvider
from app.ai.rag import InMemoryRetriever, RAGPipeline
from app.ai.rag.retriever import RetrievedChunk
from app.ai.student_analysis import StudentAnalysis, analyse_student_response


@dataclass(frozen=True)
class TutorResponse:
    answer: str
    sources: list[RetrievedChunk]


class LearnMateAI:
    """Facade used by the Streamlit layer.

    Member 1 should call this class instead of importing provider/RAG internals.
    Member 3 can later replace the retriever with a persistent pgvector
    implementation behind the same pipeline contract.
    """

    def __init__(self, config: AIConfig | None = None):
        self.config = config or get_ai_config()
        self.provider = GeminiProvider(
        api_key=self.config.api_key,
        model=self.config.model,
        embedding_model=self.config.embedding_model,
        embedding_dimensions=self.config.embedding_dimensions,
)
        self.retriever = InMemoryRetriever()
        self.rag = RAGPipeline(
            self.provider,
            self.retriever,
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
            top_k=self.config.top_k,
            min_similarity=self.config.min_similarity,
        )

    def ingest_text(self, text: str, metadata: dict | None = None) -> int:
        return len(self.rag.ingest_text(text, metadata))


    def ask(
        self,
        question: str,
        *,
        subject: str,
        topic: str | None = None,
        syllabus_context: str | None = None,
        metadata_filter: dict | None = None,
    ) -> TutorResponse:
        if not question.strip():
            raise ValueError("question cannot be empty.")

        filter_data = dict(metadata_filter or {})
        if subject:
            filter_data.setdefault("subject", subject)
        if topic:
            filter_data.setdefault("topic", topic)

        print("DEBUG 1: Starting retrieval", flush=True)
        results = self.rag.retrieve(question, metadata_filter=filter_data)
        print(f"DEBUG 2: Retrieval complete. Chunks: {len(results)}", flush=True)

        context = self.rag.build_context(results)
        print("DEBUG 3: Context built", flush=True)

        if syllabus_context:
            context = f"SYLLABUS SCOPE:\n{syllabus_context}\n\nRETRIEVED MATERIAL:\n{context}"

        user_input = f"""
Subject: {subject}
Topic: {topic or "not specified"}

Student question:
{question}

Academic context:
{context}
""".strip()

        print("DEBUG 4: Sending to Gemini", flush=True)
        answer = self.provider.generate(TUTOR_INSTRUCTIONS, user_input)
        print("DEBUG 5: Gemini response received", flush=True)

        return TutorResponse(answer=answer, sources=results)


    def analyse_response(
        self,
        *,
        topic: str,
        question: str,
        student_answer: str,
        expected_context: str,
    ) -> StudentAnalysis:
        return analyse_student_response(
            self.provider,
            topic=topic,
            question=question,
            student_answer=student_answer,
            expected_context=expected_context,
        )

    def create_quiz(self, context: str, count: int = 5):
        return generate_quiz(self.provider, context=context, count=count)

    def create_flashcards(self, context: str, count: int = 8):
        return generate_flashcards(self.provider, context=context, count=count)

    def create_important_questions(self, context: str, count: int = 8):
        return generate_important_questions(
            self.provider, context=context, count=count
        )
