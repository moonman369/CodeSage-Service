"""FastMCP server entrypoint defining core CodeSage tools.

Async tools (scaffolded with TODOs):
    1. ping               - health check.
    2. code_understanding - embed + retrieve + generate answer about code.
    3. code_history       - metadata queries (commit / branch / PR) via external providers.
    4. hybrid_search      - combined metadata + code (RAG) search flow.
    5. config_info        - basic server configuration information.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List

from .services.ping_service import execute_ping
from .services.code_understanding_service import execute_code_understanding
from .services.code_history_service import execute_code_history
from .services.hybrid_search_service import execute_hybrid_search
from .services.config_info_service import execute_config_info

try:  # FastMCP availability
    from fastmcp import FastMCP
except ImportError as exc:  # pragma: no cover
    raise SystemExit("FastMCP not installed. Run `uv sync`.") from exc

logger = logging.getLogger("codesage_core.server")
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s:%(name)s: %(message)s")

SERVER_VERSION = "1.0"
TOOL_NAMES = [
    "ping",
    "code_understanding",
    "code_history",
    "hybrid_search",
    "config_info",
    "list_repos",
    "list_commits",
    "list_prs",
    "load_repository",
]


# In-memory store for transient metadata results (e.g., history of queries)
_history: List[Dict[str, Any]] = []


@asynccontextmanager
async def _lifespan(app: FastMCP):  # type: ignore[unused-ignore]
    await _startup()
    try:
        yield
    finally:
        await _shutdown()


app = FastMCP(
    name="codesage-core",
    version=SERVER_VERSION,
    instructions="CodeSage MCP: code understanding, metadata, hybrid search, config.",
    lifespan=_lifespan,
)


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@app.tool(description="Simple health-check tool.")
async def ping() -> Dict[str, Any]:
    """Delegate to ping service."""
    return execute_ping()


@app.tool(description="Embed query, retrieve code chunks, produce answer (scaffold).")
async def code_understanding(query: str, repo_path: str = "./") -> Dict[str, Any]:
    """Delegate to code understanding service."""
    result = execute_code_understanding(query, repo_path)
    _history.append({"timestamp": datetime.utcnow().isoformat() + "Z", "type": "code_understanding", "query": query})
    return result


@app.tool(description="Metadata queries for commits / branches / PRs (scaffold).")
async def code_history(query: str, type: str) -> Dict[str, Any]:  # noqa: A002
    """Delegate to code history service."""
    result = execute_code_history(query, {"type": type})
    _history.append({"timestamp": datetime.utcnow().isoformat() + "Z", "type": f"history:{type}", "query": query})
    return result


@app.tool(description="Hybrid query spanning metadata + code (scaffold).")
async def hybrid_search(query: str, type: str = "branch", repo_path: str = "./") -> Dict[str, Any]:
    """Delegate to hybrid search service."""
    result = execute_hybrid_search(query, {"type": type}, repo_path)
    _history.append({"timestamp": datetime.utcnow().isoformat() + "Z", "type": "hybrid_search", "query": query})
    return result


@app.tool(description="Return server configuration and environment info.")
async def config_info() -> Dict[str, Any]:
    """Delegate to config info service and augment with runtime counters."""
    base = execute_config_info()
    base.update({"history_items": len(_history), "tools": TOOL_NAMES})
    return base


# ---------------------------------------------------------------------------
# GitHub / Repository tools (placeholders)
# ---------------------------------------------------------------------------


@app.tool(description="List repositories accessible to the current user/session (placeholder).")
async def list_repos() -> Dict[str, Any]:
    """Return a placeholder list of repository names.

    TODO:
      - Integrate with GitHub MCP or other SCM provider
      - Support pagination / filtering
    """
    return {"repos": ["alpha", "beta", "gamma"], "source": "stub"}


@app.tool(description="List recent commits for a repository branch (placeholder).")
async def list_commits(repo: str, branch: str = "main", limit: int = 10) -> Dict[str, Any]:
    """Return a placeholder commit list for a repo/branch.

    Parameters
    ----------
    repo: repository name
    branch: branch to list commits from
    limit: maximum commits to return

    TODO:
      - Call GitHub MCP commit listing with pagination
      - Surface diff stats / authors
    """
    commits = [
        {
            "sha": f"deadbeef{i:02d}",
            "message": f"Stub commit message {i}",
            "author": "codesage-bot",
            "branch": branch,
            "repo": repo,
        }
        for i in range(min(limit, 5))
    ]
    return {"repo": repo, "branch": branch, "commits": commits, "returned": len(commits), "source": "stub"}


@app.tool(description="List pull requests for a repository (placeholder).")
async def list_prs(repo: str, state: str = "open", limit: int = 10) -> Dict[str, Any]:
    """Return a placeholder list of pull requests.

    Parameters
    ----------
    repo: repository name
    state: PR state filter (open/closed/merged)
    limit: max number of PRs

    TODO:
      - Integrate with GitHub MCP PR listing
      - Include reviewers / labels / mergeability
    """
    prs = [
        {
            "id": 100 + i,
            "title": f"Add feature {i}",
            "state": state,
            "repo": repo,
        }
        for i in range(min(limit, 3))
    ]
    return {"repo": repo, "state": state, "prs": prs, "returned": len(prs), "source": "stub"}


@app.tool(description="Load repository metadata to prepare for embeddings/code search (placeholder).")
async def load_repository(repo: str, default_branch: str = "main") -> Dict[str, Any]:
    """Simulate repository load and metadata preparation.

    TODO:
      - Clone / fetch repository if not present
      - Build file manifest + lightweight statistics
      - Kick off background embedding job
    """
    manifest = {
        "files_indexed": 0,  # placeholder until real indexing
        "languages": ["python"],  # stub
        "default_branch": default_branch,
    }
    return {
        "repo": repo,
        "loaded": True,
        "manifest": manifest,
        "message": f"Repository '{repo}' load scheduled (stub).",
        "source": "stub",
    }


# ---------------------------------------------------------------------------
# Lifecycle helpers
# ---------------------------------------------------------------------------


async def _startup() -> None:
    logger.info("Starting CodeSage MCP server (tools: %s)", ", ".join(TOOL_NAMES))
    await asyncio.sleep(0)


async def _shutdown() -> None:
    logger.info("Shutting down CodeSage MCP server")
    await asyncio.sleep(0)


# ---------------------------------------------------------------------------
# CLI Entry
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="Run CodeSage MCP Server")
    parser.add_argument("--transport", default=os.getenv("CODESAGE_MCP_TRANSPORT", "stdio"), help="stdio | http | sse | streamable-http")
    parser.add_argument("--host", default=os.getenv("CODESAGE_MCP_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.getenv("CODESAGE_MCP_PORT", "8000")))
    args = parser.parse_args()

    transport = args.transport.lower().strip()
    allowed = {"stdio", "http", "sse", "streamable-http"}
    if transport not in allowed:
        raise SystemExit(f"Invalid transport '{transport}'. Allowed: {', '.join(sorted(allowed))}")

    if transport == "stdio":
        app.run(transport="stdio")
    else:
        app.run(transport=transport, host=args.host, port=args.port)


if __name__ == "__main__":  # pragma: no cover
    main()
