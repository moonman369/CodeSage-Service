# core/embedder/base_embedder.py

from abc import ABC, abstractmethod
from typing import List

class BaseEmbedder(ABC):
    @abstractmethod
    def embed_chunks(self, chunks: List) -> List:
        """
        Takes a list of chunks, returns list of chunks with embedding vector added under key 'embedding'.
        """
        pass

    @abstractmethod
    def embed_chunks_from_file(self, json_file_path: str) -> List:
        """
        Loads chunks from JSON file, embeds them, returns updated chunks list.
        """
        pass
