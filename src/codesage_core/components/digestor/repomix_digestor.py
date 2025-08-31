# core/summarizer/repomix_summarizer.py

from codesage_core.components.digestor.base_digestor import BaseDigestor
from repomix import RepoProcessor, RepomixConfig
import os
from dotenv import load_dotenv

load_dotenv()

DIGESTOR_REPOMIX_CONFIG_OUTPUT_STYLE = os.getenv("DIGESTOR_REPOMIX_CONFIG_OUTPUT_STYLE", "plain")

class RepomixDigestor(BaseDigestor):
    def digest_repo(self, repo_url: str) -> dict:
        # Extract project name from repo URL
        project_name = self._extract_project_name(repo_url)

        # Create custom configuration
        config = RepomixConfig()

        # Output settings
        # Store project name in output file name for segregation
        output_filename = "outputs/digestor/repomix_output.md"
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        config.output.file_path = output_filename
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
        config.ignore.custom_patterns = [
            # === Build artifacts ===
            "*.log",
            "*.tmp",
            "*.out",
            "*.o",
            "*.obj",
            "*.class",
            "*.exe",
            "*.dll",
            "*.so",
            "*.a",
            "*.lib",
            "*.pyc",
            "*.pyo",
            "*.ipynb_checkpoints/**",

            # === Dependency folders ===
            "node_modules/**",
            ".venv/**",
            "venv/**",
            "env/**",
            "__pycache__/**",
            "target/**",           # Rust, Maven
            "build/**",            # Common in many stacks
            "dist/**",             # Node, Python, etc.
            "bin/**",              # Java, Go
            "obj/**",              # .NET

            # === Version control & system files ===
            ".git/**",
            ".gitignore",
            ".gitattributes",
            ".github/**",
            ".DS_Store",
            "Thumbs.db",
            "*.swp",

            # === Editor/IDE configs ===
            ".idea/**",            # IntelliJ
            ".vscode/**",
            ".vs/**",              # Visual Studio

            # === Cache & temp folders ===
            ".cache/**",
            "cache/**",
            "tmp/**",
            "logs/**",
            "npm-cache/**",
            "yarn-cache/**",
            "coverage/**",
            "*.coverage",
            "*.lcov",
            "test-results/**",
            "reports/**",

            # === Docs, Markdown, Licenses ===
            "docs/**",
            "*.md",
            # 🚨 Whitelist all possible README variants
            "!README*",
            "!readme*",
            "!Readme*",
            "LICENSE",
            "LICENSE.txt",
            "LICENSE.md",
            "COPYING",

            # === Environment/Secrets/Boilerplate ===
            ".env",
            ".env.local",
            ".env.production",
            ".env.development",
            ".env.test",
            "*.key",
            "*.pem",
            "*.crt",

            # === Lock files / Manifest redundancies ===
            "package-lock.json",
            "yarn.lock",
            "pnpm-lock.yaml",
            "poetry.lock",
            "Pipfile.lock",
            "composer.lock",
            "*.iml",

            # === Static asset noise ===
            "*.png",
            "*.jpg",
            "*.jpeg",
            "*.svg",
            "*.gif",
            "*.ico",
            "*.mp4",
            "*.mp3",
            "*.woff",
            "*.woff2",
            "*.ttf",
            "*.eot",

            # === Large model/data/artifacts ===
            "*.h5",
            "*.pt",
            "*.ckpt",
            "*.tflite",
            "*.onnx",
            "*.zip",
            "*.tar",
            "*.gz",
            "*.7z",

            # === Generated output (RAG or otherwise) ===
            "outputs/**",
            "repomix-output.md",
            "*.json",
            "!manifest.json",     # Keep manifest context if needed
        ]

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
        result = processor.process(write_output=False)

        # Prepend project name to output content
        project_header = f"# Project: {project_name}\n\n# Project URL: {repo_url}\n\n"
        output_content = project_header + result.output_content

        # Write output file with project name at the top
        with open(config.output.file_path, "w", encoding="utf-8") as f:
            f.write(output_content)

        # Access processing results
        print(f"Total files: {result.total_files}")
        print(f"Total characters: {result.total_chars}")
        print(f"Total tokens: {result.total_tokens}")
        print(f"Output saved to: {result.config.output.file_path}")
        print(output_content)

        # Return output with project name for downstream segregation
        return {
            "content": output_content,
            "repository_url": repo_url,
            "project_name": project_name,
            "output_file": result.config.output.file_path,
        }

    def _extract_project_name(self, repo_url: str) -> str:
        """
        Extracts the project name from a git repository URL.
        E.g. https://github.com/user/project.git -> project
        """
        name = repo_url.rstrip('/').split('/')[-1]
        if name.endswith('.git'):
            name = name[:-4]
        return name

    def digest_directory(self, repo_path: str) -> dict:
        # Use the directory name as the project name
        project_name = os.path.basename(os.path.normpath(repo_path))

        # Create custom configuration
        config = RepomixConfig()

        # Store project name in output file name for segregation
        output_filename = f"{project_name}-repomix-output.md"
        config.output.file_path = os.path.join("outputs", output_filename)

        # Handle multiprocessing differently
        if os.name == 'nt':  # Windows
            # On Windows, limit to a single worker to avoid multiprocessing issues
            os.environ['REPOMIX_MAX_WORKERS'] = '1'

        processor = RepoProcessor(repo_path, config=config)
        result = processor.process(write_output=False)

        # Prepend project name to output content
        project_header = f"# Project: {project_name}\n\n# Project URL: {repo_path}\n\n"
        output_content = project_header + result.output_content

        # Write output file with project name at the top
        with open(config.output.file_path, "w", encoding="utf-8") as f:
            f.write(output_content)

        # Access processing results
        print(f"Total files: {result.total_files}")
        print(f"Total characters: {result.total_chars}")
        print(f"Total tokens: {result.total_tokens}")
        print(f"Output saved to: {result.config.output.file_path}")
        print(output_content)

        # Return output with project name for downstream segregation
        return {
            "content": output_content,
            "repository_path": repo_path,
            "project_name": project_name,
            "output_file": result.config.output.file_path,
        }
