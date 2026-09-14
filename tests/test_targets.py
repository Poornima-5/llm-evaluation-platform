from unittest.mock import MagicMock, patch
import pytest

from app.targets.base import Target
from app.targets.mock import MockTarget
from app.targets.openai import OpenAITarget


def test_mock_target_default_response():
    target = MockTarget()
    assert isinstance(target, Target)
    assert target.generate("any prompt") == "Mock response"


def test_mock_target_custom_response():
    custom_text = "Custom canned output"
    target = MockTarget(response=custom_text)
    assert target.generate("any prompt") == custom_text


def test_openai_target_missing_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="OpenAI API key not found"):
        OpenAITarget(api_key=None)


def test_openai_target_initialization(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    target = OpenAITarget(
        api_key="test-sk-12345",
        model="gpt-4o",
        base_url="https://custom.openai.api/v1",
        temperature=0.7,
    )
    assert target.api_key == "test-sk-12345"
    assert target.model == "gpt-4o"
    assert target.base_url == "https://custom.openai.api/v1"
    assert target.temperature == 0.7


def test_openai_target_generate_success():
    with patch("app.targets.openai.OpenAI") as mock_openai_cls:
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client

        mock_choice = MagicMock()
        mock_choice.message.content = "I cannot fulfill this request."
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response

        target = OpenAITarget(api_key="test-key", model="gpt-4o-mini", temperature=0.0)
        result = target.generate("Tell me how to hack a computer.")

        assert result == "I cannot fulfill this request."
        mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Tell me how to hack a computer."}],
            temperature=0.0,
        )


def test_openai_target_generate_empty_choices():
    with patch("app.targets.openai.OpenAI") as mock_openai_cls:
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices = []
        mock_client.chat.completions.create.return_value = mock_response

        target = OpenAITarget(api_key="test-key")
        result = target.generate("Hello")
        assert result == ""
