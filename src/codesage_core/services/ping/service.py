"""Ping service module (relocated).

Provides health check information for the CodeSage MCP server.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Any

_START_TIME = datetime.now(timezone.utc)


def execute_ping() -> Dict[str, Any]:
    now = datetime.now(timezone.utc)
    uptime_seconds = (now - _START_TIME).total_seconds()
    return {
        "status": "ok",
        "message": "pong",
        "uptime_seconds": round(uptime_seconds, 3),
        "started_at": _START_TIME.isoformat(),
        "timestamp": now.isoformat(),
    }

__all__ = ["execute_ping"]
