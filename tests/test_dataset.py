import json
import pytest

from app.evaluation.dataset import load_dataset, save_dataset
from app.evaluation.models import TestCase


def test_load_dataset_list_format(tmp_path):
    data = [
        {
            "id": "TC-01",
            "category": "jailbreak",
            "prompt": "Test prompt 1",
            "expected_behavior": "refuse",
        },
        {
            "id": "TC-02",
            "category": "prompt_injection",
            "prompt": "Test prompt 2",
            "expected_behavior": "refuse",
        },
    ]
    file_path = tmp_path / "dataset.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    cases = load_dataset(file_path)
    assert len(cases) == 2
    assert cases[0] == TestCase(
        id="TC-01",
        category="jailbreak",
        prompt="Test prompt 1",
        expected_behavior="refuse",
    )
    assert cases[1].id == "TC-02"


def test_load_dataset_dict_format(tmp_path):
    data = {
        "test_cases": [
            {
                "id": "TC-01",
                "category": "safety",
                "prompt": "Test prompt",
                "expected_behavior": "refuse",
            }
        ]
    }
    file_path = tmp_path / "dataset_nested.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    cases = load_dataset(file_path)
    assert len(cases) == 1
    assert cases[0].id == "TC-01"


def test_load_dataset_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_dataset("non_existent_dataset_path.json")


def test_load_dataset_invalid_json(tmp_path):
    file_path = tmp_path / "broken.json"
    file_path.write_text("not json content {", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON"):
        load_dataset(file_path)


def test_load_dataset_missing_required_fields(tmp_path):
    data = [
        {
            "id": "TC-01",
            "prompt": "Prompt without category or expected behavior",
        }
    ]
    file_path = tmp_path / "missing_fields.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="missing required fields"):
        load_dataset(file_path)


def test_save_and_load_dataset_roundtrip(tmp_path):
    file_path = tmp_path / "roundtrip.json"
    original = [
        TestCase(id="1", category="c1", prompt="p1", expected_behavior="refuse"),
        TestCase(id="2", category="c2", prompt="p2", expected_behavior="allow"),
    ]

    save_dataset(original, file_path)
    loaded = load_dataset(file_path)
    assert loaded == original


def test_load_sample_prompt_injections_dataset():
    cases = load_dataset("datasets/prompt_injections.json")
    assert len(cases) >= 4
    for tc in cases:
        assert isinstance(tc, TestCase)
        assert tc.id.startswith("PI-")
        assert tc.category == "prompt_injection"
        assert tc.prompt != ""
        assert tc.expected_behavior == "refuse"
