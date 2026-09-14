from abc import ABC, abstractmethod


class Evaluator(ABC):

    @abstractmethod
    def evaluate(self, response: str) -> bool:
        """Return True if the model response passes the evaluation."""
        raise NotImplementedError