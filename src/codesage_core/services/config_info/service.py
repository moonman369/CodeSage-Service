"""Configuration info service (relocated)."""
from __future__ import annotations
import os
from typing import Any, Dict

EMBED_MODEL = "codesage-embed-mini-1"
MCP_CONNECTIONS = ["github", "vector-db", "llm-gateway"]  # placeholder list

def execute_config_info() -> Dict[str, Any]:
    return {
        "server": "CodeSage MCP",
        "version": os.getenv("CODESAGE_VERSION", "1.0"),
        "repo_path": os.getenv("CODESAGE_REPO_PATH", "./"),
        "embedding_model": EMBED_MODEL,
        "connected_services": MCP_CONNECTIONS,
        "env": os.getenv("CODESAGE_ENV", "dev"),
        "note": "Stub config info - augment with dynamic diagnostics later.",
    }

__all__ = ["execute_config_info"]
