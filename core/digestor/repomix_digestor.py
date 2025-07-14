# core/summarizer/repomix_summarizer.py

from core.digestor.base_digestor import BaseDigestor
from repomix import RepoProcessor, RepomixConfig
import os
from dotenv import load_dotenv

load_dotenv()

DIGESTOR_REPOMIX_CONFIG_OUTPUT_STYLE = os.getenv("DIGESTOR_REPOMIX_CONFIG_OUTPUT_STYLE", "plain")

class RepomixDigestor(BaseDigestor):
    def digest_repo(self, repo_url: str) -> str:
        # Create custom configuration
        config = RepomixConfig()

        # Output settings
        # config.output.file_path = "custom-output.md"
        config.output.style = DIGESTOR_REPOMIX_CONFIG_OUTPUT_STYLE # supports "plain", "markdown", and "xml"
        config.output.show_line_numbers = True
        config.output.copy_to_clipboard = True
        config.output.calculate_tokens = True

        # Security settings
        config.security.enable_security_check = True
        config.security.exclude_suspicious_files = True

        # Compression settings
        config.compression.enabled = True
        config.compression.keep_signatures = True
        config.compression.keep_docstrings = True
        config.compression.keep_interfaces = True  # Interface mode for API documentation

        # Include/Ignore patterns
        # config.include = ["src/**/*", "tests/**/*"]
        config.ignore.custom_patterns = ["*.log", "*.tmp"]
        config.ignore.use_gitignore = True

        # Remote repository configuration
        config.remote.url = repo_url
        config.remote.branch = "main"  # Changed to "main" as it's more common now
        
        # Handle multiprocessing differently
        if os.name == 'nt':  # Windows
            # On Windows, limit to a single worker to avoid multiprocessing issues
            os.environ['REPOMIX_MAX_WORKERS'] = '1'
        
        # Process repository with custom config
        processor = RepoProcessor(repo_url=repo_url, config=config)
        result = processor.process(write_output=True)

        # Access processing results
        print(f"Total files: {result.total_files}")
        print(f"Total characters: {result.total_chars}")
        print(f"Total tokens: {result.total_tokens}")
        print(f"Output saved to: {result.config.output.file_path}")
        print(result.output_content)
        
        return result.output_content

    def digest_directory(self, repo_path: str) -> str:
        # Create custom configuration
        config = RepomixConfig()
        
        # Handle multiprocessing differently
        if os.name == 'nt':  # Windows
            # On Windows, limit to a single worker to avoid multiprocessing issues
            os.environ['REPOMIX_MAX_WORKERS'] = '1'
            
        processor = RepoProcessor(repo_path, config=config)
        result = processor.process()

        # Access processing results
        print(f"Total files: {result.total_files}")
        print(f"Total characters: {result.total_chars}")
        print(f"Total tokens: {result.total_tokens}")
        print(f"Output saved to: {result.config.output.file_path}")
        
        return result.output_content
