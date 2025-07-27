from abc import ABC, abstractmethod
from typing import List, Dict

class BaseLLMClient(ABC):
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """
        Sends the prompt to an LLM backend (e.g., OpenAI, Claude) and returns the output string.
        """
        pass