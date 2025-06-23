class TagExtractor:
    def supports(self, language: str) -> bool:
        return language in ["html", "xml"] 
    def extract(self, root, code):
        tags = []
        def walk(node):
            if node.type == "start_tag":
                tag_name_node = node.child_by_field_name("tag_name")
                tag_name = tag_name_node.text.decode("utf8") if tag_name_node else "<unknown>"
                tags.append({"tag": tag_name, "start_line": node.start_point[0] + 1})
            for child in node.children:
                walk(child)
        walk(root)
        return tags