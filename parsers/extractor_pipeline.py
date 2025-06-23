# parsers/extractor_pipeline.py

from parsers.extractors.function_extractor import FunctionExtractor
from parsers.extractors.class_extractor import ClassExtractor
from parsers.extractors.import_extractor import ImportExtractor
from parsers.extractors.variable_extractor import VariableExtractor

class FeatureExtractionPipeline:
    def __init__(self, language: str):
        self.parser = TreeSitterParser(language)
        self.language = language
        self.extractors = [
            FunctionExtractor(),
            ClassExtractor(),
            ImportExtractor(),
            VariableExtractor(),
        ]

    def extract_all(self, code: str) -> dict:
        root = self.parser.parse_code(code)
        results = {}

        for extractor in self.extractors:
            if extractor.supports(self.language):
                key = extractor.__class__.__name__.replace("Extractor", "").lower()
                results[key] = extractor.extract(root, code)

        return results
