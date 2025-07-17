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
        
def test_qdrant_vector_store():
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


if __name__ == "__main__":
    test_qdrant_vector_store()