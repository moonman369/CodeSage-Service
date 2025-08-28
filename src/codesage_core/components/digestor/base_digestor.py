# core/summarizer/base_summarizer.py

from abc import ABC, abstractmethod

class BaseDigestor(ABC):
    @abstractmethod
    def digest_repo(self, repo_path: str) -> str:
        pass

    @abstractmethod
    def digest_directory(self, repo_path: str) -> str:
        pass
