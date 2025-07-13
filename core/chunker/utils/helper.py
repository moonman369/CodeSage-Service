import os

def get_comment_prefix(language: str) -> str:
    """
    Returns the correct comment prefix string based on language.
    Used to prepend metadata to each code chunk.
    """
    comment_map = {
        "python": "#",
        "java": "//",
        "javascript": "//",
        "typescript": "//",
        "c": "//",
        "cpp": "//",
        "go": "//",
        "ruby": "#",
        "bash": "#",
        "sh": "#",
        "yaml": "#",
        "toml": "#",
        "json": "//",  # not valid JSON, but readable for LLMs
        "html": "<!--",  # not typical, but supported
        "css": "/*",
        "php": "//",
        "rust": "//",
        "kotlin": "//",
        "swift": "//",
        "scala": "//",
        "dart": "//"
    }
    return comment_map.get(language.lower(), "#")  # fallback to Python-style


def detect_language_from_extension(filename: str) -> str:
    ext_map = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".java": "java",
        ".cpp": "cpp",
        ".c": "c",
        ".rb": "ruby",
        ".sh": "bash",
        ".go": "go",
        ".html": "html",
        ".css": "css",
        ".json": "json",
        ".yaml": "yaml",
        ".toml": "toml",
        ".php": "php",
        ".rs": "rust",
        ".kt": "kotlin",
        ".swift": "swift",
        ".scala": "scala",
        ".dart": "dart"
    }
    _, ext = os.path.splitext(filename)
    return ext_map.get(ext.lower(), "plaintext")
