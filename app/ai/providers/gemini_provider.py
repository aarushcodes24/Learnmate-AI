import os
from collections.abc import Sequence

from google import genai
from google.genai import types

from app.ai.providers.base import LLMProvider


class GeminiProvider(LLMProvider):
    """Gemini implementation of the LearnMate LLM provider."""

    def __init__(
        self,
        api_key=None,
        model=None,
        embedding_model=None,
        embedding_dimensions=None,
    ):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. Add it to your .env file."
            )

        self.model = model or os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash",
        )

        self.embedding_model = embedding_model or os.getenv(
            "GEMINI_EMBEDDING_MODEL",
            "gemini-embedding-001",
        )

        self.embedding_dimensions = int(
            embedding_dimensions
            or os.getenv("GEMINI_EMBEDDING_DIMENSIONS", "768")
        )

        self.client = genai.Client(api_key=self.api_key)

    def generate(self, instructions: str, user_input: str) -> str:
        """Generate a response using Gemini."""

        response = self.client.models.generate_content(
            model=self.model,
            contents=user_input,
            config=types.GenerateContentConfig(
                system_instruction=instructions,
            ),
        )

        if not response.text:
            raise RuntimeError("Gemini returned an empty response.")

        return response.text

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        """Generate embeddings for text."""

        if not texts:
            return []

        embeddings = []

        for text in texts:
            response = self.client.models.embed_content(
                model=self.embedding_model,
                contents=text,
                config=types.EmbedContentConfig(
                    output_dimensionality=self.embedding_dimensions,
                ),
            )

            embeddings.append(response.embeddings[0].values)

        return embeddings