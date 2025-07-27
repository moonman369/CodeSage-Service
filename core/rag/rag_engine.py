# rag_engine/engine.py

from .base_rag_engine import BaseRAGEngine
from core.vector_store.qdrant_vector_store import QdrantVectorStore
from core.llm.openrouter_ai_client import OpenRouterAIClient
from core.prompt.basic_prompt_builder import BasicPromptBuilder

class RAGEngine(BaseRAGEngine):
    def __init__(self, retriever: QdrantVectorStore, prompt_builder: BasicPromptBuilder, llm_client: OpenRouterAIClient):
        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.llm_client = llm_client

    def generate_response(self, query: str) -> str:
        # Step 1: Retrieve top-k relevant chunks
        relevant_chunks = self.retriever.get_relevant_chunks(query)

        # Step 2: Compose final prompt
        prompt = self.prompt_builder.compose_prompt(query=query, context_chunks=relevant_chunks)

        # Step 3: Send to LLM and get output
        response = self.llm_client.get_completion(prompt)

        return response
