from typing import List, Dict
from abc import ABC, abstractmethod
from sentence_transformers import SentenceTransformer
from codesage_core.components.embedder.base_embedder import BaseEmbedder
from codesage_core.components.vector_store.qdrant_vector_store import QdrantVectorStore
import os


class LocalEmbedder(BaseEmbedder):
    def __init__(self, embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        print(f"⏳ Loading local embedding model: {embedding_model}")
        self.model = SentenceTransformer(embedding_model)
        print("✅ Model loaded successfully!")

        self.vector_store = QdrantVectorStore(
            vector_size=self.model.get_sentence_embedding_dimension()
        )

    def embed_chunks(self, chunks: List[Dict]) -> List[Dict]:
        for chunk in chunks:
            text = chunk.get("llm_summary") or chunk.get("raw_code") or ""
            if text.strip():
                embedding = self.model.encode(text, convert_to_numpy=True).tolist()
                chunk["embedding"] = embedding
            else:
                chunk["embedding"] = []
        

        return chunks

    def embed_chunks_from_file(self, json_file_path: str) -> List[Dict]:
        import json
        if not os.path.isfile(json_file_path):
            raise FileNotFoundError(f"❌ File not found: {json_file_path}")

        with open(json_file_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)

        print(f"📄 Loaded {len(chunks)} chunks from {json_file_path}")
        return self.embed_chunks(chunks)

    def embed_text(self, text: str) -> List[float]:
        return self.model.encode(text, convert_to_numpy=True).tolist()
