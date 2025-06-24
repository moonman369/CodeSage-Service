class KeyValueExtractor:
    def supports(self, language: str) -> bool:
        return language in ["yaml", "toml", "json"]

    def extract(self, root, code: str):
        kv_pairs = []

        def walk(node, prefix=""):
            # YAML: block_mapping_pair
            if node.type in ("pair", "block_mapping_pair"):
                key = "<unknown>"

                # Get key
                if len(node.children) >= 1:
                    key_node = node.children[0]
                    key = key_node.text.decode("utf8")

                full_key = f"{prefix}.{key}" if prefix else key
                kv_pairs.append({
                    "key": full_key,
                    "line": node.start_point[0] + 1
                })

                # If nested object/value, keep walking
                if len(node.children) >= 2:
                    value_node = node.children[1]
                    walk(value_node, full_key)

            # TOML: tables and key-value pairs
            elif node.type == "table":
                for child in node.children:
                    walk(child, prefix)
            else:
                for child in node.children:
                    walk(child, prefix)

        walk(root)
        return kv_pairs
