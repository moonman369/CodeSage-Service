class StyleExtractor:
    def supports(self, language: str) -> bool:
        return language == "css"

    def extract(self, root, code: str):
        if root is None:
            return []

        styles = []

        def walk(node):
            if node.type == "rule_set":
                selector_text = "<unknown>"
                declarations = []

                # Extract the selector text
                selectors_node = next((c for c in node.children if c.type == "selectors"), None)
                if selectors_node:
                    selector_text = code[selectors_node.start_byte:selectors_node.end_byte].strip()

                # Extract declarations from the block
                block_node = next((c for c in node.children if c.type == "block"), None)
                if block_node:
                    for child in block_node.children:
                        if child.type == "declaration":
                            children = child.children
                            prop, val = "<unknown>", "<unknown>"

                            if len(children) >= 3:
                                prop = children[0].text.decode("utf8")
                                val = children[2].text.decode("utf8")

                            declarations.append({
                                "property": prop,
                                "value": val,
                                "line": child.start_point[0] + 1
                            })

                styles.append({
                    "selector": selector_text,
                    "declarations": declarations,
                    "line": node.start_point[0] + 1
                })

            for child in node.children:
                walk(child)

        walk(root)
        return styles
