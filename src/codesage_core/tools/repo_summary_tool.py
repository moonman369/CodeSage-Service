"""MCP tool layer for repository-level summarisation.

Defines request schemas & lightweight endpoint functions delegating to the
RepoSummaryService. Kept separate from server wiring for testability.
"""
from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Dict, Any

from codesage_core.services.repo_summary.repo_summary_service import RepoSummaryService

__all__ = [
    "GetRepoSummaryRequest",
    "GetRepoStructureRequest",
    "RepoSummaryTool",
    "get_repo_summary_endpoint",
    "get_repo_structure_endpoint",
]


class GetRepoSummaryRequest(BaseModel):
    project_name: str = Field(..., description="Project / repository name (matches project_name in vector store)")
    prompt: str | None = Field(None, description="Optional semantic instruction (e.g. 'Explain repo briefly').")


class GetRepoStructureRequest(BaseModel):
    project_name: str = Field(..., description="Project / repository name")


_service = RepoSummaryService()


def get_repo_summary_endpoint(req: GetRepoSummaryRequest) -> Dict[str, Any]:
    return _service.get_repo_summary(req.project_name, prompt=req.prompt)


def get_repo_structure_endpoint(req: GetRepoStructureRequest) -> Dict[str, Any]:
    return _service.get_repo_structure(req.project_name)


class RepoSummaryTool:
    """Thin wrapper exposing repo-level summary endpoints for server registration.

    Methods intentionally use camelCase names (getRepoSummary / getRepoStructure)
    to mirror the initial architectural spec.
    """

    def __init__(self, service: RepoSummaryService | None = None) -> None:
        self._service = service or RepoSummaryService()

    def getRepoSummary(self, project_name: str, prompt: str | None = None) -> Dict[str, Any]:  # noqa: N802 (spec requires casing)
        return self._service.get_repo_summary(project_name, prompt=prompt)

    def getRepoStructure(self, project_name: str) -> Dict[str, Any]:  # noqa: N802
        return self._service.get_repo_structure(project_name)

