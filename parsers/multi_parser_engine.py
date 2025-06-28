# parsers/multi_parser_engine.py

from tree_sitter import Parser, Language

# Import each installed grammar package
import tree_sitter_python
import tree_sitter_javascript
import tree_sitter_typescript
import tree_sitter_java
import tree_sitter_c
import tree_sitter_cpp
import tree_sitter_c_sharp
import tree_sitter_go
import tree_sitter_rust
import tree_sitter_ruby
import tree_sitter_php
import tree_sitter_bash
import tree_sitter_lua
import tree_sitter_html
import tree_sitter_css
import tree_sitter_json
import tree_sitter_yaml
import tree_sitter_toml
import tree_sitter_markdown
import tree_sitter_sql
import tree_sitter_kotlin
import tree_sitter_scala
import tree_sitter_elixir
import tree_sitter_haskell
import tree_sitter_fortran
import tree_sitter_graphql
import tree_sitter_groovy
import tree_sitter_arduino
import tree_sitter_make
import tree_sitter_scss
import tree_sitter_svelte
import tree_sitter_solidity

# Extractors
from parsers.extractors.function_extractor import FunctionExtractor
from parsers.extractors.class_extractor import ClassExtractor
from parsers.extractors.import_extractor import ImportExtractor
from parsers.extractors.variable_extractor import VariableExtractor
from parsers.extractors.constant_extractor import ConstantExtractor
from parsers.extractors.doc_comment_extractor import DocCommentExtractor
from parsers.extractors.key_value_extractor import KeyValueExtractor
from parsers.extractors.style_extractor import StyleExtractor
from parsers.extractors.tag_extractor import TagExtractor
from parsers.extractors.annotation_extractor import AnnotationExtractor
from parsers.extractors.json_extractor import JSONKeyValueExtractor
from parsers.extractors.yaml_extractor import YAMLKeyValueExtractor
from parsers.extractors.toml_extractor import TOMLKeyValueExtractor
from parsers.extractors.sql_extractor import SQLExtractor
from parsers.extractors.graphql_extractor import GraphQLExtractor



LANGUAGE_BUILDERS = {
    "python": Language(tree_sitter_python.language()),
    "javascript": Language(tree_sitter_javascript.language()),
    "typescript": Language(tree_sitter_typescript.language_typescript()),
    "tsx": Language(tree_sitter_typescript.language_tsx()),
    "java": Language(tree_sitter_java.language()),
    "c": Language(tree_sitter_c.language()),
    "cpp": Language(tree_sitter_cpp.language()),
    "c_sharp": Language(tree_sitter_c_sharp.language()),
    "go": Language(tree_sitter_go.language()),
    "rust": Language(tree_sitter_rust.language()),
    "ruby": Language(tree_sitter_ruby.language()),
    "php": Language(tree_sitter_php.language_php()),
    "bash": Language(tree_sitter_bash.language()),
    "lua": Language(tree_sitter_lua.language()),
    "html": Language(tree_sitter_html.language()),
    "css": Language(tree_sitter_css.language()),
    "json": Language(tree_sitter_json.language()),
    "yaml": Language(tree_sitter_yaml.language()),
    "toml": Language(tree_sitter_toml.language()),
    "markdown": Language(tree_sitter_markdown.language()),
    "sql": Language(tree_sitter_sql.language()),
    "kotlin": Language(tree_sitter_kotlin.language()),
    "scala": Language(tree_sitter_scala.language()),
    "elixir": Language(tree_sitter_elixir.language()),
    "haskell": Language(tree_sitter_haskell.language()),
    "fortran": Language(tree_sitter_fortran.language()),
    "graphql": Language(tree_sitter_graphql.language()),
    "groovy": Language(tree_sitter_groovy.language()),
    "arduino": Language(tree_sitter_arduino.language()),
    "make": Language(tree_sitter_make.language()),
    "scss": Language(tree_sitter_scss.language()),
    "svelte": Language(tree_sitter_svelte.language()),
    "solidity": Language(tree_sitter_solidity.language()),
}

EXTRACTORS = [
    FunctionExtractor(),
    ClassExtractor(),
    ImportExtractor(),
    VariableExtractor(),
    ConstantExtractor(),
    DocCommentExtractor(),
    KeyValueExtractor(),
    StyleExtractor(),
    TagExtractor(),
    AnnotationExtractor(),
    JSONKeyValueExtractor(),
    YAMLKeyValueExtractor(),
    TOMLKeyValueExtractor(),
    SQLExtractor(),
    GraphQLExtractor(),
]

class MultiParserEngine:
    def __init__(self, language_name: str):
        if language_name not in LANGUAGE_BUILDERS:
            raise ValueError(f"Unsupported language: {language_name}")
        self.language = language_name
        lang = LANGUAGE_BUILDERS[language_name]
        self.parser = Parser(lang)

    def parse_code(self, code: str):
        return self.parser.parse(bytes(code, "utf8")).root_node

    def extract_all_features(self, code: str) -> dict:
        root = self.parse_code(code)
        results = {}
        for extractor in EXTRACTORS:
            if extractor.supports(self.language):
                print(f"Using extractor: {extractor.__class__.__name__} for language: {self.language}")
                key = extractor.__class__.__name__.replace("Extractor", "").lower()
                results[key] = extractor.extract(root, code)
        return results
