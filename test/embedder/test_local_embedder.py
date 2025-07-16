import json
from core.embedder.local_embedder import LocalEmbedder

def test_local_embedder():
    """
    Test the LocalEmbedder with a sample chunk file.
    Embeds chunks and saves the output with embeddings to a new JSON file.
    """
    input_path = "outputs/summaries/all_chunks_output.json"
    output_path = "outputs/embeddings/embedded_chunks.json"

    embedder = LocalEmbedder(embedding_model="sentence-transformers/all-MiniLM-L6-v2")

    embedded_chunks = embedder.embed_chunks_from_file(input_path)

    print(f"✅ Total Embedded Chunks: {len(embedded_chunks)}")
    print(f"📊 Sample Embedding (first 5 dims): {embedded_chunks[0]['embedding'][:5]}...")

    # Create output directory if needed
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(embedded_chunks, f, indent=2)

    print(f"✅ Embedded chunks saved to: {output_path}")


if __name__ == "__main__":
    test_local_embedder()
