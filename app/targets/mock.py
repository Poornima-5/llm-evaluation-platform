from .base import Target


class MockTarget(Target):

    def __init__(self, response: str = "Mock response"):
        self.response = response

    def generate(self, prompt: str) -> str:
        return self.response