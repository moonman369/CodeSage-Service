# cli/test_parser.py

from parsers.multi_parser import TreeSitterParser

sample_py = """
def add(x, y):
    return x + y

class User:
    def greet(self):
        print("hi")
"""

# parser = TreeSitterParser("python")
# print("Python functions:", parser.extract_functions(sample_py))

sample_js = """
import { apiSummary } from "../config/api/apiSummary";
import customAxios from "./customAxios";

export const fetchUserDetails = async () => {
  try {
    const response = await customAxios({
      url: apiSummary.endpoints.user.getUserDetails.path,
      method: apiSummary.endpoints.user.getUserDetails.method,
    });
    return response;
  } catch (error) {
    console.error(error);
  }
};

"""

parser_js = TreeSitterParser("javascript")
print("JS functions:", parser_js.parse_code(sample_js))
