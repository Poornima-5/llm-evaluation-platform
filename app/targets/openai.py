import os
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI

from .base import Target

# Load environment variables from .env if present
load_dotenv()


class OpenAITarget(Target):
    """OpenAI-compatible LLM target adapter implementing the Target interface."""

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: float = 0.0,
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Please provide api_key or set OPENAI_API_KEY in your environment or .env file."
            )

        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
        self.temperature = temperature

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    def generate(self, prompt: str) -> str:
        """Generate a response using the OpenAI Chat Completions API."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
        )
        choice = response.choices[0] if response.choices else None
        if choice and choice.message and choice.message.content:
            return choice.message.content
        return ""
