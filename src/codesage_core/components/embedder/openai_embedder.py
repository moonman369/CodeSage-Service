import json
import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

from langchain.embeddings import OpenAIEmbeddings


class OpenAIEmbedder:
    def __init__(self, embedding_model: str = "text-embedding-3-small"):
        self.openai_api_key = os.getenv("SUMMARIZER_OPENROUTER_API_KEY");
        self.embedder = OpenAIEmbeddings(
            api_key=self.openai_api_key,
            model=embedding_model,
        )

    def embed_chunks(self, chunks: List[Dict]) -> List[Dict]:
        """
        Takes a list of chunks and returns list of dicts with embeddings added.
        Skips chunks with empty or missing llm_summary.
        """
        embedded_chunks = []

        for chunk in chunks:
            summary = chunk.get("llm_summary", "").strip()
            if not summary:
                continue

            embedding = self.embedder.embed_query(summary)
            embedded_chunks.append({
                "embedding": embedding,
                "metadata": chunk.get("metadata", {}),
                "llm_summary": summary
            })

        return embedded_chunks

    def embed_chunks_from_file(self, file_path: str) -> List[Dict]:
        """
        Loads a JSON file of chunks and returns embedded versions.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)

        return self.embed_chunks(chunks)
