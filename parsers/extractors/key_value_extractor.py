class KeyValueExtractor:
    def supports(self, language: str) -> bool:
        return language in ["yaml", "toml", "json"]
    def extract(self, root, code):
        kv_pairs = []
        def walk(node, prefix=""):
            if node.type == "pair":
                key_node = node.child_by_field_name("key")
                value_node = node.child_by_field_name("value")
                key = key_node.text.decode("utf8") if key_node else "<unknown>"
                full_key = f"{prefix}.{key}" if prefix else key
                kv_pairs.append({"key": full_key, "line": node.start_point[0] + 1})
                if value_node.type == "object":
                    for child in value_node.children:
                        walk(child, prefix=full_key)
            for child in node.children:
                walk(child, prefix)
        walk(root)
        return kv_pairs