from collections.abc import Sequence

from app.ai.config import AIConfig
from app.ai.providers.base import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI implementation of the shared LLM provider contract."""

    def __init__(self, config: AIConfig):
        if not config.api_key:
            raise ValueError(
                "OPENAI_API_KEY is missing. Add it to the environment before "
                "using the AI service."
            )
        from openai import OpenAI

        self.config = config
        self.client = OpenAI(api_key=config.api_key)

    def generate(self, instructions: str, user_input: str) -> str:
        response = self.client.responses.create(
            model=self.config.model,
            instructions=instructions,
            input=user_input,
        )
        return response.output_text.strip()

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []

        response = self.client.embeddings.create(
            model=self.config.embedding_model,
            input=list(texts),
            dimensions=self.config.embedding_dimensions,
        )
        ordered = sorted(response.data, key=lambda item: item.index)
        return [item.embedding for item in ordered]
