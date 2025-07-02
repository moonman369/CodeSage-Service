"""
Summarizer that interfaces with RepoMix/GitIngest to provide code summaries.
"""
from typing import Dict, List, Optional, Union
import os
import json


class Summarizer:
    """
    Generates summaries of code repositories by interfacing with RepoMix/GitIngest.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the summarizer with optional configuration.
        
        Args:
            config_path: Path to configuration file for the summarizer
        """
        self.config = {}
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.load(f)
    
    def summarize_file(self, file_path: str) -> Dict:
        """
        Generate a summary for a single file.
        
        Args:
            file_path: Path to the file to summarize
            
        Returns:
            Dictionary containing summary data
        """
        # Implementation to interface with RepoMix/GitIngest
        # This is a placeholder for the actual implementation
        return {
            "file_path": file_path,
            "summary": "Placeholder summary for " + os.path.basename(file_path),
            "tokens": 0,
            "language": self._detect_language(file_path)
        }
    
    def summarize_directory(self, dir_path: str, recursive: bool = True) -> List[Dict]:
        """
        Generate summaries for all files in a directory.
        
        Args:
            dir_path: Path to the directory
            recursive: Whether to recursively process subdirectories
            
        Returns:
            List of dictionaries containing summary data for each file
        """
        summaries = []
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    summary = self.summarize_file(file_path)
                    summaries.append(summary)
                except Exception as e:
                    print(f"Error summarizing {file_path}: {str(e)}")
            
            if not recursive:
                break
                
        return summaries
    
    def summarize_repository(self, repo_url: str, output_path: Optional[str] = None) -> Dict:
        """
        Generate summaries for an entire git repository.
        
        Args:
            repo_url: URL of the git repository
            output_path: Path to save the output summary
            
        Returns:
            Dictionary with repository summary data
        """
        # Implementation to clone and process the repository
        # This is a placeholder for the actual implementation
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        summary = {
            "repo_name": repo_name,
            "repo_url": repo_url,
            "summary": f"Placeholder repository summary for {repo_name}",
            "file_count": 0,
            "files": []
        }
        
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(summary, f, indent=2)
                
        return summary
    
    def _detect_language(self, file_path: str) -> str:
        """
        Detect the programming language of a file based on its extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            String representing the detected language
        """
        extension = os.path.splitext(file_path)[1].lower()
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.c': 'c',
            '.cpp': 'cpp',
            '.cs': 'c#',
            '.go': 'go',
            '.rb': 'ruby',
            '.php': 'php',
            '.rs': 'rust',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
        }
        return language_map.get(extension, 'unknown')
