from abc import ABC, abstractmethod
from collections.abc import Sequence


class LLMProvider(ABC):
    """Provider contract used by the rest of the AI engine.

    Member 1 and other modules should depend on this interface, not directly
    on an LLM vendor SDK.
    """

    @abstractmethod
    def generate(self, instructions: str, user_input: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        raise NotImplementedError
