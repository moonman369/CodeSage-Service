# cli/test_parser.py

from parsers.multi_parser_engine import MultiParserEngine

# sample_py = """
# def add(x, y):
#     return x + y

# class User:
#     def greet(self):
#         print("hi")
# """

# parser = TreeSitterParser("python")
# print("Python functions:", parser.extract_functions(sample_py))

sample_js = """
import { apiSummary } from "../config/api/apiSummary";
import customAxios from "./customAxios";

// test commnent
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

parser_js = MultiParserEngine("javascript")
print("JS functions:", parser_js.extract_all_features(sample_js))
