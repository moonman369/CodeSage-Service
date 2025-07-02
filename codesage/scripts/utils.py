"""
Utility functions for CodeSage operations.
"""
import os
import json
import logging
from typing import Dict, List, Any, Optional, Union
import re


def setup_logging(log_level: str = "INFO"):
    """
    Set up logging configuration.
    
    Args:
        log_level: The log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")
    
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("codesage.log")
        ]
    )


def load_json(file_path: str) -> Dict:
    """
    Load JSON from a file.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Loaded JSON as dictionary
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Dict, file_path: str):
    """
    Save dictionary as JSON file.
    
    Args:
        data: Dictionary to save
        file_path: Path to save JSON file
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def get_file_extensions(dir_path: str) -> Dict[str, int]:
    """
    Get counts of file extensions in a directory.
    
    Args:
        dir_path: Path to directory
        
    Returns:
        Dictionary mapping extensions to counts
    """
    ext_counts = {}
    
    for root, _, files in os.walk(dir_path):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext:
                ext = ext.lower()
                ext_counts[ext] = ext_counts.get(ext, 0) + 1
                
    return ext_counts


def detect_language(file_path: str) -> str:
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
        '.html': 'html',
        '.css': 'css',
        '.json': 'json',
        '.md': 'markdown',
        '.sql': 'sql',
    }
    return language_map.get(extension, 'unknown')


def count_tokens(text: str) -> int:
    """
    Estimate the number of tokens in a text.
    This is a simple approximation, not an exact count.
    
    Args:
        text: The input text
        
    Returns:
        Estimated token count
    """
    # Simple approximation: split on whitespace and punctuation
    return len(re.findall(r'\w+|[^\w\s]', text))


def is_binary_file(file_path: str) -> bool:
    """
    Check if a file is binary or text.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if the file is binary, False otherwise
    """
    try:
        with open(file_path, 'tr', encoding='utf-8') as f:
            f.read(1024)
        return False
    except UnicodeDecodeError:
        return True
