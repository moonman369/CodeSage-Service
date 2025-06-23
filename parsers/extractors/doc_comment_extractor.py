class DocCommentExtractor:
    def supports(self, language: str) -> bool:
        return language in ["python", "javascript", "java", "typescript"]
    def extract(self, root, code):
        comments = []
        def walk(node):
            if node.type in ("comment", "documentation_comment"):
                text = node.text.decode("utf8")
                comments.append({"doc": text.strip(), "line": node.start_point[0] + 1})
            for child in node.children:
                walk(child)
        walk(root)
        return comments