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
import json
import asyncio
import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List

from .services.ping.service import execute_ping
from .schemas.code_understanding import (
    CodeUnderstandingRequest,
    CodeUnderstandingResponse,
)
from .services.code_understanding.service_impl import CodeUnderstandingService
from .services.code_history.service import execute_code_history
from .services.hybrid_search.service import execute_hybrid_search
from .services.config_info.service import execute_config_info
from .services.github_mcp_service import GitHubMCPService  # TODO: move fully into services/github
from .services.repository.load_service import execute_load_repository
from .tools.repo_summary_tool import RepoSummaryTool

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
    "list_github_tools",
    "list_user_repos",
    "list_repos",
    "list_commits",
    "list_prs",
    "load_repository",
    "get_file_contents",
    "repo_summary",
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


_code_understanding_service = CodeUnderstandingService()
_repo_summary_tool = RepoSummaryTool()


@app.tool(description="Embed query, retrieve code chunks, produce answer about repository code.")
async def code_understanding(
    repo: str,
    query: str,
    context_files: List[str] | None = None,
    top_k: int = 5,
) -> Dict[str, Any]:
    """Main code understanding tool.

    Accepts validated parameters, executes service pipeline and returns
    response matching CodeUnderstandingResponse. Validation performed via the
    Pydantic request/response schemas to keep contract explicit.
    """
    req = CodeUnderstandingRequest(repo=repo, query=query, context_files=context_files, top_k=top_k)
    out = _code_understanding_service.handle(
        repo=req.repo,
        query=req.query,
        top_k=req.top_k,
        context_files=req.context_files,
    )
    # Handle not_found passthrough before strict schema validation
    if isinstance(out, dict) and out.get("status") == "not_found":
        _history.append({"timestamp": datetime.utcnow().isoformat() + "Z", "type": "code_understanding", "query": query})
        return out  # includes status + message
    resp = CodeUnderstandingResponse(**out)
    _history.append({"timestamp": datetime.utcnow().isoformat() + "Z", "type": "code_understanding", "query": query})
    return resp.model_dump()


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
# GitHub / Repository tools
# ---------------------------------------------------------------------------

_github_service = GitHubMCPService()


@app.tool(description="List all available GitHub MCP server tools (remote GitHub MCP capabilities).")
async def list_github_tools() -> Dict[str, Any]:
    return await _github_service.available_tools()


@app.tool(description="List repositories; optional github_user filters owner/namespace if supported.")
async def list_repos(github_user: str | None = None) -> Dict[str, Any]:
    if github_user:
        raw = await _github_service.search_repositories(query=f"user:{github_user}")
        # Attempt to parse JSON text payload into structured form for convenience
        if isinstance(raw, dict) and raw.get("source") == "github-mcp":
            inner = raw.get("result")
            parsed = _maybe_parse_mcp_text_json(inner)
            if parsed is not None:
                raw["parsed"] = parsed
        return raw
    # Fallback: require a user for now (GitHub search API needs a query)
    return {"source": "error", "tool": "list_repos", "error_type": "MissingParameter", "error_message": "github_user is required when using list_repos (use list_user_repos tool)"}


@app.tool(description="List repositories for a GitHub user with optional filters (language, topic, min_stars). Uses search_repositories under the hood.")
async def list_user_repos(
    user: str,
    language: str | None = None,
    topic: str | None = None,
    min_stars: int | None = None,
    page: int = 1,
    per_page: int = 30,
) -> Dict[str, Any]:
    if not user:
        return {"source": "error", "tool": "list_user_repos", "error_type": "MissingParameter", "error_message": "user is required"}
    if page < 1:
        return {"source": "error", "tool": "list_user_repos", "error_type": "ValidationError", "error_message": "page must be >= 1"}
    if per_page < 1 or per_page > 100:
        return {"source": "error", "tool": "list_user_repos", "error_type": "ValidationError", "error_message": "per_page must be between 1 and 100"}
    query_parts = [f"user:{user}"]
    if language:
        query_parts.append(f"language:{language}")
    if topic:
        query_parts.append(f"topic:{topic}")
    if min_stars is not None and min_stars >= 0:
        query_parts.append(f"stars:>={min_stars}")
    params: Dict[str, Any] = {"query": " ".join(query_parts), "page": page, "perPage": per_page}
    raw = await _github_service.search_repositories(**params)
    if isinstance(raw, dict) and raw.get("source") == "github-mcp":
        inner = raw.get("result")
        parsed = _maybe_parse_mcp_text_json(inner)
        if parsed is not None:
            raw["parsed"] = parsed
    return raw


# ---------------------------------------------------------------------------
# Helper: attempt to parse a typical MCP text-only JSON tool response
# ---------------------------------------------------------------------------

def _maybe_parse_mcp_text_json(obj: Any):  # noqa: D401
    """If the MCP tool response uses content[0].text containing JSON, parse it.

    Returns parsed JSON (dict/list) or None if not parseable.
    """
    try:
        if isinstance(obj, dict) and isinstance(obj.get("content"), list) and obj["content"]:
            first = obj["content"][0]
            if isinstance(first, dict) and first.get("type") == "text" and isinstance(first.get("text"), str):
                txt = first["text"].strip()
                if txt.startswith("{") or txt.startswith("["):
                    return json.loads(txt)
    except Exception:
        return None
    return None


@app.tool(description="List recent commits for a repository branch; optional github_user scope.")
async def list_commits(repo: str, branch: str = "main", limit: int = 10, github_user: str | None = None) -> Dict[str, Any]:
    return await _github_service.list_commits(repo=repo, branch=branch, limit=limit, owner=github_user)


@app.tool(description="List pull requests for a repository; optional github_user scope.")
async def list_prs(repo: str, state: str = "open", limit: int = 10, github_user: str | None = None) -> Dict[str, Any]:
    return await _github_service.list_pull_requests(repo=repo, state=state, limit=limit, owner=github_user)


@app.tool(description="Load repository metadata; optional github_user scope.")
async def load_repository(repo: str, default_branch: str = "main", github_user: str | None = None) -> Dict[str, Any]:
    return await execute_load_repository(repo, default_branch=default_branch, github_user=github_user)


@app.tool(description="Get file or directory contents from a GitHub repository (delegates to GitHub MCP get_file_contents).")
async def get_file_contents(repo: str, path: str, ref: str = "main", github_user: str | None = None) -> Dict[str, Any]:
    # Delegate directly; param names align with typical GitHub conventions.
    return await _github_service.get_file_contents(owner=github_user, repo=repo, path=path, ref=ref)


@app.tool(name="repo_summary", description="Generates a high-level summary or structure of the repository. Accepts optional semantic prompt to tailor summary.")
async def repo_summary(project_name: str, structure: bool = False, prompt: str | None = None) -> Dict[str, Any]:
    """Return repo-wide summary or structure.

    Parameters:
        project_name: repository identifier (matches vector store project_name)
        structure: if True, return hierarchical file structure else semantic summary
    """
    if not project_name:
        return {"status": "error", "error_type": "ValidationError", "message": "project_name is required"}
    if structure:
        return _repo_summary_tool.getRepoStructure(project_name)
    return _repo_summary_tool.getRepoSummary(project_name, prompt=prompt)


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
