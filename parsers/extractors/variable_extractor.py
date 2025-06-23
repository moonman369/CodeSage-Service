# parsers/extractors/variable_extractor.py

class VariableExtractor:
    def supports(self, language: str) -> bool:
        return language in [
            "python", "javascript", "typescript", "tsx", "java", "go", "rust", "php"
        ]

    def extract(self, root, code: str):
        variables = []
        seen = set()

        def walk(node):
            if node.type == "variable_declarator":
                identifier_node = node.child_by_field_name("name")
                if identifier_node:
                    name = identifier_node.text.decode("utf8")
                    key = (name, node.start_point, node.end_point)
                    if key not in seen:
                        variables.append({
                            "name": name,
                            "start_line": node.start_point[0] + 1,
                            "end_line": node.end_point[0] + 1,
                        })
                        seen.add(key)
            for child in node.children:
                walk(child)

        walk(root)
        return variables
