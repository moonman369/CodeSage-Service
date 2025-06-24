class StyleExtractor:
    def supports(self, language: str) -> bool:
        return language == "css"

    def extract(self, root, code: str):
        if root is None:
            return []

        styles = []

        def walk(node):
            if node.type == "declaration":
                # Extract raw text of children instead of using field names
                children = node.children
                prop, val = "<unknown>", "<unknown>"

                if len(children) >= 3:
                    # Typically: [property_name, ':', value]
                    prop_node = children[0]
                    val_node = children[2]
                    prop = prop_node.text.decode("utf8")
                    val = val_node.text.decode("utf8")

                styles.append({
                    "property": prop,
                    "value": val,
                    "line": node.start_point[0] + 1
                })

            for child in node.children:
                walk(child)

        walk(root)
        return styles
