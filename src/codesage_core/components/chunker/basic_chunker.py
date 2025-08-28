import re
from typing import List, Dict
from codesage_core.components.chunker.base_chunker import BaseChunker
from codesage_core.components.chunker.utils.helper import detect_language_from_extension, get_comment_prefix

DEFAULT_CHUNK_SIZE = 80
DEFAULT_OVERLAP = 15

# Updated regex to match "## File: path/to/file"
FILE_SECTION_REGEX = re.compile(r"^## (.+)$", re.MULTILINE)

# Matches any code block like ```javascript\n1: line...\n2: line...\n```
CODE_BLOCK_REGEX = re.compile(r"```(\w+)\n(.*?)```", re.DOTALL)


class BasicChunker(BaseChunker):
    def __init__(self, chunk_size: int = DEFAULT_CHUNK_SIZE, overlap: int = DEFAULT_OVERLAP):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, markdown_digest: str) -> List[Dict]:
        # Extract project name from the top of the digest
        project_name = None
        project_match = re.search(r"^# Project: (.+)$", markdown_digest, re.MULTILINE)
        if project_match:
            project_name = project_match.group(1).strip()
        project_url = None
        project_match = re.search(r"^# Project URL: (.+)$", markdown_digest, re.MULTILINE)
        if project_match:
            project_url = project_match.group(1).strip()
        files = self._parse_markdown_digest(markdown_digest)
        all_chunks = []

        for file_block in files:
            code_chunks = self._chunk_code(
                code=file_block["code"],
                language=file_block["language"],
                file_path=file_block["file_path"],
                project_name=project_name,
                project_url=project_url
            )
            all_chunks.extend(code_chunks)

        return all_chunks

    def _parse_markdown_digest(self, text: str) -> List[Dict]:
        files = []
        file_matches = list(FILE_SECTION_REGEX.finditer(text))
        for idx, match in enumerate(file_matches):
            file_path = match.group(1).strip()
            section_start = match.end()
            section_end = file_matches[idx + 1].start() if idx + 1 < len(file_matches) else len(text)
            section_text = text[section_start:section_end]

            code_match = CODE_BLOCK_REGEX.search(section_text)
            if not code_match:
                continue

            language = code_match.group(1).strip()
            raw_code = code_match.group(2).strip()

            # Remove line numbers like "  1: some code"
            code_lines = [
                line.split(":", 1)[-1].lstrip()
                for line in raw_code.splitlines()
                if ":" in line
            ]
            cleaned_code = "\n".join(code_lines)

            files.append({
                "file_path": file_path,
                "language": language,
                "code": cleaned_code
            })

        return files

    def _chunk_code(self, code: str, language: str, file_path: str, project_name: str = None, project_url: str = None) -> List[Dict]:
        lines = code.splitlines()
        total_lines = len(lines)
        comment_prefix = get_comment_prefix(language)
        chunks = []
        chunk_index = 0
        start = 0

        while start < total_lines:
            end = min(start + self.chunk_size, total_lines)
            chunk_lines = lines[start:end]

            chunks.append({
                "chunk_summary": "",  # leave blank for now
                "metadata": {
                    "file_path": file_path,
                    "language": language,
                    "start_line": start + 1,
                    "end_line": end,
                    "chunk_index": chunk_index,
                    "total_chunks_in_file": (total_lines + self.chunk_size - 1) // self.chunk_size,
                    "source": "repomix-digest"
                },
                "raw_code": "\n".join(chunk_lines),
                "project_name": project_name,
                "project_url": project_url
            })

            chunk_index += 1
            if end == total_lines:
                break
            start += self.chunk_size - self.overlap

        return chunks
