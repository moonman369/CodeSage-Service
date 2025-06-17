# parsers/treesitter_parser.py

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

class TreeSitterParser:
    def __init__(self, language_name: str):
        if language_name not in LANGUAGE_BUILDERS:
            raise ValueError(f"Unsupported language: {language_name}")
        lang = LANGUAGE_BUILDERS[language_name]
        self.parser = Parser(lang)

    def parse_code(self, code: str):
        return self.parser.parse(bytes(code, "utf8")).root_node

    def extract_functions(self, code: str):
        root = self.parse_code(code)
        funcs = []

        def walk(node):
            if node.type in ("function_definition", "method_definition", "function"):
                name_node = node.child_by_field_name("name")
                name = name_node.text.decode("utf8") if name_node else "<anonymous>"
                funcs.append({
                    "name": name,
                    "start_line": node.start_point[0] + 1,
                    "end_line": node.end_point[0] + 1,
                })
            for child in node.children:
                walk(child)
        walk(root)
        return funcs
