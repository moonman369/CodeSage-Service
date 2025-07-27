from .base_prompt_builder import BasePromptBuilder


class BasicPromptBuilder(BasePromptBuilder):
    def build_prompt_chunk(self, chunk: dict) -> str:
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
    
    def build_prompt_rag(self, chunk: dict) -> str:
        pass
