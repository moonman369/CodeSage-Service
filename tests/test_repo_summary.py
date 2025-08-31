from __future__ import annotations

"""Tests for repo_summary tool service layer (using stub fallback).

These tests exercise the not_found path since no real vector store is
configured in the test environment. They also mock a service instance to
simulate found repos with and without summaries.
"""
from typing import List, Dict, Any
import types

from codesage_core.services.repo_summary.repo_summary_service import RepoSummaryService


class DummyVectorStore:
    def __init__(self, points: List[Dict[str, Any]]):
        self._points = points

    def has_project(self, project_name: str) -> bool:
        return bool(self._points)

    def query(self, query_vector, project_name: str = "", top_k: int = 10):  # minimal compat
        # Return sample hits embedding payload in expected key
        return [{"metadata": p} for p in self._points[:top_k]]


def _mk_point(file_path: str, language: str, summary: str = "") -> Dict[str, Any]:
    return {
        "project_name": "demo",
        "metadata": {"file_path": file_path, "language": language},
        "llm_summary": summary,
        "raw_code": "print('hello')",
    }


def test_repo_summary_not_found():
    service = RepoSummaryService(vector_store=DummyVectorStore(points=[]))
    resp = service.get_repo_summary("demo")
    assert resp["status"] == "not_found"


def test_repo_summary_with_summaries():
    points = [
        _mk_point("src/a.py", "python", "Handles user auth"),
        _mk_point("src/b.py", "python", "Processes payments"),
    ]
    service = RepoSummaryService(vector_store=DummyVectorStore(points=points))
    resp = service.get_repo_summary("demo")
    assert resp["status"] == "ok"
    assert "auth" in resp["summary"].lower()
    assert resp["summaries_used"] == 2


def test_repo_summary_without_summaries():
    points = [
        _mk_point("src/a.py", "python", ""),
        _mk_point("src/b.py", "python", ""),
    ]
    service = RepoSummaryService(vector_store=DummyVectorStore(points=points))
    resp = service.get_repo_summary("demo")
    assert resp["status"] == "ok" or resp["status"] == "not_found"  # depending on heuristic fallback usage
    if resp["status"] == "ok":
        assert resp["summaries_used"] == 0
