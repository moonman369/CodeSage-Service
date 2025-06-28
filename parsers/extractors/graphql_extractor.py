class GraphQLExtractor:
    def supports(self, language: str) -> bool:
        return language == "graphql"

    def extract(self, root, code):
        elements = []
        
        def walk(node):
            if node.type == "type_definition":
                name_node = node.child_by_field_name("name")
                name = name_node.text.decode("utf8") if name_node else "Unknown"
                
                elements.append({
                    "type": "type_definition",
                    "name": name,
                    "line": node.start_point[0] + 1
                })
            elif node.type == "field_definition":
                name_node = node.child_by_field_name("name")
                name = name_node.text.decode("utf8") if name_node else "Unknown"
                
                elements.append({
                    "type": "field",
                    "name": name,
                    "line": node.start_point[0] + 1
                })
            elif node.type == "operation_definition":
                operation_type = None
                for child in node.named_children:
                    if child.type == "operation_type":
                        operation_type = child.text.decode("utf8")
                        break
                
                elements.append({
                    "type": "operation",
                    "operation_type": operation_type or "query",
                    "line": node.start_point[0] + 1
                })
            elif node.type == "interface_definition" or node.type == "union_definition" or node.type == "enum_definition":
                name_node = node.child_by_field_name("name")
                name = name_node.text.decode("utf8") if name_node else "Unknown"
                
                elements.append({
                    "type": node.type.replace("_definition", ""),
                    "name": name,
                    "line": node.start_point[0] + 1
                })
            
            for child in node.named_children:
                walk(child)
        
        walk(root)
        return elements