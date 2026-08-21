from app.evaluation.evaluators.base import Evaluator
from app.evaluation.models import EvaluationResult, TestCase
from app.targets.base import Target


class EvaluationRunner:

    def __init__(self, target: Target, evaluator: Evaluator):
        self.target = target
        self.evaluator = evaluator

    def run(self, test_case: TestCase) -> EvaluationResult:
        response = self.target.generate(test_case.prompt)

        passed = self.evaluator.evaluate(response)

        return EvaluationResult(
            test_id=test_case.id,
            category=test_case.category,
            prompt=test_case.prompt,
            response=response,
            passed=passed,
        )