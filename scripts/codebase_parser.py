import os
from parsers.language_resolver import LanguageResolver
from parsers.multi_parser_engine import MultiParserEngine

# Directories we should skip entirely
SKIP_DIRS = {
    ".git", ".venv", "env", "node_modules", "build", "dist",
    "__pycache__", ".mypy_cache", ".pytest_cache", "target",
    ".idea", ".vscode", ".coverage", ".next", ".cache"
}

# Extensions to skip (binaries, media, archives, etc.)
SKIP_EXTENSIONS = {
    ".pyc", ".class", ".o", ".exe", ".dll", ".so", ".zip", ".tar", ".gz",
    ".png", ".jpg", ".jpeg", ".svg", ".gif", ".mp3", ".mp4", ".avi",
    ".mov", ".ttf", ".ico", ".pdf", ".woff", ".woff2", ".eot", ".bin", ".gitignore", ".txt"
}

def is_valid_file(filepath: str) -> bool:
    ext = os.path.splitext(filepath)[1].lower()

    if ext in SKIP_EXTENSIONS:
        return False

    # Skip files with no extension or unknown language
    if not ext or LanguageResolver.resolve(filepath) is None:
        return False

    return True

def parse_codebase(root_dir: str) -> dict:
    results = {}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Remove skipped directories from traversal
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for filename in filenames:
            full_path = os.path.join(dirpath, filename)

            if not is_valid_file(full_path):
                continue

            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    code = f.read()

                language = LanguageResolver.resolve(full_path)
                parser = MultiParserEngine(language)
                features = parser.extract_all_features(code)

                results[full_path] = {
                    "language": language,
                    "features": features
                }

            except Exception as e:
                print(f"[Skip] {full_path}: {e}")
                continue

    return results
