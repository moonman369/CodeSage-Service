class ConstantExtractor:
    def supports(self, language: str) -> bool:
        return language in ["python", "typescript", "java"]
    def extract(self, root, code):
        constants = []
        def walk(node):
            if node.type == "constant_declaration":
                name_node = node.child_by_field_name("name")
                name = name_node.text.decode("utf8") if name_node else "<unknown>"
                constants.append({"name": name, "line": node.start_point[0] + 1})
            for child in node.children:
                walk(child)
        walk(root)
        return constants
