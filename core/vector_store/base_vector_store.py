from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseVectorStore(ABC):

    @abstractmethod
    def upsert(self, embeddings: List[Dict[str, Any]]) -> None:
        """
        Inserts or updates vector embeddings in the store.
        Each item in the list should contain:
          - 'id': unique string ID
          - 'embedding': List[float]
          - 'metadata': Dict with chunk details (like summary, file, etc.)
        """
        pass

    @abstractmethod
    def query(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Performs a similarity search with a given embedding vector.
        Returns a list of matched chunks and their metadata.
        """
        pass

    @abstractmethod
    def delete_collection(self) -> None:
        """
        Deletes the entire collection or namespace from the vector store.
        """
        pass
