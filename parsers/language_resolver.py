# parsers/language_resolver.py

from pathlib import Path


# def resolve_language(file_path: str) -> str | None:
#     ext = Path(file_path).suffix
#     return EXTENSION_MAP.get(ext)

class LanguageResolver:
    EXTENSION_MAP = {
        # Python
        ".py": "python",
        ".pyi": "python",
        ".pyc": "python",
        ".pyd": "python",
        ".pyw": "python",
        
        # JavaScript
        ".js": "javascript",
        ".jsx": "javascript",
        ".mjs": "javascript",
        ".cjs": "javascript",
        
        # TypeScript
        ".ts": "typescript",
        ".tsx": "tsx",
        ".d.ts": "typescript",
        
        # Java
        ".java": "java",
        ".jar": "java",
        
        # C/C++
        ".c": "c",
        ".h": "c",
        ".cpp": "cpp",
        ".cc": "cpp",
        ".cxx": "cpp",
        ".hpp": "cpp",
        ".hxx": "cpp",
        
        # C#
        ".cs": "c_sharp",
        
        # Go
        ".go": "go",
        
        # Rust
        ".rs": "rust",
        
        # Ruby
        ".rb": "ruby",
        ".erb": "ruby",
        
        # PHP
        ".php": "php",
        ".phtml": "php",
        
        # Bash
        ".sh": "bash",
        ".bash": "bash",
        
        # Lua
        ".lua": "lua",
        
        # HTML
        ".html": "html",
        ".htm": "html",
        
        # CSS
        ".css": "css",
        
        # JSON
        ".json": "json",
        
        # YAML
        ".yaml": "yaml",
        ".yml": "yaml",
        
        # TOML
        ".toml": "toml",
        
        # Markdown
        ".md": "markdown",
        ".markdown": "markdown",
        
        # SQL
        ".sql": "sql",
        
        # Kotlin
        ".kt": "kotlin",
        ".kts": "kotlin",
        
        # Scala
        ".scala": "scala",
        ".sc": "scala",
        
        # Elixir
        ".ex": "elixir",
        ".exs": "elixir",
        
        # Haskell
        ".hs": "haskell",
        ".lhs": "haskell",
        
        # Fortran
        ".f": "fortran",
        ".f90": "fortran",
        ".f95": "fortran",
        ".f03": "fortran",
        
        # GraphQL
        ".graphql": "graphql",
        ".gql": "graphql",
        
        # Groovy
        ".groovy": "groovy",
        ".gvy": "groovy",
        ".gradle": "groovy",
        
        # Arduino
        ".ino": "arduino",
        
        # Makefile
        ".mk": "make",
        "Makefile": "make",
        ".makefile": "make",
        
        # SCSS
        ".scss": "scss",
        
        # Svelte
        ".svelte": "svelte",
        
        # Solidity
        ".sol": "solidity",
    }
     
    @classmethod
    def resolve(cls, filename: str) -> str:
            for ext, lang in cls.EXTENSION_MAP.items():
                if filename.endswith(ext):
                    return lang
            raise ValueError(f"Unsupported or unknown file extension for file: {filename}")