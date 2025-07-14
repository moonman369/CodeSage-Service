from typing import Dict
from .interfaces import ChunkProcessorInterface, PromptBuilderInterface, LLMClientInterface


class LLMChunkProcessor(ChunkProcessorInterface):
    def __init__(self, prompt_builder: PromptBuilderInterface, llm_client: LLMClientInterface):
        self.prompt_builder = prompt_builder
        self.llm_client = llm_client

    def process_chunk(self, chunk: Dict) -> Dict:
        prompt = self.prompt_builder.build_prompt(chunk)
        response = self.llm_client.generate_response(prompt)
        chunk["llm_summary"] = response
        return chunk
