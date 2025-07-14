# core/processor/chunk_processor.py

import os
import json
from typing import List, Dict
from core.summarizer.interfaces import LLMClientInterface, ChunkProcessorInterface, PromptBuilderInterface
from core.summarizer.basic_prompt_builder import BasicPromptBuilder
from core.summarizer.chunk_processor import LLMChunkProcessor
from core.chunker.basic_chunker import BasicChunker
from test.chunker.test_basic_chunker import read_digest_from_root
from core.summarizer.openrouter_ai_client import OpenRouterAIClient


def test_chunk_processor(
    chunks: List[Dict],
    chunk_processor: ChunkProcessorInterface,
    output_dir: str = "outputs/summarized-chunks.txt"
) -> None:
    """
    Processes chunks using the provided chunk processor and saves the results.
    
    :param chunks: List of chunk dictionaries to be processed.
    :param chunk_processor: An instance of ChunkProcessorInterface to process chunks.
    :param output_dir: Directory where individual processed chunks will be saved.
    """
    # Create outputs directory relative to project root
    root_outputs_dir = os.path.join(".", "outputs")
    os.makedirs(root_outputs_dir, exist_ok=True)
    
    # Create directory for individual chunk outputs
    chunks_output_dir = os.path.join(root_outputs_dir, "chunks")
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "outputs", "summaries")
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each chunk and collect results
    all_processed_chunks = []
    
    for i, chunk in enumerate(chunks):
        # Process the chunk
        print(f"Processing chunk {i + 1}/{len(chunks)}: {chunk['metadata']['file_path']}")
        processed_chunk = chunk_processor.process_chunk(chunk)
        all_processed_chunks.append(processed_chunk)
        
        # Save individual chunk to its own file
        # individual_output_file = os.path.join(chunks_output_dir, f"chunk_{i + 1}_output.json")
        # with open(individual_output_file, 'w', encoding='utf-8') as f:
        #     json.dump(processed_chunk, f, indent=4)
        
        # print(f"Processed chunk {i + 1} and saved to {individual_output_file}")
    
    # Save all processed chunks to a single output file in ./outputs
    all_chunks_output_file = os.path.join(output_dir, "all_chunks_output.json")
    with open(all_chunks_output_file, 'w', encoding='utf-8') as f_all:
        json.dump(all_processed_chunks, f_all, indent=4)
    
    print(f"\nAll {len(all_processed_chunks)} chunks processed and saved to {all_chunks_output_file}")


if __name__ == "__main__":
    markdown_digest = read_digest_from_root()
    
    chunker = BasicChunker(chunk_size=80, overlap=15)
    chunks = chunker.chunk(markdown_digest)

    chunk_processor = LLMChunkProcessor(
        prompt_builder=BasicPromptBuilder(),
        llm_client=OpenRouterAIClient()
    )

    test_chunk_processor(chunks, chunk_processor)

