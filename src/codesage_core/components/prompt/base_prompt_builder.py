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
    def build_prompt_rag(
        self,
        user_query: str,
        retrieved_chunks: List[Dict],
        system_prompt: str = "You are a helpful AI assistant that understands code and answers queries precisely.",
        max_context_chars: int = 4000,
    ) -> str:
        """
        Builds an LLM-friendly prompt from the given chunk.
        """
        pass
