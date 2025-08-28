"""Code understanding service (relocated)."""
from __future__ import annotations
from typing import Any, Dict, List

DUMMY_EMBED_MODEL = "codesage-embed-mini-1"

def _stub_generate_embedding(text: str) -> List[float]:
    base = sum(ord(ch) for ch in text) or 1
    return [round((base % p) / p, 5) for p in (101, 113, 127, 131)]

def _stub_fetch_repo_chunks(repo_path: str, top_k: int = 2) -> List[Dict[str, Any]]:
    return [
        {
            "id": f"chunk-{i}",
            "path": f"{repo_path}/module_{i}.py",
            "content": "def placeholder(): ...",
            "score": 0.9 - i * 0.05,
        }
        for i in range(top_k)
    ]

def execute_code_understanding(query: str, repo_path: str) -> Dict[str, Any]:
    embedding = _stub_generate_embedding(query)
    chunks = _stub_fetch_repo_chunks(repo_path)
    return {
        "query": query,
        "repo_path": repo_path,
        "embedding_model": DUMMY_EMBED_MODEL,
        "embedding": embedding,
        "relevant_chunks": chunks,
        "note": "Stub implementation - replace with real embedding + vector search pipeline.",
    }

__all__ = ["execute_code_understanding"]
