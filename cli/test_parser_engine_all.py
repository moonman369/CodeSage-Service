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

def test(language, code):
    print(f"\n=== Testing {language.upper()} ===")
    parser = MultiParserEngine(language)
    output = parser.extract_all_features(code)
    # for key, items in output.items():
    #     print(f"\n[{key.upper()}]")
    #     for item in items:
    #         print(item)
    for key, items in output.items():
      print(f"\n[{key.upper()}]")
      if not items:
        print("No items found.")
        continue
      for item in items:
        print(item)
    print("-" * 100)

if __name__ == "__main__":
    # parser = MultiParserEngine("css")
    # print(parser.parse_code(sample_css))
    test("javascript", sample_js)
    test("java", sample_java)
    test("html", sample_html)
    test("yaml", sample_yaml)
    test("css", sample_css)
