import os
import re
from core.chunker.basic_chunker import BasicChunker

def read_digest_from_root(filename="repomix-output.md") -> str:
    """
    Reads the markdown digest from the project root.
    Assumes this test script is run from anywhere inside the CodeSage repo.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Navigate up to project root (two levels up from test/chunker)
    root_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
    digest_path = os.path.join(root_dir, filename)
    
    print(f"Looking for digest at: {digest_path}")
    if not os.path.exists(digest_path):
        raise FileNotFoundError(f"Digest file not found at: {digest_path}")

    with open(digest_path, "r", encoding="utf-8") as f:
        content = f.read()
        print(f"Successfully loaded digest ({len(content)} characters)")
        return content

def test_chunking_from_digest():
    markdown_digest = read_digest_from_root()
    print(f"📄 Digest Length: {len(markdown_digest)} characters")
    # matches = re.findall(r"^## (.+)$", markdown_digest, re.MULTILINE)
    # print(f"Matched Files: {matches}")
    
    # Create chunker with appropriate settings for the test
    chunker = BasicChunker(chunk_size=80, overlap=15)
    chunks = chunker.chunk(markdown_digest)

    print(f"✅ Total Chunks Generated: {len(chunks)}")
    
    # Save chunks to output directory
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "outputs", "chunks")
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "chunks_output.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, chunk in enumerate(chunks):
            f.write(f"CHUNK {i + 1}\n")
            f.write(f"File: {chunk['metadata']['file_path']}\n")
            f.write(f"Lines: {chunk['metadata']['start_line']}-{chunk['metadata']['end_line']}\n")
            f.write(f"Language: {chunk['metadata']['language']}\n")
            f.write(f"Raw Code: {chunk['raw_code']}\n")
            f.write("-" * 80 + "\n")
            f.write(chunk['chunk_summary'] + "\n")
            f.write("\n\n" + "=" * 80 + "\n\n")
    
    print(f"✅ Chunks saved to: {output_file}")

    # Display sample chunks for quick verification
    # sample_count = min(3, len(chunks))
    # for i, chunk in enumerate(chunks[:sample_count]):
    #     print(f"\n--- Sample Chunk {i + 1}/{sample_count} ---")
    #     print(f"File: {chunk['metadata']['file_path']}")
    #     print(f"Lines: {chunk['metadata']['start_line']}-{chunk['metadata']['end_line']}")
    #     print(f"Language: {chunk['metadata']['language']}")
        
    #     # Truncate chunk text for display
    #     chunk_text = chunk['chunk_text']
    #     max_display = 300
    #     if len(chunk_text) > max_display:
    #         print(chunk_text[:max_display] + "...")
    #     else:
    #         print(chunk_text)

if __name__ == "__main__":
    test_chunking_from_digest()
