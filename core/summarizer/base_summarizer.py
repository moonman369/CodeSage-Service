# core/summarizer/base_summarizer.py

from abc import ABC, abstractmethod

class BaseSummarizer(ABC):
    @abstractmethod
    def summarize_repo(self, repo_path: str) -> str:
        pass

    @abstractmethod
    def summarize_directory(self, repo_path: str) -> str:
        pass
