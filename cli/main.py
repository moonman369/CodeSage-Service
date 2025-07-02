"""
Command-line interface for running CodeSage modules.
"""
import argparse
import os
import sys
import json
from typing import Dict, List, Any, Optional

# Import core components
from codesage.core.summarizer.summarizer import Summarizer
from codesage.core.chunker.chunker import Chunker
from codesage.core.embedder.embedder import Embedder
from codesage.core.retriever.retriever import Retriever


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="CodeSage - AI-Powered Code Documentation Tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Summarize command
    summarize_parser = subparsers.add_parser("summarize", help="Summarize code")
    summarize_parser.add_argument("path", help="Path to file or directory to summarize")
    summarize_parser.add_argument("--recursive", "-r", action="store_true", help="Process directories recursively")
    summarize_parser.add_argument("--output", "-o", help="Output file path")
    
    # Chunk command
    chunk_parser = subparsers.add_parser("chunk", help="Split code into chunks")
    chunk_parser.add_argument("path", help="Path to file or directory to chunk")
    chunk_parser.add_argument("--size", "-s", type=int, default=1000, help="Chunk size in characters")
    chunk_parser.add_argument("--overlap", type=int, default=200, help="Overlap between chunks")
    chunk_parser.add_argument("--output-dir", "-o", help="Output directory for chunks")
    
    # Embed command
    embed_parser = subparsers.add_parser("embed", help="Create embeddings from chunks")
    embed_parser.add_argument("path", help="Path to chunks file or directory")
    embed_parser.add_argument("--model", "-m", default="default", help="Embedding model to use")
    embed_parser.add_argument("--output", "-o", help="Output file for embeddings")
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Query embeddings")
    query_parser.add_argument("embeddings", help="Path to embeddings file")
    query_parser.add_argument("query", help="Query text")
    query_parser.add_argument("--top-k", "-k", type=int, default=5, help="Number of results to return")
    
    # Pipeline command (run the full pipeline)
    pipeline_parser = subparsers.add_parser("pipeline", help="Run the full pipeline")
    pipeline_parser.add_argument("path", help="Path to file or directory to process")
    pipeline_parser.add_argument("--recursive", "-r", action="store_true", help="Process directories recursively")
    pipeline_parser.add_argument("--output-dir", "-o", default="outputs", help="Output directory")
    pipeline_parser.add_argument("--chunk-size", "-s", type=int, default=1000, help="Chunk size in characters")
    pipeline_parser.add_argument("--model", "-m", default="default", help="Embedding model to use")
    
    return parser.parse_args()


def command_summarize(args):
    """Run the summarize command."""
    summarizer = Summarizer()
    
    if os.path.isfile(args.path):
        result = summarizer.summarize_file(args.path)
        summary = [result]
    else:
        summary = summarizer.summarize_directory(args.path, recursive=args.recursive)
    
    if args.output:
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"Summary written to {args.output}")
    else:
        print(json.dumps(summary, indent=2))


def command_chunk(args):
    """Run the chunk command."""
    chunker = Chunker(chunk_size=args.size, overlap=args.overlap)
    
    if os.path.isfile(args.path):
        chunks = chunker.chunk_file(args.path)
    else:
        chunks = chunker.chunk_directory(args.path, output_dir=args.output_dir)
    
    if not args.output_dir:
        print(json.dumps(chunks, indent=2))
    else:
        print(f"Chunks written to {args.output_dir}")


def command_embed(args):
    """Run the embed command."""
    embedder = Embedder(model_name=args.model)
    
    # Load chunks
    if os.path.isfile(args.path):
        with open(args.path, 'r') as f:
            chunks = json.load(f)
    else:
        print("Error: Embedding requires a chunks file")
        return
    
    # Create embeddings
    embeddings = embedder.embed_chunks(chunks)
    
    # Save or print embeddings
    if args.output:
        embedder.save_embeddings(embeddings, args.output)
        print(f"Embeddings saved to {args.output}")
    else:
        print(json.dumps(embeddings, indent=2))


def command_query(args):
    """Run the query command."""
    retriever = Retriever(embeddings_path=args.embeddings)
    results = retriever.query(args.query, top_k=args.top_k)
    
    print(f"Top {len(results)} results for query: {args.query}")
    for i, result in enumerate(results):
        print(f"\n{i+1}. {result['id']} (similarity: {result['similarity']:.4f})")
        print(f"   File: {result['file_path']}")
        print(f"   Content: {result['content'][:100]}...")


def command_pipeline(args):
    """Run the full pipeline."""
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)
    
    # Step 1: Summarize
    print("Step 1: Summarizing code...")
    summarizer = Summarizer()
    if os.path.isfile(args.path):
        summary = [summarizer.summarize_file(args.path)]
    else:
        summary = summarizer.summarize_directory(args.path, recursive=args.recursive)
    
    summary_path = os.path.join(output_dir, "summary.json")
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Summary written to {summary_path}")
    
    # Step 2: Chunk
    print("Step 2: Chunking code...")
    chunker = Chunker(chunk_size=args.chunk_size)
    chunks_dir = os.path.join(output_dir, "chunks")
    if os.path.isfile(args.path):
        chunks = chunker.chunk_file(args.path)
        os.makedirs(chunks_dir, exist_ok=True)
        with open(os.path.join(chunks_dir, "chunks.json"), 'w') as f:
            json.dump(chunks, f, indent=2)
    else:
        chunks = chunker.chunk_directory(args.path, output_dir=chunks_dir)
    
    # Step 3: Embed
    print("Step 3: Creating embeddings...")
    embedder = Embedder(model_name=args.model)
    embeddings = embedder.embed_chunks(chunks)
    
    embeddings_path = os.path.join(output_dir, "embeddings.json")
    embedder.save_embeddings(embeddings, embeddings_path)
    print(f"Embeddings saved to {embeddings_path}")
    
    print("Pipeline completed successfully!")


def main():
    """Main entry point for the CLI."""
    args = parse_args()
    
    if args.command == "summarize":
        command_summarize(args)
    elif args.command == "chunk":
        command_chunk(args)
    elif args.command == "embed":
        command_embed(args)
    elif args.command == "query":
        command_query(args)
    elif args.command == "pipeline":
        command_pipeline(args)
    else:
        print("Please specify a command. Use --help for more information.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
