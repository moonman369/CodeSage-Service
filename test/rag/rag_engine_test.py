from core.embedder.local_embedder import LocalEmbedder
from core.embedder.local_embedder import LocalEmbedder
from core.rag.rag_engine import RAGEngine
from core.vector_store.qdrant_vector_store import QdrantVectorStore
from core.llm.openrouter_ai_client import OpenRouterAIClient
from core.prompt.basic_prompt_builder import BasicPromptBuilder


def test_rag_engine(prompt: str = "") -> None:
    # Initialize components
    retriever = QdrantVectorStore()
    prompt_builder = BasicPromptBuilder()
    embedder = LocalEmbedder()
    llm_client = OpenRouterAIClient()

    # Create RAG engine
    rag_engine = RAGEngine(retriever, prompt_builder, embedder, llm_client)

    # Test RAG engine response
    response = rag_engine.generate_response(prompt, project_name="Portfolio")


if __name__ == "__main__":
    test_rag_engine(
        "Which section of the website contains the logic to fetch leetcode and github repositories and display them on the portfolio? Also follow up question, is there any specific cors related code present?"
    )
