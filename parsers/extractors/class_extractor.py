# parsers/extractors/class_extractor.py

class ClassExtractor:
    def supports(self, language: str) -> bool:
        return language in [
            "python", "javascript", "typescript", "tsx", "java", "c_sharp",
            "ruby", "php", "kotlin", "scala"
        ]

    def extract(self, root, code: str):
        classes = []

        def walk(node):
            if node.type in ("class_definition", "class_declaration"):
                name_node = node.child_by_field_name("name")
                name = name_node.text.decode("utf8") if name_node else "<anonymous>"
                classes.append({
                    "name": name,
                    "start_line": node.start_point[0] + 1,
                    "end_line": node.end_point[0] + 1,
                })
            for child in node.children:
                walk(child)

        walk(root)
        return classes
