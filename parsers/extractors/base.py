# parsers/extractors/base.py

from abc import ABC, abstractmethod
from tree_sitter import Node

class BaseExtractor(ABC):
    @abstractmethod
    def supports(self, language: str) -> bool:
        pass

    @abstractmethod
    def extract(self, root_node: Node, source_code: str) -> list[dict]:
        pass
 