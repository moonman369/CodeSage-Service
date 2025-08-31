"""Utilities for building repository-wide summaries from file-level data.

Designed to be lightweight and pure so it's easy to unit test.
"""
from __future__ import annotations

from typing import Iterable, List, Dict, Any, Tuple
from collections import Counter
import math

__all__ = [
    "aggregate_language_distribution",
    "aggregate_llm_summaries",
    "heuristic_fallback_summary",
    "compose_repo_summary",
]


def aggregate_language_distribution(chunks: Iterable[Dict[str, Any]]) -> List[Tuple[str, int]]:
    counts: Counter[str] = Counter()
    for c in chunks:
        lang = (c.get("metadata", {}).get("language") or c.get("metadata", {}).get("lang") or "unknown").lower()
        counts[lang] += 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


def aggregate_llm_summaries(chunks: Iterable[Dict[str, Any]], max_items: int = 30) -> List[str]:
    summaries: List[str] = []
    for c in chunks:
        summary = (c.get("llm_summary") or c.get("metadata", {}).get("llm_summary") or "").strip()
        if summary:
            summaries.append(summary)
            if len(summaries) >= max_items:
                break
    return summaries


def heuristic_fallback_summary(chunks: Iterable[Dict[str, Any]], max_files: int = 20) -> str:
    files: List[str] = []
    for c in chunks:
        fp = c.get("metadata", {}).get("file_path") or c.get("metadata", {}).get("path")
        if fp and fp not in files:
            files.append(fp)
        if len(files) >= max_files:
            break
    if not files:
        return "Repository appears empty or not indexed."
    root_dirs = Counter(f.split("/")[0] for f in files if "/" in f)
    dir_part = ", ".join(f"{d} ({n})" for d, n in root_dirs.most_common(5)) or "single-level layout"
    return f"Repo contains at least {len(files)} tracked files across top-level areas: {dir_part}."


def compose_repo_summary(project: str, summaries: List[str], lang_dist: List[Tuple[str, int]], total_files: int) -> str:
    if summaries:
        joined = " ".join(summaries[:10])  # keep concise
    else:
        joined = ""
    total_snippets = len(summaries)
    lang_part = ", ".join(f"{lang}:{count}" for lang, count in lang_dist[:5]) or "unknown"
    density = (total_snippets / total_files) if total_files else 0.0
    coverage_pct = min(100.0, round(density * 100, 1))
    core = [
        f"Project '{project}' overview:",
        f"Languages: {lang_part} (total files={total_files}).",
        f"Summaries coverage: {coverage_pct}% of files have LLM summaries (approx).",
    ]
    if joined:
        core.append(f"Representative summaries: {joined}")
    return " \n".join(core)
