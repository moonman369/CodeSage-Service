"""Service layer for the repo_summary MCP tool.

Provides high-level repository summarisation distinct from fine-grained RAG.
"""
from __future__ import annotations

from typing import Any, Dict, List
import logging

from codesage_core.components.vector_store.qdrant_vector_store import QdrantVectorStore
from codesage_core.components.summary.summary_builder import (
    aggregate_language_distribution,
    aggregate_llm_summaries,
    heuristic_fallback_summary,
    compose_repo_summary,
)

logger = logging.getLogger(__name__)

__all__ = ["RepoSummaryService"]


class RepoSummaryService:
    def __init__(self, vector_store: QdrantVectorStore | None = None) -> None:
        # Attempt reuse of existing vector store init; fallback stub if missing env.
        if vector_store is not None:
            self.vector_store = vector_store
        else:
            try:  # pragma: no cover - env dependent
                self.vector_store = QdrantVectorStore()
            except Exception as exc:
                logger.warning("repo_summary_vector_store_unavailable: %s", exc)
                self.vector_store = _StubVectorStore()

    def _fetch_all_points(self, project: str, limit: int = 5000) -> List[Dict[str, Any]]:
        # Qdrant search API needs a vector; for listing we attempt a dummy query then may extend.
        # For simplicity, reuse vector search with a neutral zero vector matching by filter only.
        if not hasattr(self.vector_store, "has_project"):
            return []
        if not self.vector_store.has_project(project):  # type: ignore[attr-defined]
            return []
        # We don't have direct 'scroll' implemented; run a broad query multiple times with random vec.
        # Simplify: single query with zero vector may still return top_k only; treat as sample.
        try:
            dim = getattr(self.vector_store, "vector_size", 384)
            zero_vec = [0.0] * dim
            sample = self.vector_store.query(query_vector=zero_vec, project_name=project, top_k=min(256, limit))
            # Extract payload directly
            return [hit.get("metadata", {}) for hit in sample]
        except Exception as exc:  # pragma: no cover
            logger.error("repo_summary_fetch_points_failed: %s", exc)
            return []

    def get_repo_summary(self, project_name: str, prompt: str | None = None) -> Dict[str, Any]:
        # Try vector DB first
        points = self._fetch_all_points(project_name)
        if not points:
            # Try to scan/embed using code_understanding, then retry
            try:  # Attempt lightweight scan using stub code_understanding (if present)
                from codesage_core.services.code_understanding_service import execute_code_understanding  # type: ignore
                scan_result = execute_code_understanding(prompt or "Summarize repository", project_name)
                chunks = scan_result.get("relevant_chunks", [])  # list of dicts (stub shape)
                if chunks:
                    dim = getattr(self.vector_store, "vector_size", 384)
                    for idx, c in enumerate(chunks):
                        # Normalise to vector_store.upsert schema
                        # Qdrant expects UUID or int IDs; generate UUID if provided id not valid
                        import uuid
                        c_id = c.get("id") or c.get("path") or f"scan-{idx}"
                        # If not UUID format, replace.
                        try:
                            uuid.UUID(str(c_id))
                        except Exception:
                            c_id = str(uuid.uuid4())
                        c["id"] = c_id
                        c.setdefault("embedding", [0.0] * dim)  # dummy embedding so Qdrant accepts
                        c["project_name"] = project_name
                        c["metadata"] = {"file_path": c.get("path", ""), "language": "unknown"}
                        c.setdefault("llm_summary", c.get("content", ""))
                    if hasattr(self.vector_store, "upsert") and hasattr(self.vector_store, "query"):
                        try:
                            self.vector_store.upsert(chunks)  # type: ignore[attr-defined]
                        except Exception as exc:  # pragma: no cover
                            logger.warning("repo_summary_stub_upsert_failed: %s", exc)
                    points = self._fetch_all_points(project_name)
            except Exception as exc:
                logger.error("repo_summary_scan_embed_failed: %s", exc)
                points = []
        if not points:
            return {"status": "not_found", "message": "Repo data not available in Vector DB or scan/embed failed", "project": project_name}

        lang_dist = aggregate_language_distribution(points)
        summaries = aggregate_llm_summaries(points)
        total_files = len({p.get("metadata", {}).get("file_path") for p in points if p.get("metadata", {}).get("file_path")})
        if not summaries:
            fallback = heuristic_fallback_summary(points)
            overview = compose_repo_summary(project_name, [], lang_dist, total_files) + "\n" + fallback
        else:
            overview = compose_repo_summary(project_name, summaries, lang_dist, total_files)
        base_summary = {
            "status": "ok",
            "project": project_name,
            "summary": overview,
            "languages": [lang for lang, _ in lang_dist],
            "language_breakdown": [{"language": lang, "count": count} for lang, count in lang_dist],
            "files_indexed": total_files,
            "summaries_used": len(summaries),
        }
        if prompt:
            base_summary["prompt"] = prompt
        return base_summary

    def get_repo_structure(self, project_name: str) -> Dict[str, Any]:
        # Try vector DB first
        points = self._fetch_all_points(project_name)
        if not points:
            # Try to scan/embed using code_understanding, then retry
            try:
                from codesage_core.services.code_understanding_service import execute_code_understanding  # type: ignore
                scan_result = execute_code_understanding("Summarize repository structure", project_name)
                chunks = scan_result.get("relevant_chunks", [])
                if chunks:
                    dim = getattr(self.vector_store, "vector_size", 384)
                    for idx, c in enumerate(chunks):
                        import uuid
                        c_id = c.get("id") or c.get("path") or f"scan-{idx}"
                        try:
                            uuid.UUID(str(c_id))
                        except Exception:
                            c_id = str(uuid.uuid4())
                        c["id"] = c_id
                        c.setdefault("embedding", [0.0] * dim)
                        c["project_name"] = project_name
                        c["metadata"] = {"file_path": c.get("path", ""), "language": "unknown"}
                        c.setdefault("llm_summary", c.get("content", ""))
                    if hasattr(self.vector_store, "upsert") and hasattr(self.vector_store, "query"):
                        try:
                            self.vector_store.upsert(chunks)  # type: ignore[attr-defined]
                        except Exception as exc:  # pragma: no cover
                            logger.warning("repo_structure_stub_upsert_failed: %s", exc)
                    points = self._fetch_all_points(project_name)
            except Exception as exc:
                logger.error("repo_structure_scan_embed_failed: %s", exc)
                points = []
        if not points:
            return {"status": "not_found", "message": "Repo data not available in Vector DB or scan/embed failed", "project": project_name}
        files = sorted({p.get("metadata", {}).get("file_path") for p in points if p.get("metadata", {}).get("file_path")})
        tree: Dict[str, Any] = {}
        for fp in files:
            parts = fp.split("/")
            cursor = tree
            for part in parts:
                cursor = cursor.setdefault(part, {})
        return {"status": "ok", "project": project_name, "structure": tree, "file_count": len(files)}


class _StubVectorStore:  # fallback stub
    def has_project(self, project_name: str) -> bool:  # noqa: D401
        return False
