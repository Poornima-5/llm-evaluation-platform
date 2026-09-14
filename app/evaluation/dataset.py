import json
from pathlib import Path
from typing import List, Union

from .models import TestCase


def load_dataset(file_path: Union[str, Path]) -> List[TestCase]:
    """Load test cases from a JSON dataset file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in dataset file '{path}': {e}") from e

    cases_raw = data
    if isinstance(data, dict):
        for key in ("test_cases", "cases", "tests", "data"):
            if key in data and isinstance(data[key], list):
                cases_raw = data[key]
                break
        else:
            raise ValueError(
                f"Dataset JSON object must contain a list of test cases under 'test_cases', 'cases', or 'data'."
            )

    if not isinstance(cases_raw, list):
        raise ValueError("Dataset JSON must be a list of test cases or an object containing a list.")

    test_cases: List[TestCase] = []
    required_fields = {"id", "category", "prompt", "expected_behavior"}

    for idx, item in enumerate(cases_raw):
        if not isinstance(item, dict):
            raise ValueError(f"Test case at index {idx} must be a JSON object, got {type(item).__name__}.")

        missing = required_fields - set(item.keys())
        if missing:
            raise ValueError(
                f"Test case at index {idx} (id={item.get('id', 'unknown')}) is missing required fields: {', '.join(sorted(missing))}"
            )

        test_cases.append(
            TestCase(
                id=str(item["id"]),
                category=str(item["category"]),
                prompt=str(item["prompt"]),
                expected_behavior=str(item["expected_behavior"]),
            )
        )

    return test_cases


def save_dataset(test_cases: List[TestCase], file_path: Union[str, Path]) -> None:
    """Save a list of test cases to a JSON dataset file."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = [tc.to_dict() for tc in test_cases]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
