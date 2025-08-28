# rag_engine/interface.py

from abc import ABC, abstractmethod
from typing import List, Dict


class BaseRAGEngine(ABC):
    @abstractmethod
    def generate_response(self, query: str, project_name: str) -> str:
        """Given a user query, return a response generated via RAG."""
        pass
