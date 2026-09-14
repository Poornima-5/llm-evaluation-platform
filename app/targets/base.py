from abc import ABC, abstractmethod


class Target(ABC):
    """Interface for any LLM that can be evaluated."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a response for the given prompt."""
        raise NotImplementedError