"""Schemas for the `code_understanding` MCP tool.

Defines the validated request & response contracts so the server, service and
tests share a single source of truth. Only lightweight / serialisable fields
are exposed – heavy objects (embeddings, raw chunk dicts) stay internal.
"""
from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field

__all__ = [
    "CodeUnderstandingRequest",
    "CodeUnderstandingResponse",
]


class CodeUnderstandingRequest(BaseModel):
    """Input for the code_understanding tool.

    repo: logical repository identifier (e.g. name or path or URL fragment).
    query: natural language question.
    context_files: optional whitelist of file paths to constrain retrieval.
    top_k: number of chunks to retrieve (default 5, capped internally).
    """

    repo: str = Field(..., description="Repository name / path / id scope for search")
    query: str = Field(..., description="Natural language user query about the code")
    context_files: Optional[List[str]] = Field(
        default=None,
        description="Optional list of file paths to restrict retrieval to specific files",
    )
    top_k: int = Field(5, ge=1, le=50, description="Number of code chunks to retrieve (1-50)")


class CodeUnderstandingResponse(BaseModel):
    """Structured output from the code_understanding tool.

    answer: final natural language answer from the LLM (or fallback stub).
    relevant_chunks: list of textual snippet/summary strings supplied as context.
    """

    answer: str = Field(..., description="Answer synthesized from retrieved code context")
    relevant_chunks: List[str] = Field(
        default_factory=list, description="Ordered list of the most relevant code summaries/snippets"
    )
