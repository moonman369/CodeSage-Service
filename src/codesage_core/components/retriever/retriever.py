"""
Retriever implementation for querying vector databases to find relevant code chunks.
"""
from typing import List, Dict, Any, Optional, Union
import os
import json
import pickle
import numpy as np


class Retriever:
    """
    Implements vector database querying to retrieve relevant code chunks.
    """
    
    def __init__(self, embeddings_path: Optional[str] = None):
        """
        Initialize the retriever with pre-computed embeddings.
        
        Args:
            embeddings_path: Path to the embeddings file
        """
        self.embeddings = {}
        
        if embeddings_path and os.path.exists(embeddings_path):
            self.load_embeddings(embeddings_path)
    
    def load_embeddings(self, embeddings_path: str):
        """
        Load embeddings from a file.
        
        Args:
            embeddings_path: Path to the embeddings file
        """
        ext = os.path.splitext(embeddings_path)[1].lower()
        
        if ext == '.pkl':
            with open(embeddings_path, 'rb') as f:
                self.embeddings = pickle.load(f)
        elif ext == '.json':
            with open(embeddings_path, 'r', encoding='utf-8') as f:
                self.embeddings = json.load(f)
        else:
            raise ValueError(f"Unsupported embeddings format: {ext}")
    
    def query(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Find the most relevant chunks for a query.
        
        Args:
            query_text: The query text
            top_k: Number of results to return
            
        Returns:
            List of relevant chunks with similarity scores
        """
        # In a real implementation, this would:
        # 1. Embed the query text
        # 2. Compute similarity with all chunk embeddings
        # 3. Return the top_k most similar chunks
        
        # For this stub, we'll return random chunks
        import random
        
        if not self.embeddings:
            return []
        
        chunk_ids = list(self.embeddings.keys())
        selected_ids = random.sample(chunk_ids, min(top_k, len(chunk_ids)))
        
        results = []
        for chunk_id in selected_ids:
            metadata = self.embeddings[chunk_id].get('metadata', {})
            results.append({
                'id': chunk_id,
                'content': metadata.get('content', ''),
                'file_path': metadata.get('file_path', ''),
                'similarity': random.random(),  # Placeholder similarity score
                'metadata': metadata
            })
        
        # Sort by similarity (highest first)
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results
    
    def batch_query(self, queries: List[str], top_k: int = 5) -> List[List[Dict[str, Any]]]:
        """
        Run multiple queries at once.
        
        Args:
            queries: List of query texts
            top_k: Number of results to return per query
            
        Returns:
            List of result lists, one per query
        """
        return [self.query(query, top_k) for query in queries]
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Compute cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity value
        """
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0
            
        return dot_product / (norm1 * norm2)
