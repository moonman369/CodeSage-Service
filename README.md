# CodeSage: AI-Powered Code Documentation Tool

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

CodeSage is an intelligent code documentation assistant that leverages AI to automatically generate human-readable documentation from source code. It supports multiple programming languages and provides both CLI and Web API interfaces.

## Features

- **Multi-Language Support**: Parse code structures across different programming languages using Tree-sitter
- **AI-Powered Documentation**: Generate comprehensive docstrings using Large Language Models
- **Flexible Output Formats**: Insert docstrings directly into source code or export to markdown
- **Command-Line Interface**: Easily integrate into development workflows and CI/CD pipelines
- **Web API** (Planned): Access documentation capabilities through a web interface
- **Semantic Code Q&A** (Optional): Ask questions about your codebase using embeddings and semantic search

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/CodeSage-Service.git
cd CodeSage-Service

# Create a virtual environment
python -m venv codesage-venv

# Activate the environment
# On Windows:
codesage-venv\Scripts\activate
# On Unix/MacOS:
# source codesage-venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize Tree-sitter grammars (if needed)
# Instructions will be provided
```

## Usage

### Command Line Interface

```bash
# Generate documentation for a Python file
python -m cli.cli document path/to/your/file.py

# Generate documentation for an entire directory
python -m cli.cli document path/to/your/project/ --recursive

# Export documentation as markdown
python -m cli.cli document path/to/your/file.py --output markdown --output-path docs/

# Get help
python -m cli.cli --help
```

### Future Web Interface

A web interface is planned for future releases, which will provide:

- RESTful API endpoints for documentation generation
- Interactive UI for exploring and managing documentation
- Team collaboration features

## Architecture

CodeSage follows a modular, extensible architecture:

```
CodeSage-Service/
│
├── parsers/            # Code parsers for different languages
│   ├── __init__.py
│   └── ...
│
├── agents/             # LLM-based documentation generators
│   ├── __init__.py
│   └── ...
│
├── outputs/            # Documentation formatters and writers
│   ├── __init__.py
│   └── ...
│
├── cli/                # Command-line interface
│   ├── cli.py
│   └── ...
│
├── web/                # Future web API and interface
│   └── ...
│
├── embeddings/         # Vector storage and semantic search (planned)
│   └── ...
│
└── vendor/             # Tree-sitter grammars and external dependencies
    └── ...
```

## Extending CodeSage

### Adding Support for a New Language

To add support for a new programming language:

1. Add appropriate Tree-sitter grammar to the `vendor/` directory
2. Create a new parser in the `parsers/` module that implements the common parser interface
3. Register the new parser in the parser factory

### Custom Output Formats

To add a new output format:

1. Create a new writer class in the `outputs/` module
2. Implement the required methods to format and write documentation
3. Register the new format in the output format factory

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [OpenAI](https://openai.com/) for providing the LLM capabilities
- [Tree-sitter](https://tree-sitter.github.io/tree-sitter/) for robust code parsing
