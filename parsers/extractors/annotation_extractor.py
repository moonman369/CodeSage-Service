class AnnotationExtractor:
    def supports(self, language: str) -> bool:
            return language in ["python", "java", "typescript"]
    def extract(self, root, code):
        annotations = []
        def walk(node):
            if node.type == "annotation":
                name = node.text.decode("utf8")
                annotations.append({"decorator": name, "line": node.start_point[0] + 1})
            for child in node.children:
                walk(child)
        walk(root)
        return annotations