from core.embedder.base_embedder import BaseEmbedder
from core.embedder.openai_embedder import OpenAIEmbedder

def test_openai_embedder():
    """
    Test the OpenAIEmbedder with a sample chunk.
    This is a basic test to ensure the embedder can process a chunk and return an embedding.
    """
    embedder = OpenAIEmbedder(embedding_model="text-embedding-3-small")

    embedded_chunks = embedder.embed_chunks_from_file("outputs/summaries/all_chunks_output.json")

    print(f"Total Embedded Chunks: {len(embedded_chunks)}")
    print(f"Sample Embedding: {embedded_chunks[0]['embedding'][:5]}...")  # Print first 5 dimensions of the embedding


if __name__ == "__main__":
    test_openai_embedder()