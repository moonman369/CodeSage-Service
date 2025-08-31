"""Tests for the code_understanding tool.

These tests exercise the public async tool function exposed by the server.
They intentionally do not require a live Qdrant / LLM backend – absence of
environment configuration should trigger graceful fallbacks that still return
the expected schema shape.
"""
from __future__ import annotations

import importlib
import pytest


@pytest.mark.asyncio
async def test_code_understanding_basic():
    server = importlib.import_module("codesage_core.server")
    resp = await server.code_understanding(repo="demo", query="What does the repository do?", top_k=3)
    assert isinstance(resp, dict)
    assert "answer" in resp and isinstance(resp["answer"], str)
    assert "relevant_chunks" in resp and isinstance(resp["relevant_chunks"], list)


@pytest.mark.asyncio
async def test_code_understanding_with_context_files():
    server = importlib.import_module("codesage_core.server")
    resp = await server.code_understanding(
        repo="demo", query="Explain utils", context_files=["src/utils/helpers.py"], top_k=2
    )
    assert isinstance(resp, dict)
    assert "answer" in resp
    assert "relevant_chunks" in resp
    # Context file filtering should not raise even if no matches
    assert isinstance(resp["relevant_chunks"], list)