"""Concrete implementation of the code understanding workflow.

Pipeline:
 1. Embed user query (cached within process) using LocalEmbedder.
 2. Retrieve top-K relevant chunks from QdrantVectorStore (optionally filtered).
 3. Build concise RAG prompt with BasicPromptBuilder.
 4. Generate final answer via OpenRouterAIClient (LLM). If LLM unavailable, use
    a deterministic fallback answer so the tool always returns a response.

The service only returns lightweight serialisable fields (answer + context
strings) – raw chunk metadata is not exposed directly to keep the schema lean.
"""
from __future__ import annotations

from typing import Dict, List, Optional
import hashlib
import logging

from codesage_core.components.embedder.local_embedder import LocalEmbedder
from codesage_core.components.vector_store.qdrant_vector_store import QdrantVectorStore
from codesage_core.components.prompt.basic_prompt_builder import BasicPromptBuilder
from codesage_core.components.llm.openrouter_ai_client import OpenRouterAIClient

logger = logging.getLogger(__name__)


class CodeUnderstandingService:
    """High-level orchestrator for code understanding queries."""

    def __init__(
        self,
        embedder: Optional[LocalEmbedder] = None,
        vector_store: Optional[QdrantVectorStore] = None,
        prompt_builder: Optional[BasicPromptBuilder] = None,
        llm_client: Optional[OpenRouterAIClient] = None,
        max_top_k: int = 15,
    ) -> None:
        # Attempt to initialise full stack; fall back to lightweight stubs if unavailable
        self.embedder: LocalEmbedder | _StubEmbedder  # type: ignore[name-defined]
        self.vector_store: QdrantVectorStore | _StubVectorStore  # type: ignore[name-defined]
        if embedder is not None:
            self.embedder = embedder
            self.vector_store = vector_store or embedder.vector_store  # type: ignore[attr-defined]
        else:
            try:  # pragma: no cover - depends on external env
                real_embedder = LocalEmbedder()
                self.embedder = real_embedder
                self.vector_store = vector_store or real_embedder.vector_store
            except Exception as exc:  # Fallback stub path
                logger.warning("code_understanding_embedder_init_failed: %s", exc)
                self.embedder = _StubEmbedder()
                self.vector_store = _StubVectorStore()

        self.prompt_builder = prompt_builder or BasicPromptBuilder()
        self._llm_client = llm_client  # lazy
        self.max_top_k = max_top_k
        self._query_cache: Dict[str, List[float]] = {}

    # -------------------- internal helpers -------------------- #
    def _cache_key(self, repo: str, query: str) -> str:
        return hashlib.sha1(f"{repo}\n{query}".encode("utf-8")).hexdigest()

    def _embed_query(self, repo: str, query: str) -> List[float]:
        key = self._cache_key(repo, query)
        if key in self._query_cache:
            return self._query_cache[key]
        emb = self.embedder.embed_text(query)
        self._query_cache[key] = emb
        return emb

    def _ensure_llm(self) -> Optional[OpenRouterAIClient]:
        if self._llm_client is not None:
            return self._llm_client
        try:
            self._llm_client = OpenRouterAIClient()
        except Exception as exc:  # pragma: no cover - depends on env
            logger.warning("code_understanding_llm_unavailable: %s", exc)
            self._llm_client = None
        return self._llm_client

    # -------------------- public API -------------------- #
    def handle(
        self,
        repo: str,
        query: str,
        top_k: int = 5,
        context_files: Optional[List[str]] = None,
    ) -> Dict[str, List[str] | str]:
        """Execute full retrieval + generation flow.

        Returns dict matching CodeUnderstandingResponse fields.
        """
        top_k_eff = max(1, min(self.max_top_k, top_k))
        query_vec = self._embed_query(repo, query)

        # If vector store supports project existence check, short-circuit if missing
        if hasattr(self.vector_store, "has_project"):
            bypass = False
            try:
                bypass = bool(int(os.getenv("CODESAGE_BYPASS_PROJECT_CHECK", "0")))  # type: ignore[name-defined]
            except Exception:
                bypass = False
            try:
                exists = self.vector_store.has_project(repo)  # type: ignore[attr-defined]
                if not exists and not bypass:
                    logger.info("code_understanding_missing_project: %s", repo)
                    return {
                        "answer": "",
                        "relevant_chunks": [],
                        "status": "not_found",  # type: ignore[dict-item]
                        "message": f"No codebase data found for project {repo} in the Vector DB.",  # type: ignore[dict-item]
                    }
                if not exists and bypass:
                    logger.info("code_understanding_project_check_bypassed: %s", repo)
            except Exception as exc:
                logger.warning("code_understanding_project_check_failed: %s", exc)
                # Continue to attempt query

        # Retrieve raw hits
        try:
            hits = self.vector_store.query(query_vector=query_vec, project_name=repo, top_k=top_k_eff)
        except Exception as exc:  # pragma: no cover - network issues
            logger.error("code_understanding_vector_query_failed: %s", exc)
            hits = []

        # Optional file filter (client-side because Qdrant payload flattening)
        if context_files:
            lowered = {f.lower() for f in context_files}
            filtered = []
            for h in hits:
                file_path = (
                    h.get("metadata", {})
                    .get("metadata", {})
                    .get("file_path")
                )
                if file_path and file_path.lower() in lowered:
                    filtered.append(h)
            if filtered:
                hits = filtered

        # Build context strings (prefer llm_summary, fallback to raw_code snippet)
        context_strings: List[str] = []
        for h in hits:
            payload = h.get("metadata", {})
            meta = payload.get("metadata", {})
            file_path = meta.get("file_path") or meta.get("path") or "unknown"
            summary = payload.get("llm_summary") or meta.get("llm_summary") or ""
            raw_code = payload.get("raw_code") or meta.get("raw_code") or ""
            if summary:
                context_strings.append(f"[{file_path}] {summary.strip()}")
            elif raw_code:
                snippet = raw_code[:300].replace("\n", " ")
                context_strings.append(f"[{file_path}] {snippet}...")
        # Truncate to requested top_k
        context_strings = context_strings[:top_k_eff]

        # Generate answer
        llm = self._ensure_llm()
        if llm and context_strings:
            prompt = self.prompt_builder.build_prompt_rag(query, hits[:top_k_eff])
            answer = llm.generate_response(prompt) or ""
        else:
            # Fallback deterministic answer
            answer = (
                "(fallback) Unable to access LLM or context. "
                "Retrieved 0 chunks." if not context_strings else
                "(fallback) LLM unavailable; returning concatenated context summaries. "
                + " ".join(context_strings)
            )

        return {"answer": answer.strip(), "relevant_chunks": context_strings}


# -------------------- lightweight stubs (no external deps) -------------------- #


class _StubVectorStore:
    def query(self, query_vector: List[float], project_name: str = "", top_k: int = 5):  # noqa: D401
        return []


class _StubEmbedder:
    def __init__(self) -> None:  # noqa: D401
        self.vector_store = _StubVectorStore()

    def embed_text(self, text: str) -> List[float]:  # deterministic tiny vector
        h = hashlib.sha1(text.encode("utf-8")).digest()
        return [round(b / 255, 6) for b in h[:8]]


__all__ = ["CodeUnderstandingService"]
