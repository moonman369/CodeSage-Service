"""Hybrid search service.

Combines code history and code understanding outputs into a merged response (stub).
"""
from __future__ import annotations

from typing import Any, Dict

from .code_history_service import execute_code_history
from .code_understanding_service import execute_code_understanding


def execute_hybrid_search(query: str, metadata: Dict[str, Any], repo_path: str) -> Dict[str, Any]:
    """Perform a hybrid search across metadata and code.

    Steps:
      1. Get metadata slice (commit / branch / PR) via code history service.
      2. Run code understanding for contextual code chunks.
      3. Merge and provide a synthesized placeholder summary.
    """
    history_part = execute_code_history(query, metadata)
    code_part = execute_code_understanding(query, repo_path)

    merged_summary = (
        "Hybrid summary (stub): combined "
        f"history type={history_part.get('type')} with {len(code_part.get('relevant_chunks', []))} code chunks."
    )

    return {
        "query": query,
        "metadata_type": history_part.get("type"),
        "history": history_part,
        "code": code_part,
        "summary": merged_summary,
        "note": "Stub hybrid search - add ranking fusion + LLM reasoning later.",
    }
