from abc import ABC, abstractmethod
from typing import List, Dict


class BaseChunkProcessor(ABC):
    @abstractmethod
    def process_chunk(self, chunk: Dict) -> Dict:
        """
        Accepts a single code chunk (with metadata) and returns enriched chunk data (e.g., summary, tags).
        """
        pass