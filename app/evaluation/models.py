from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List


@dataclass
class TestCase:
    __test__ = False

    id: str
    category: str
    prompt: str
    expected_behavior: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EvaluationResult:
    test_id: str
    category: str
    prompt: str
    response: str
    passed: bool
    expected_behavior: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EvaluationReport:
    timestamp: str
    target: str
    evaluator: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    pass_rate: float
    results: List[EvaluationResult] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)