"""
Chunker implementation for splitting code into manageable chunks for processing.
"""
from typing import List, Dict, Any, Optional
import os
import json
import re


class Chunker:
    """
    Implements text splitting strategy for code repositories.
    Splits code into chunks based on structure, size, or semantic boundaries.
    """
    
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        """
        Initialize the chunker with configuration parameters.
        
        Args:
            chunk_size: Maximum size of a chunk in characters
            overlap: Number of characters to overlap between consecutive chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split a text into overlapping chunks.
        
        Args:
            text: The text to split into chunks
            
        Returns:
            List of text chunks
        """
        chunks = []
        if len(text) <= self.chunk_size:
            chunks.append(text)
        else:
            start = 0
            while start < len(text):
                end = start + self.chunk_size
                if end < len(text):
                    # Try to find a good break point (newline, period, etc.)
                    break_point = self._find_break_point(text, end)
                    chunk = text[start:break_point]
                    chunks.append(chunk)
                    start = break_point - self.overlap
                else:
                    chunk = text[start:]
                    chunks.append(chunk)
                    break
        
        return chunks
    
    def chunk_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Split a file into chunks for processing.
        
        Args:
            file_path: Path to the file to chunk
            
        Returns:
            List of dictionaries with chunk data and metadata
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Skip binary files or files with encoding issues
            return []
            
        chunks = self.chunk_text(content)
        
        result = []
        for i, chunk in enumerate(chunks):
            result.append({
                "id": f"{os.path.basename(file_path)}_chunk_{i}",
                "file_path": file_path,
                "content": chunk,
                "chunk_index": i,
                "total_chunks": len(chunks)
            })
            
        return result
    
    def chunk_directory(self, dir_path: str, output_dir: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Process all files in a directory into chunks.
        
        Args:
            dir_path: Path to the directory
            output_dir: Directory to save individual chunk files
            
        Returns:
            List of all chunks from all files
        """
        all_chunks = []
        
        for root, _, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_chunks = self.chunk_file(file_path)
                    all_chunks.extend(file_chunks)
                    
                    if output_dir and file_chunks:
                        os.makedirs(output_dir, exist_ok=True)
                        output_file = os.path.join(
                            output_dir, 
                            f"{os.path.basename(file_path)}.chunks.json"
                        )
                        with open(output_file, 'w', encoding='utf-8') as f:
                            json.dump(file_chunks, f, indent=2)
                            
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")
        
        return all_chunks
    
    def _find_break_point(self, text: str, position: int) -> int:
        """
        Find a good break point near the given position.
        Prefers breaking at paragraph or sentence boundaries.
        
        Args:
            text: The text to search in
            position: The approximate position to break at
            
        Returns:
            The actual position to break at
        """
        # Look for paragraph break
        paragraph_match = re.search(r'\n\s*\n', text[position-100:position+100])
        if paragraph_match:
            return position - 100 + paragraph_match.start()
            
        # Look for line break
        line_match = re.search(r'\n', text[position-50:position+50])
        if line_match:
            return position - 50 + line_match.start()
            
        # Look for sentence break
        sentence_match = re.search(r'[.!?]\s', text[position-30:position+30])
        if sentence_match:
            return position - 30 + sentence_match.start() + 1
            
        # If no good break point found, just break at the position
        return position
