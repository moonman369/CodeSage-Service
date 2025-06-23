# parsers/extractors/function_extractor.py

class FunctionExtractor:
    def supports(self, language: str) -> bool:
        return language in [
            "python", "javascript", "typescript", "tsx", "java", "c", "cpp",
            "go", "rust", "php", "ruby", "kotlin", "scala"
        ]

    def extract(self, root, code: str):
        functions = []

        def walk(node):
            if node.type in ("function_definition", "function_declaration", "method_definition"):
                name_node = node.child_by_field_name("name")
                name = name_node.text.decode("utf8") if name_node else "<anonymous>"
                functions.append({
                    "name": name,
                    "start_line": node.start_point[0] + 1,
                    "end_line": node.end_point[0] + 1,
                })

            # For arrow functions or anonymous function expressions
            if node.type in ("lexical_declaration", "variable_declarator"):
                for child in node.children:
                    if child.type in ("arrow_function", "function"):
                        name = "<anonymous>"
                        # Try to find identifier
                        identifier_node = next(
                            (c for c in node.children if c.type == "identifier"), None)
                        if identifier_node:
                            name = identifier_node.text.decode("utf8")
                        functions.append({
                            "name": name,
                            "start_line": node.start_point[0] + 1,
                            "end_line": node.end_point[0] + 1,
                        })
            for child in node.children:
                walk(child)

        walk(root)
        return functions
