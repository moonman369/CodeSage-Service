"""Ping service module.

Provides health check information for the CodeSage MCP server.
External dependencies (uptime metrics, health probes) can be integrated later.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Any

_START_TIME = datetime.now(timezone.utc)


def execute_ping() -> Dict[str, Any]:
    """Return basic health info and uptime.

    Returns
    -------
    dict
        JSON-serializable health snapshot.
    """
    now = datetime.now(timezone.utc)
    uptime_seconds = (now - _START_TIME).total_seconds()
    return {
        "status": "ok",
        "message": "pong",
        "uptime_seconds": round(uptime_seconds, 3),
        "started_at": _START_TIME.isoformat(),
        "timestamp": now.isoformat(),
    }
