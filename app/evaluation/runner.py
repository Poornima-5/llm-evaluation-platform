import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from app.evaluation.evaluators.base import Evaluator
from app.evaluation.models import EvaluationReport, EvaluationResult, TestCase
from app.targets.base import Target


class EvaluationRunner:

    def __init__(self, target: Target, evaluator: Evaluator):
        self.target = target
        self.evaluator = evaluator

    def run(self, test_case: TestCase) -> EvaluationResult:
        """Run evaluation for a single test case."""
        response = self.target.generate(test_case.prompt)
        passed = self.evaluator.evaluate(response)

        return EvaluationResult(
            test_id=test_case.id,
            category=test_case.category,
            prompt=test_case.prompt,
            response=response,
            passed=passed,
            expected_behavior=test_case.expected_behavior,
        )

    def run_batch(
        self,
        test_cases: List[TestCase],
        output_path: Optional[Union[str, Path]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> EvaluationReport:
        """Run evaluation for a batch of test cases and generate a structured report."""
        results: List[EvaluationResult] = []
        for test_case in test_cases:
            result = self.run(test_case)
            results.append(result)

        total_tests = len(results)
        passed_tests = sum(1 for r in results if r.passed)
        failed_tests = total_tests - passed_tests
        pass_rate = round((passed_tests / total_tests) * 100, 2) if total_tests > 0 else 0.0

        target_name = getattr(self.target, "model", None) or self.target.__class__.__name__
        evaluator_name = self.evaluator.__class__.__name__

        run_metadata: Dict[str, Any] = {
            "target_class": self.target.__class__.__name__,
            "evaluator_class": evaluator_name,
        }
        if hasattr(self.target, "model"):
            run_metadata["model"] = getattr(self.target, "model")
        if metadata:
            run_metadata.update(metadata)

        report = EvaluationReport(
            timestamp=datetime.now(timezone.utc).isoformat(),
            target=target_name,
            evaluator=evaluator_name,
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            pass_rate=pass_rate,
            results=results,
            metadata=run_metadata,
        )

        if output_path is not None:
            self.save_report(report, output_path)

        return report

    @staticmethod
    def save_report(report: EvaluationReport, output_path: Union[str, Path]) -> Path:
        """Save an evaluation report to a JSON file."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, indent=2)
        return path