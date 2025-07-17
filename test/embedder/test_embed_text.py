from core.embedder.local_embedder import LocalEmbedder

def test_embed_text(text: str = "This is a test text."):
    embedder = LocalEmbedder()
    embeddings = embedder.embed_text(text)
    print(f"✅ Embedding for text '{text[:30]}...': {embeddings[:5]}")  # Print first 5 dimensions of the embedding
    return embeddings

if __name__ == "__main__":
    test_embed_text("This is a test text.")