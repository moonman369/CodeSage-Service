import os
import json
import argparse
from typing import List, Dict, Optional
from dotenv import load_dotenv
from fastmcp import FastMCP

from core.digestor.repomix_digestor import RepomixDigestor
from core.chunker.basic_chunker import BasicChunker
from core.summarizer.chunk_processor import LLMChunkProcessor
from core.prompt.basic_prompt_builder import BasicPromptBuilder
from core.llm.openrouter_ai_client import OpenRouterAIClient
from core.embedder.local_embedder import LocalEmbedder
from core.vector_store.qdrant_vector_store import QdrantVectorStore
from core.rag.rag_engine import RAGEngine

load_dotenv()

app = FastMCP(
    name="codesage",
    version="0.1.0",
    instructions="CodeSage MCP Server: codebase loading, querying, suggestions, and related tools.",
)

# Lazy singletons (created on demand)
_digestor: Optional[RepomixDigestor] = None
_chunker: Optional[BasicChunker] = None
_chunk_processor: Optional[LLMChunkProcessor] = None
_embedder: Optional[LocalEmbedder] = None
_vector_store: Optional[QdrantVectorStore] = None
_rag_engine: Optional[RAGEngine] = None

PROJECT_STATE_DIR = os.path.join("outputs", "projects")
os.makedirs(PROJECT_STATE_DIR, exist_ok=True)


def get_digestor():
    global _digestor
    if _digestor is None:
        _digestor = RepomixDigestor()
    return _digestor


def get_chunker():
    global _chunker
    if _chunker is None:
        _chunker = BasicChunker()
    return _chunker


def get_chunk_processor():
    global _chunk_processor
    if _chunk_processor is None:
        _chunk_processor = LLMChunkProcessor(BasicPromptBuilder(), OpenRouterAIClient())
    return _chunk_processor


def get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = LocalEmbedder()
    return _embedder


def get_vector_store():
    global _vector_store
    if _vector_store is None:
        # LocalEmbedder already instantiates QdrantVectorStore but we also expose directly
        _vector_store = get_embedder().vector_store
    return _vector_store


def get_rag_engine():
    global _rag_engine
    if _rag_engine is None:
        _rag_engine = RAGEngine(
            retriever=get_vector_store(),
            prompt_builder=BasicPromptBuilder(),
            embedder=get_embedder(),
            llm_client=OpenRouterAIClient(),
        )
    return _rag_engine


def _project_chunks_path(project_name: str) -> str:
    return os.path.join(PROJECT_STATE_DIR, f"{project_name}_chunks.json")


def _project_digest_path(project_name: str) -> str:
    return os.path.join(PROJECT_STATE_DIR, f"{project_name}_digest.md")


def _save_chunks(project_name: str, chunks: List[Dict]):
    with open(_project_chunks_path(project_name), "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)


def _load_chunks(project_name: str) -> List[Dict]:
    path = _project_chunks_path(project_name)
    if not os.path.isfile(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_digest(project_name: str, content: str):
    with open(_project_digest_path(project_name), "w", encoding="utf-8") as f:
        f.write(content)


def _extract_project_name(repo_url: str) -> str:
    name = repo_url.rstrip("/").split("/")[-1]
    if name.endswith(".git"):
        name = name[:-4]
    return name


@app.tool(
    description="Load a repository (remote URL) for the first time: digest, chunk, summarize, embed, and index into vector store."
)
def load_repository(repo_url: str) -> Dict:
    project_name = _extract_project_name(repo_url)
    digestor = get_digestor()
    chunker = get_chunker()
    chunk_processor = get_chunk_processor()
    embedder = get_embedder()
    vector_store = get_vector_store()

    digest_result = digestor.digest_repo(repo_url)
    digest_content = digest_result["content"]
    _save_digest(project_name, digest_content)

    # Chunk
    chunks = chunker.chunk(digest_content)

    # Summarize each chunk (could be large; consider streaming/progress in future)
    processed_chunks = []
    for c in chunks:
        processed_chunks.append(chunk_processor.process_chunk(c))

    # Embed
    embedded_chunks = embedder.embed_chunks(processed_chunks)

    # Upsert into vector store
    vector_store.upsert(embedded_chunks)

    # Persist
    _save_chunks(project_name, embedded_chunks)

    return {
        "project_name": project_name,
        "total_chunks": len(embedded_chunks),
        "message": f"Repository {project_name} loaded and indexed.",
    }


@app.tool(
    description="Load a local directory (already cloned repo) and index it (digest, chunk, summarize, embed)."
)
def load_local_directory(directory_path: str) -> Dict:
    if not os.path.isdir(directory_path):
        return {"error": f"Directory not found: {directory_path}"}
    digestor = get_digestor()
    chunker = get_chunker()
    chunk_processor = get_chunk_processor()
    embedder = get_embedder()
    vector_store = get_vector_store()

    digest_result = digestor.digest_directory(directory_path)
    project_name = digest_result["project_name"]
    digest_content = digest_result["content"]
    _save_digest(project_name, digest_content)

    chunks = chunker.chunk(digest_content)
    processed_chunks = [chunk_processor.process_chunk(c) for c in chunks]
    embedded_chunks = embedder.embed_chunks(processed_chunks)
    vector_store.upsert(embedded_chunks)
    _save_chunks(project_name, embedded_chunks)
    return {
        "project_name": project_name,
        "total_chunks": len(embedded_chunks),
        "message": f"Local directory {project_name} loaded and indexed.",
    }


@app.tool(description="Query the loaded codebase using RAG + LLM.")
def query_codebase(project_name: str, query: str) -> Dict:
    rag = get_rag_engine()
    answer = rag.generate_response(query=query, project_name=project_name)
    return {"answer": answer}


@app.tool(
    description="Get suggestions for improving or extending codebase (RAG + LLM + simple web search)."
)
def suggestions(project_name: str, topic: str) -> Dict:
    """Provide improvement suggestions. Performs RAG answer then augments with minimal web hints."""
    # First, RAG answer
    rag = get_rag_engine()
    base_analysis = rag.generate_response(
        query=f"Provide improvement suggestions about: {topic}",
        project_name=project_name,
    )
    # Simple external search (duckduckgo)
    try:
        from duckduckgo_search import DDGS

        snippets = []
        with DDGS() as ddgs:
            for r in ddgs.text(f"software engineering {topic}", max_results=3):
                snippets.append(r.get("body") or r.get("snippet") or "")
        external = "\n".join(snippets)
    except Exception as e:
        external = f"(web search failed: {e})"

    prompt = (
        "You are merging internal codebase context with general best practices.\n"
        f"Internal Analysis:\n{base_analysis}\n\nExternal Hints:\n{external}\n\n"
        "Provide a concise, prioritized list of actionable suggestions (bulleted)."
    )
    llm = OpenRouterAIClient()
    merged = llm.generate_response(prompt)
    return {"suggestions": merged}


@app.tool(description="List all loaded projects.")
def list_projects() -> Dict:
    projects = []
    for fname in os.listdir(PROJECT_STATE_DIR):
        if fname.endswith("_chunks.json"):
            projects.append(fname.replace("_chunks.json", ""))
    return {"projects": projects}


@app.tool(
    description="Re-embed and re-index chunks for a project (e.g., after model upgrade)."
)
def reindex_project(project_name: str) -> Dict:
    chunks = _load_chunks(project_name)
    if not chunks:
        return {"error": "No chunks found for project."}
    embedder = get_embedder()
    vector_store = get_vector_store()
    # Re-embed summaries only
    for c in chunks:
        summary = c.get("llm_summary") or c.get("raw_code") or ""
        if summary:
            c["embedding"] = embedder.embed_text(summary)
    vector_store.upsert(chunks)
    _save_chunks(project_name, chunks)
    return {"message": f"Project {project_name} reindexed", "total_chunks": len(chunks)}


@app.tool(description="List chunk metadata for a given file inside a project.")
def get_file_chunks(project_name: str, file_path: str) -> Dict:
    chunks = _load_chunks(project_name)
    if not chunks:
        return {"error": "No chunks found for project."}
    file_chunks = [
        {
            "chunk_index": c.get("metadata", {}).get("chunk_index"),
            "start_line": c.get("metadata", {}).get("start_line"),
            "end_line": c.get("metadata", {}).get("end_line"),
            "summary_preview": (c.get("llm_summary") or "")[:160],
        }
        for c in chunks
        if c.get("metadata", {}).get("file_path") == file_path
    ]
    return {"file_path": file_path, "chunks": file_chunks}


def main():  # Entry point for script with transport selection
    parser = argparse.ArgumentParser(description="Run CodeSage FastMCP Server")
    parser.add_argument(
        "--transport",
        default=os.getenv("CODESAGE_MCP_TRANSPORT", "stdio"),
        help="Transport: stdio | http | sse | streamable-http (default: stdio)",
    )
    parser.add_argument(
        "--host",
        default=os.getenv("CODESAGE_MCP_HOST", "127.0.0.1"),
        help="Host for http/streamable-http/sse transports",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("CODESAGE_MCP_PORT", "8000")),
        help="Port for http/streamable-http/sse transports",
    )
    args = parser.parse_args()

    transport = args.transport.lower().strip()
    allowed = {"stdio", "http", "sse", "streamable-http"}
    if transport not in allowed:
        raise SystemExit(
            f"Invalid transport '{args.transport}'. Allowed: {', '.join(sorted(allowed))}"
        )

    if transport == "stdio":
        app.run(transport="stdio")
    else:
        # For http, sse, streamable-http pass host/port
        app.run(transport=transport, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
