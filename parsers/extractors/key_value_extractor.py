# class KeyValueExtractor:
#     def supports(self, language: str) -> bool:
#         return language in ["yaml", "toml", "json"]

#     def extract(self, root, code: str):
#         kv_pairs = []

#         def walk(node, prefix=""):
#             # YAML: block_mapping_pair
#             if node.type in ("pair", "block_mapping_pair"):
#                 key = "<unknown>"

#                 # Get key
#                 if len(node.children) >= 1:
#                     key_node = node.children[0]
#                     key = key_node.text.decode("utf8")

#                 full_key = f"{prefix}.{key}" if prefix else key
#                 kv_pairs.append({
#                     "key": full_key,
#                     "line": node.start_point[0] + 1
#                 })

#                 # If nested object/value, keep walking
#                 if len(node.children) >= 2:
#                     value_node = node.children[1]
#                     walk(value_node, full_key)

#             # TOML: tables and key-value pairs
#             elif node.type == "table":
#                 for child in node.children:
#                     walk(child, prefix)
#             else:
#                 for child in node.children:
#                     walk(child, prefix)

#         walk(root)
#         return kv_pairs
class KeyValueExtractor:
    SUPPORTED_LANGUAGES = []

    GRAMMAR_CONFIG = {
        "json": {
            "pair": "pair",
            "key_field": "key",
            "value_field": "value"
        },
        "yaml": {
            "pair": "block_mapping_pair",
            "key_field": "key",
            "value_field": "value"
        },
        "toml": {
            "pair": "pair",
            "key_field": "key",
            "value_field": "value"
        }
    }

    def supports(self, language: str) -> bool:
        return language in self.SUPPORTED_LANGUAGES

    def extract(self, root, code, language):
        if language not in self.GRAMMAR_CONFIG:
            return []
        config = self.GRAMMAR_CONFIG[language]
        pair_type = config["pair"]
        key_field = config["key_field"]
        value_field = config["value_field"]

        kv_pairs = []

        def walk(node, prefix=""):
            if node.type == pair_type:
                key_node = node.child_by_field_name(key_field)
                value_node = node.child_by_field_name(value_field)
                key = key_node.text.decode("utf8") if key_node else "<unknown>"
                full_key = f"{prefix}.{key}" if prefix else key
                kv_pairs.append({
                    "key": full_key,
                    "line": node.start_point[0] + 1
                })
                # Recurse if value is a nested object/array
                if value_node:
                    for child in value_node.children:
                        walk(child, prefix=full_key)
            else:
                for child in node.children:
                    walk(child, prefix)
        walk(root)
        return kv_pairs
