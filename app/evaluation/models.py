from dataclasses import dataclass


@dataclass
class TestCase:
    id: str
    category: str
    prompt: str
    expected_behavior: str

@dataclass
class EvaluationResult:
    test_id: str
    category: str
    prompt: str
    response: str
    passed: bool