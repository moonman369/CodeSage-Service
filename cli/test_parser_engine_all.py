from parsers.multi_parser_engine import MultiParserEngine

# Sample JS for functions, imports, variables, annotations, doc comments, constants
sample_js = """
// This is a doc comment
const MAX_USERS = 100;

@MyDecorator
export const fetchUserDetails = async () => {
  try {
    const response = await fetch('/api/user');
    return response;
  } catch (error) {
    console.error(error);
  }
};
"""

sample_java = """
import java.util.List;

// Java class example
public class UserService {
    private static final int MAX_USERS = 100;

    @Deprecated
    public void fetchUserDetails() {
        // Fetch user details logic
    }
}
"""

# Sample HTML
sample_html = """
<!DOCTYPE html>
<html>
  <head><title>Test Page</title></head>
  <body>
    <div id="main" class="container">
      <h1>Welcome</h1>
    </div>
  </body>
</html>
"""

# Sample YAML
sample_yaml = """
name: CodeSage
version: 1.0
dependencies:
  tree-sitter: latest
"""

# Sample CSS
sample_css = """
body {
  background-color: #fff;
}
.container {
  display: flex;
}
"""

# Sample JSON with nested objects and arrays
sample_json = """
{
  "project": "CodeSage",
  "version": "2.0.0",
  "settings": {
    "debug": false,
    "maxThreads": 4,
    "features": ["documentation", "analysis", "refactoring"]
  },
  "languages": [
    {
      "name": "python",
      "extensions": [".py", ".pyi"],
      "priority": 1
    },
    {
      "name": "javascript",
      "extensions": [".js", ".jsx"],
      "priority": 2,
      "config": {
        "parser": "babel",
        "sourceType": "module"
      }
    }
  ],
  "statistics": {
    "linesProcessed": 10000,
    "filesAnalyzed": 120,
    "performance": {
      "averageTime": 0.23,
      "peak": 1.45
    }
  }
}
"""

# Sample SQL with multiple statement types
sample_sql = """
-- Create a table for users
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO users (username, email) 
VALUES ('john_doe', 'john@example.com'),
       ('jane_smith', 'jane@example.com');

-- Query with JOIN and WHERE
SELECT u.username, p.title 
FROM users u
JOIN posts p ON u.user_id = p.user_id
WHERE u.created_at > '2023-01-01'
ORDER BY p.created_at DESC
LIMIT 10;

-- Update statement
UPDATE users 
SET last_login = CURRENT_TIMESTAMP
WHERE user_id IN (SELECT user_id FROM active_sessions);
"""

# Sample GraphQL schema
sample_graphql = """
type User {
  id: ID!
  username: String!
  email: String!
  posts: [Post!]
  profile: Profile
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  tags: [String!]
}

type Profile {
  bio: String
  avatar: String
  socialLinks: [String!]
}

interface Node {
  id: ID!
}

union SearchResult = User | Post

enum Role {
  ADMIN
  EDITOR
  VIEWER
}

type Query {
  user(id: ID!): User
  users: [User!]!
  search(term: String!): [SearchResult!]!
}

type Mutation {
  createUser(username: String!, email: String!): User!
  updateProfile(userId: ID!, bio: String, avatar: String): Profile
}
"""

def test(language, code):
    print(f"\n=== Testing {language.upper()} ===")
    parser = MultiParserEngine(language)
    output = parser.extract_all_features(code)
    for key, items in output.items():
      print(f"\n[{key.upper()}]")
      if not items:
        print("No items found.")
        continue
      for item in items:
        print(item)
    print("-" * 100)

if __name__ == "__main__":
    # parser = MultiParserEngine("json")
    # print(parser.parse_code(sample_json))
    test("javascript", sample_js)
    test("java", sample_java)
    test("html", sample_html)
    test("yaml", sample_yaml)
    test("css", sample_css)
    test("json", sample_json)
    # test("sql", sample_sql)         # Added SQL test
    # test("graphql", sample_graphql) # Added GraphQL test
