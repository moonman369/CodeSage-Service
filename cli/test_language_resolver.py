from parsers.language_resolver import LanguageResolver

lang = LanguageResolver.resolve("main.md")  # returns "python"
print(lang)