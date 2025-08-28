# rag_engine/engine.py

from .base_rag_engine import BaseRAGEngine
from codesage_core.components.vector_store.qdrant_vector_store import QdrantVectorStore
from codesage_core.components.llm.openrouter_ai_client import OpenRouterAIClient
from codesage_core.components.prompt.basic_prompt_builder import BasicPromptBuilder
from codesage_core.components.embedder.local_embedder import LocalEmbedder
from typing import List


class RAGEngine(BaseRAGEngine):
    def __init__(
        self,
        retriever: QdrantVectorStore,
        prompt_builder: BasicPromptBuilder,
        embedder: LocalEmbedder,
        llm_client: OpenRouterAIClient,
    ):
        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.embedder = embedder
        self.llm_client = llm_client

    def generate_response(self, query: str, project_name: str) -> str:
        import logging

        logger = logging.getLogger(__name__)
        print(
            f"\n[CodeSage] Received query for project: '{project_name}'\nQuery: {query}\n"
        )

        # Step 1: Embed the user query
        query_vector = self.embedder.embed_text(query)
        print(f"[CodeSage] Query vector generated. Length: {len(query_vector)}\n")

        # Step 2: Retrieve top-k relevant chunks
        relevant_chunks = self.retriever.query(
            query_vector=query_vector, project_name=project_name, top_k=5
        )
        print(
            f"[CodeSage] Retrieved {len(relevant_chunks)} relevant chunks for project: '{project_name}'.\n"
        )
        # print(f"Relevant chunks: {relevant_chunks[0]}")

        # Step 3: Compose final prompt
        prompt = self.prompt_builder.build_prompt_rag(
            user_query=query, retrieved_chunks=relevant_chunks
        )
        print(
            f"[CodeSage] Prompt composed for LLM. Length: {len(prompt)} characters.\nPreview:\n{prompt[:500]}...\n"
        )

        # Step 4: Send to LLM and get output
        response = self.llm_client.generate_response(prompt)
        print(
            f"[CodeSage] LLM response generated. Length: {len(response)} characters.\n"
        )

        return response.strip()
