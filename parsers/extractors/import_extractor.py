# parsers/extractors/import_extractor.py

class ImportExtractor:
    def supports(self, language: str) -> bool:
        return language in [
            "python", "javascript", "typescript", "tsx", "java", "go", "rust"
        ]

    def extract(self, root, code: str):
        imports = []

        def walk(node):
            if node.type in ("import_statement", "import_declaration"):
                imports.append({
                    "start_line": node.start_point[0] + 1,
                    "end_line": node.end_point[0] + 1,
                    "type": node.type,
                })
            for child in node.children:
                walk(child)

        walk(root)
        return imports
