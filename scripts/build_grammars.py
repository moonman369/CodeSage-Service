from tree_sitter import Parser
from tree_sitter_languages import get_parser

# Initialize a language mapping

LANGUAGE_MAP = {
    "python": get_parser("python"),
    "javascript": get_parser("javascript"),
    "typescript": get_parser("typescript"),
    "tsx": get_parser("tsx"),
    "java": get_parser("java"),
    "c": get_parser("c"),
    "cpp": get_parser("cpp"),
    "c_sharp": get_parser("c-sharp"),
    "go": get_parser("go"),
    "rust": get_parser("rust"),
    "ruby": get_parser("ruby"),
    "php": get_parser("php"),
    "bash": get_parser("bash"),
    "lua": get_parser("lua"),
    "html": get_parser("html"),
    "css": get_parser("css"),
    "json": get_parser("json"),
    "yaml": get_parser("yaml"),
    "toml": get_parser("toml"),
    "markdown": get_parser("markdown"),
    "sql": get_parser("sql"),
    "swift": get_parser("swift"),
    "kotlin": get_parser("kotlin"),
    "dart": get_parser("dart"),
    "scala": get_parser("scala"),
    "elixir": get_parser("elixir"),
    "haskell": get_parser("haskell"),
}
def get_parser(language_key: str) -> Parser:
    if language_key not in LANGUAGE_MAP:
        raise ValueError(f"Unsupported language: {language_key}")
    
    parser = Parser()
    parser.set_language(LANGUAGE_MAP[language_key])
    return parser

# Try with Python
parser = get_parser("python")
tree = parser.parse(b"def foo(): return 42")
print(tree.root_node.sexp())  # e.g., (module (function_definition ...))
