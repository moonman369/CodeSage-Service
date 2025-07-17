from typing import List, Dict, Any
import os

def load_chunks_from_file(file_path: str) -> List[Dict[str, Any]]:
        """
        Loads chunks from a JSON file.
        Each chunk should be a dictionary with 'id', 'embedding', and optional metadata.
        """
        import json
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)

        print(f"Loaded {len(chunks)} chunks from {file_path}")
        return chunks
        
def test_upsert_vector_store():
    """
    Test the QdrantVectorStore by upserting and querying chunks.
    """
    from core.vector_store.qdrant_vector_store import QdrantVectorStore

    # Load chunks from a sample file
    input_path = "outputs/embeddings/embedded_chunks.json"
    chunks = load_chunks_from_file(input_path)

    # Initialize Qdrant vector store
    vector_store = QdrantVectorStore()

    # Upsert chunks into the vector store
    vector_store.upsert(chunks)
    print("✅ Chunks upserted successfully!")

def test_query_vector_store(text: str = "This is a test query."):
    """
    Test querying the Qdrant vector store.
    """
    from core.vector_store.qdrant_vector_store import QdrantVectorStore

    # Initialize Qdrant vector store
    vector_store = QdrantVectorStore()

    from test.embedder.test_embed_text import test_embed_text
    # Example query vector (replace with actual embedding)
    query_vector = test_embed_text(text)
    results = vector_store.query(query_vector, top_k=5)

    print(f"✅ Query results: {results}")
    import os
    import json
    output_path = "outputs/vector_store/query_results.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"✅ Embedded chunks saved to: {output_path}")


if __name__ == "__main__":
    # test_upsert_vector_store()
    test_query_vector_store("Where is XML transformation handled?")