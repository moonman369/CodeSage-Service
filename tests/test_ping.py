"""Tests for the ping tool."""
from __future__ import annotations

import importlib

from pydantic import BaseModel


def test_ping_tool() -> None:
    server = importlib.import_module("codesage_core.server")

    class Dummy(BaseModel):
        message: str

    # Directly call the ping coroutine
    resp = server.asyncio.run(server.ping(server.PingRequest(message="hello")))  # type: ignore[attr-defined]
    assert resp.echoed == "hello"
    assert resp.length == 5
