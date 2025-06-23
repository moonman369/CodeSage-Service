class StyleExtractor:
    def supports(self, language: str) -> bool:
        return language in ["css", "scss"]
    def extract(self, root, code):
        styles = []
        def walk(node):
            if node.type == "rule_set":
                selector = ""
                for child in node.children:
                    if child.type == "selector":
                        selector = child.text.decode("utf8")
                styles.append({"selector": selector, "start_line": node.start_point[0] + 1})
            for child in node.children:
                walk(child)
        walk(root)