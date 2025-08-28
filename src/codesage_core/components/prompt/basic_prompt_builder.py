from .base_prompt_builder import BasePromptBuilder
from typing import List, Dict


class BasicPromptBuilder(BasePromptBuilder):
    def build_prompt_chunk(self, chunk: Dict) -> str:
        file_path = chunk["metadata"]["file_path"]
        language = chunk["metadata"]["language"]
        start = chunk["metadata"]["start_line"]
        end = chunk["metadata"]["end_line"]
        code = chunk["raw_code"]

        return (
            f"You are an expert software engineer and technical documenter.\n"
            f"The following is a snippet of {language} code, taken from a larger codebase that is being analyzed in parts.\n"
            f"This snippet is one of many chunks extracted for semantic understanding and summarization.\n"
            f"\n"
            f"File Path: {file_path}\n"
            f"Lines: {start}-{end}\n"
            f"---\n"
            f"Code:\n"
            f"{code}\n"
            f"---\n"
            f"\n"
            f"Please answer the following:\n"
            f"1. What is this chunk of code doing? (Summarize in 4-5 sentences)\n"
            f"2. If possible, mention any functions, classes, or patterns it seems to belong to.\n"
            f"3. Mention any dependencies, environment variables, external modules, or other files this chunk interacts with.\n"
            f"4. Classify this code chunk as one of the following: configuration, utility/helper, controller/logic, route/entrypoint, model/schema, or unknown.\n"
            f"\n"
            f"Only return your summary and insights. Do not explain what you are doing or include extra formatting."
        )

    def build_prompt_rag(
        self,
        user_query: str,
        retrieved_chunks: List[Dict],
        system_prompt: str = "You are a helpful AI assistant that understands code and answers queries precisely.",
        max_context_chars: int = 4000,
    ) -> str:
        """
        Composes a complete prompt with top-K chunk context and user query.

        Parameters:
        - user_query: the actual question from the user
        - retrieved_chunks: top-K chunks from the vector database
        - system_prompt: optional system role message
        - max_context_chars: max allowed size for combined context

        Returns:
        - Full prompt string for the LLM
        """
        context_parts = []
        total_chars = 0

        for chunk in retrieved_chunks:
            # print(chunk)
            chunk_data = chunk.get("metadata", {})
            file_path = (
                chunk_data.get("metadata", {}).get("file_path") or "Unknown File"
            )
            summary = chunk_data.get("llm_summary", "").strip()
            raw_code = chunk_data.get("raw_code", "").strip()

            # Prefer summary if available
            if summary:
                part = f"[File: {file_path}]\nSummary: {summary}\n"
            else:
                snippet = raw_code[:500] + "..." if raw_code else "[No code available]"
                part = f"[File: {file_path}]\nCode Snippet:\n{snippet}\n"

            if total_chars + len(part) > max_context_chars:
                break

            context_parts.append(part)
            total_chars += len(part)

        context_str = "\n".join(context_parts)

        final_prompt = (
            f"{system_prompt}\n\n"
            f"Context:\n{context_str}\n\n"
            f"User Query:\n{user_query.strip()}"
        )

        return final_prompt
