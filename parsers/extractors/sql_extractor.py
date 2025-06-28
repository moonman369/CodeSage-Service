class SQLExtractor:
    def supports(self, language: str) -> bool:
        return language == "sql"

    def extract(self, root, code):
        sql_elements = []
        
        def walk(node):
            if node.type == "select_statement":
                sql_elements.append({
                    "type": "select_statement",
                    "line": node.start_point[0] + 1,
                    "text": node.text.decode("utf8")
                })
            elif node.type == "create_statement":
                sql_elements.append({
                    "type": "create_statement", 
                    "line": node.start_point[0] + 1,
                    "text": node.text.decode("utf8")
                })
            elif node.type == "insert_statement":
                sql_elements.append({
                    "type": "insert_statement",
                    "line": node.start_point[0] + 1,
                    "text": node.text.decode("utf8")
                })
            elif node.type == "update_statement":
                sql_elements.append({
                    "type": "update_statement",
                    "line": node.start_point[0] + 1,
                    "text": node.text.decode("utf8")
                })
            elif node.type == "delete_statement":
                sql_elements.append({
                    "type": "delete_statement",
                    "line": node.start_point[0] + 1,
                    "text": node.text.decode("utf8")
                })
                
            for child in node.named_children:
                walk(child)
                
        walk(root)
        return sql_elements