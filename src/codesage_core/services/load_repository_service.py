"""Service layer for load_repository tool."""
from __future__ import annotations

from typing import Any, Dict

from codesage_core.services.github_mcp_service import GitHubMCPService


async def execute_load_repository(repo: str, default_branch: str = "main", github_user: str | None = None) -> Dict[str, Any]:
    """Load (stub) repository metadata using GitHub MCP service.

    The previous implementation relied on a removed `repository_overview` helper.
    We now approximate by searching for the repository via the MCP search tools.
    """
    service = GitHubMCPService()

    # Build a basic search query. If caller provided explicit owner separately,
    # use "repo:owner/name" syntax; otherwise just pass the repo string.
    owner = github_user
    if "/" in repo:  # repo might already be owner/name
        owner_part, name_part = repo.split("/", 1)
        owner = owner or owner_part
        repo_name = name_part
    else:
        repo_name = repo

    query = f"repo:{owner}/{repo_name}" if owner else repo_name
    search_result = await service.search_repositories(query=query)

    base: Dict[str, Any] = search_result if isinstance(search_result, dict) else {"source": "unknown", "result": search_result}

    # Create a lightweight manifest stub; real indexing handled elsewhere.
    manifest = {"files_indexed": 0, "languages": ["python"], "default_branch": default_branch}
    base.update({
        "repo": f"{owner}/{repo_name}" if owner else repo_name,
        "loaded": True,
        "manifest": manifest,
        "message": f"Repository '{repo}' load scheduled (stub).",
    })
    if github_user:
        base.setdefault("requested_user", github_user)
    return base
