from typing import Dict
from .base_chunk_processor import BaseChunkProcessor
from core.prompt.base_prompt_builder import BasePromptBuilder
from core.llm.base_llm_client import BaseLLMClient


class LLMChunkProcessor(BaseChunkProcessor):
    def __init__(self, prompt_builder: BasePromptBuilder, llm_client: BaseLLMClient):
        self.prompt_builder = prompt_builder
        self.llm_client = llm_client

    def process_chunk(self, chunk: Dict) -> Dict:
        prompt = self.prompt_builder.build_prompt_chunk(chunk)
        response = self.llm_client.generate_response(prompt)
        chunk["llm_summary"] = response
        return chunk
