class JSONKeyValueExtractor:
    def supports(self, language: str) -> bool:
        return language == "json"

    def extract(self, root, code):
        kv_pairs = []

        def get_node_text(node):
            return code[node.start_byte:node.end_byte].strip()

        def walk(node, prefix=""):
            if node.type == "pair":
                key_node = node.child_by_field_name("key")
                value_node = node.child_by_field_name("value")

                if key_node:
                    # Extract actual key string (handle string_content inside string)
                    if key_node.type == "string":
                        content_node = key_node.child_by_field_name("content")
                        key_text = get_node_text(content_node) if content_node else get_node_text(key_node)
                    else:
                        key_text = get_node_text(key_node)

                    full_key = f"{prefix}.{key_text}" if prefix else key_text
                    kv_pairs.append({
                        "key": full_key,
                        "line": node.start_point[0] + 1
                    })

                # Dive deeper into nested objects/arrays
                if value_node:
                    if value_node.type == "object":
                        for child in value_node.named_children:
                            walk(child, prefix=full_key)
                    elif value_node.type == "array":
                        for idx, element in enumerate(value_node.named_children):
                            indexed_prefix = f"{full_key}[{idx}]"
                            walk(element, prefix=indexed_prefix)

            # elif node.type == "object" or node.type == "array":
            else:
                for child in node.named_children:
                    walk(child, prefix)

        walk(root)
        return kv_pairs
