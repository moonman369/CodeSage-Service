"""Code understanding service.

Generates embeddings and retrieves relevant code chunks for a given query.
All heavy operations are currently stubbed with deterministic placeholder values.
"""
from __future__ import annotations

from typing import Any, Dict, List

DUMMY_EMBED_MODEL = "codesage-embed-mini-1"


def _stub_generate_embedding(text: str) -> List[float]:
    """Stub embedding generator.

    Produces a tiny pseudo-embedding based on character codes to keep deterministic.
    """
    base = sum(ord(ch) for ch in text) or 1
    return [round((base % p) / p, 5) for p in (101, 113, 127, 131)]


def _stub_fetch_repo_chunks(repo_path: str, top_k: int = 2) -> List[Dict[str, Any]]:
    """Stub retrieval of code chunks from a repository path.

    Parameters
    ----------
    repo_path: str
        Path to repository (unused in stub except echoed back).
    top_k: int
        Number of chunks to return.
    """
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
    """Process a code understanding request.

    Parameters
    ----------
    query: str
        Natural language question or description.
    repo_path: str
        Path to repository root.
    """
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
