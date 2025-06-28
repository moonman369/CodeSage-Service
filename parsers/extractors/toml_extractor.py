class TOMLKeyValueExtractor:
    def supports(self, language: str) -> bool:
        return language == "toml"

    def extract(self, root, code):
        kv_pairs = []

        def walk(node, prefix=""):
            if node.type == "pair":
                key_node = node.child_by_field_name("key")
                value_node = node.child_by_field_name("value")

                if key_node:
                    key = key_node.text.decode("utf8")
                    full_key = f"{prefix}.{key}" if prefix else key
                    kv_pairs.append({
                        "key": full_key,
                        "line": node.start_point[0] + 1
                    })

                    if value_node and value_node.type in ["table", "inline_table"]:
                        for child in value_node.named_children:
                            walk(child, full_key)

            # elif node.type == "table":
            else:
                for child in node.named_children:
                    walk(child, prefix)

        walk(root)
        return kv_pairs
