"""Hybrid search service (relocated)."""
from __future__ import annotations
from typing import Any, Dict
from codesage_core.services.code_history.service import execute_code_history
from codesage_core.services.code_understanding.service import execute_code_understanding

def execute_hybrid_search(query: str, metadata: Dict[str, Any], repo_path: str) -> Dict[str, Any]:
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

__all__ = ["execute_hybrid_search"]
