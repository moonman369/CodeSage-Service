# rag_engine/interface.py

from abc import ABC, abstractmethod

class BaseRAGEngine(ABC):
    @abstractmethod
    def generate_response(self, query: str) -> str:
        """Given a user query, return a response generated via RAG."""
        pass
