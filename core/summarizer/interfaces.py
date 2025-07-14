from abc import ABC, abstractmethod
from typing import List, Dict


class ChunkProcessorInterface(ABC):
    @abstractmethod
    def process_chunk(self, chunk: Dict) -> Dict:
        """
        Accepts a single code chunk (with metadata) and returns enriched chunk data (e.g., summary, tags).
        """
        pass


class PromptBuilderInterface(ABC):
    @abstractmethod
    def build_prompt(self, chunk: Dict) -> str:
        """
        Builds an LLM-friendly prompt from the given chunk.
        """
        pass


class LLMClientInterface(ABC):
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """
        Sends the prompt to an LLM backend (e.g., OpenAI, Claude) and returns the output string.
        """
        pass
