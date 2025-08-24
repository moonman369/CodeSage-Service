"""Code history service.

Interfaces with VCS / GitHub metadata (stubbed).
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict


def _stub_commit_query(query: str) -> Dict[str, Any]:
    return {
        "commits": [
            {
                "sha": "abc123",
                "summary": "Fix bug in core module",
                "files_changed": 3,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ],
        "query": query,
    }


def _stub_branch_query(query: str) -> Dict[str, Any]:
    return {"branches": ["main", "develop", "feature/refactor"], "query": query}


def _stub_pr_query(query: str) -> Dict[str, Any]:
    return {
        "prs": [
            {
                "id": 42,
                "title": "Add new feature",
                "state": "open",
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
        ],
        "query": query,
    }


def execute_code_history(query: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Handle a metadata query (commit / branch / PR).

    Parameters
    ----------
    query: str
        User-provided filter or keyword.
    metadata: dict
        Must contain key 'type' with one of commit|branch|PR.
    """
    kind_raw = metadata.get("type", "").lower().strip()
    if kind_raw not in {"commit", "branch", "pr"}:
        return {"error": "metadata.type must be one of: commit, branch, PR"}

    if kind_raw == "commit":
        data = _stub_commit_query(query)
        summary = "Returned 1 mock commit."
    elif kind_raw == "branch":
        data = _stub_branch_query(query)
        summary = "Returned 3 mock branches."
    else:
        data = _stub_pr_query(query)
        summary = "Returned 1 mock PR."

    return {"type": kind_raw, "query": query, "data": data, "summary": summary, "note": "Stub code history."}
