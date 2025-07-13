from abc import ABC, abstractmethod
from typing import List, Dict


class BaseChunker(ABC):
    @abstractmethod
    def chunk(self, markdown_digest: str) -> List[Dict]:
        """
        Given a markdown-formatted code digest, return a list of chunked code blocks
        with associated metadata.
        """
        pass
