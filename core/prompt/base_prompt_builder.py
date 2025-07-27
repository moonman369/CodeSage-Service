from abc import ABC, abstractmethod
from typing import List, Dict

class BasePromptBuilder(ABC):
    @abstractmethod
    def build_prompt_chunk(self, chunk: Dict) -> str:
        """
        Builds an LLM-friendly prompt from the given chunk.
        """
        pass

    @abstractmethod
    def build_prompt_rag(self, chunk: Dict) -> str:
        """
        Builds an LLM-friendly prompt from the given chunk.
        """
        pass