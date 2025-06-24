class TagExtractor:
    def supports(self, language):
        return language in ["html", "xml"]

    def extract(self, root, code: str):
        tags = []

        def walk(node):
            if node.type == "element":
                tag_name = "<unknown>"
                attributes = {}

                for child in node.children:
                    if child.type == "start_tag":
                        for tag_child in child.children:
                            if tag_child.type == "tag_name":
                                tag_name = tag_child.text.decode("utf8")
                            elif tag_child.type == "attribute":
                                attr_name = None
                                attr_value = None
                                for attr_child in tag_child.children:
                                    if attr_child.type == "attribute_name":
                                        attr_name = attr_child.text.decode("utf8")
                                    elif attr_child.type == "quoted_attribute_value":
                                        attr_value = attr_child.text.decode("utf8").strip('"')
                                if attr_name:
                                    attributes[attr_name] = attr_value

                tags.append({
                    "tag": tag_name,
                    "start_line": node.start_point[0] + 1,
                    "end_line": node.end_point[0] + 1,
                    "attributes": attributes
                })

            for child in node.children:
                walk(child)

        walk(root)
        return tags
