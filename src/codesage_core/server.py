"""Minimal FastMCP server exposing core CodeSage tools.

Implements the following MCP tools (all async) with mocked logic:
1. ping              -> health check; echoes back the provided message prefixed with 'pong:'.
2. code_understanding -> naive summarization of a code snippet.
3. code_history      -> session-scoped history add/get store.
4. hybrid_search     -> mock hybrid search returning static ranked results.
5. config_info       -> returns mock configuration / environment information.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List

try:
    from fastmcp import FastMCP
except ImportError as exc:  # pragma: no cover
    raise SystemExit("FastMCP not installed. Run `uv sync` to install dependencies.") from exc

logger = logging.getLogger("codesage_core.server")
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s:%(name)s: %(message)s")

__version__ = "0.1.0"

# In-memory session history store
_history: List[Dict[str, Any]] = []


@asynccontextmanager
async def _lifespan(app: FastMCP):  # type: ignore[unused-ignore]
    """Manage startup and shutdown for the FastMCP app."""
    await _startup()
    try:
        yield
    finally:
        await _shutdown()


app = FastMCP(
    name="codesage-core",
    version=__version__,
    instructions="CodeSage Core MCP Server: diagnostics, code understanding, history, hybrid search, config info.",
    lifespan=_lifespan,
)


# ---------------------------------------------------------------------------
# Tool Implementations
# ---------------------------------------------------------------------------


@app.tool(description="Health check tool: echo back 'pong: <message>'.")
async def ping(message: str) -> Dict[str, str]:
    """Echo a message with a pong prefix."""
    return {"reply": f"pong: {message}"}


@app.tool(description="Analyze and summarize a code snippet (naive heuristic).")
async def code_understanding(code: str) -> Dict[str, str]:
    """Return a short natural language summary of the given code block.

    Heuristic summary inspects:
      - number of lines
      - presence of class / def / import keywords
    """
    lines = [l.rstrip() for l in code.splitlines() if l.strip()]
    line_count = len(lines)
    keywords = {
        "classes": sum(1 for l in lines if l.lstrip().startswith("class ")),
        "functions": sum(1 for l in lines if l.lstrip().startswith("def ")),
        "imports": sum(1 for l in lines if l.lstrip().startswith("import ") or l.lstrip().startswith("from ")),
    }
    parts = [f"~{line_count} lines"]
    if keywords["classes"]:
        parts.append(f"{keywords['classes']} class(es)")
    if keywords["functions"]:
        parts.append(f"{keywords['functions']} function(s)")
    if keywords["imports"]:
        parts.append(f"{keywords['imports']} import(s)")
    summary = "Code snippet containing " + ", ".join(parts) + "."
    return {"summary": summary}


@app.tool(description="Track or retrieve session history items.")
async def code_history(action: str, message: str | None = None) -> Dict[str, Any]:
    """Maintain an in-memory list of history records for the session.

    Parameters
    ----------
    action: 'add' or 'get'
        Operation to perform.
    message: optional string
        Message to store when action='add'.
    """
    action_norm = action.lower().strip()
    if action_norm not in {"add", "get"}:
        return {"error": "Invalid action. Use 'add' or 'get'."}
    if action_norm == "add":
        if not message:
            return {"error": "message is required when action='add'"}
        record = {"timestamp": datetime.utcnow().isoformat() + "Z", "message": message}
        _history.append(record)
        return {"status": "added", "total": len(_history)}
    # get
    return {"history": list(_history)}


@app.tool(description="Perform a mock hybrid (keyword + embedding) search.")
async def hybrid_search(query: str) -> Dict[str, Any]:
    """Return static top matches for the provided query."""
    # In a real implementation, we'd combine vector similarity + keyword ranking.
    mock_results = [
        {"id": "R1", "score": 0.91, "snippet": "def foo(): pass", "match_reason": "function name"},
        {"id": "R2", "score": 0.83, "snippet": "class Bar:", "match_reason": "class definition"},
        {"id": "R3", "score": 0.78, "snippet": "import os", "match_reason": "import usage"},
    ]
    return {"query": query, "results": mock_results[:3]}


@app.tool(description="Return mock server configuration / environment info.")
async def config_info() -> Dict[str, Any]:  # no input
    """Return sample configuration details."""
    return {
        "version": __version__,
        "environment": os.getenv("CODESAGE_ENV", "dev"),
        "history_items": len(_history),
        "tools": ["ping", "code_understanding", "code_history", "hybrid_search", "config_info"],
    }


# ---------------------------------------------------------------------------
# Lifecycle helpers
# ---------------------------------------------------------------------------


async def _startup() -> None:
    logger.info("Starting CodeSage Core MCP server (tools registered: ping, code_understanding, code_history, hybrid_search, config_info)")
    await asyncio.sleep(0)


async def _shutdown() -> None:
    logger.info("Shutting down CodeSage Core MCP server")
    await asyncio.sleep(0)


# ---------------------------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------------------------


def main() -> None:
    """Launch the MCP server selecting a transport (default stdio)."""
    parser = argparse.ArgumentParser(description="Run CodeSage Core MCP Server")
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
