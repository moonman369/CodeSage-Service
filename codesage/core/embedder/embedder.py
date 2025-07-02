"""
Embedder implementation for creating and storing vector embeddings of code chunks.
"""
from typing import List, Dict, Any, Optional, Union
import os
import json
import pickle
import numpy as np


class Embedder:
    """
    Creates and stores vector embeddings for code chunks.
    Supports multiple embedding models and storage backends.
    """
    
    def __init__(self, model_name: str = "default", dimension: int = 1536):
        """
        Initialize the embedder with the specified model.
        
        Args:
            model_name: Name of the embedding model to use
            dimension: Dimension of the embedding vectors
        """
        self.model_name = model_name
        self.dimension = dimension
        self.embeddings = {}
        
        # Placeholder for actual model loading
        # In a real implementation, this would load the appropriate embedding model
        print(f"Initializing embedder with model: {model_name}")
        
    def embed_text(self, text: str) -> List[float]:
        """
        Create an embedding vector for a text string.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as a list of floats
        """
        # This is a placeholder for the actual embedding logic
        # In a real implementation, this would call the embedding model
        
        # For demo purposes, create a simple deterministic vector
        # based on the text content
        import hashlib
        
        # Create a hash of the text
        text_hash = hashlib.md5(text.encode()).hexdigest()
        
        # Convert the hash to a numeric seed
        seed = int(text_hash, 16) % (2**32)
        
        # Use the seed to generate a deterministic random vector
        np.random.seed(seed)
        vector = np.random.normal(0, 0.1, self.dimension).tolist()
        
        return vector
        
    def embed_chunks(self, chunks: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Create embeddings for a list of chunks.
        
        Args:
            chunks: List of chunk dictionaries with at least 'id' and 'content' keys
            
        Returns:
            Dictionary mapping chunk IDs to embedding data
        """
        result = {}
        
        for chunk in chunks:
            chunk_id = chunk['id']
            content = chunk['content']
            
            embedding = self.embed_text(content)
            
            result[chunk_id] = {
                'embedding': embedding,
                'metadata': {k: v for k, v in chunk.items() if k != 'content'}
            }
            
            # Store the full content in metadata if needed later
            result[chunk_id]['metadata']['content'] = content
            
        return result
    
    def save_embeddings(self, embeddings: Dict[str, Any], output_path: str):
        """
        Save embeddings to a file.
        
        Args:
            embeddings: Dictionary of embeddings to save
            output_path: Path to save the embeddings to
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Determine the format based on the file extension
        ext = os.path.splitext(output_path)[1].lower()
        
        if ext == '.pkl':
            with open(output_path, 'wb') as f:
                pickle.dump(embeddings, f)
        elif ext == '.json':
            # Convert numpy arrays to lists for JSON serialization
            serializable_embeddings = {}
            for key, value in embeddings.items():
                if isinstance(value.get('embedding'), np.ndarray):
                    value['embedding'] = value['embedding'].tolist()
                serializable_embeddings[key] = value
                
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(serializable_embeddings, f, indent=2)
        else:
            raise ValueError(f"Unsupported output format: {ext}")
            
    def load_embeddings(self, input_path: str) -> Dict[str, Any]:
        """
        Load embeddings from a file.
        
        Args:
            input_path: Path to load embeddings from
            
        Returns:
            Dictionary of loaded embeddings
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Embedding file not found: {input_path}")
            
        ext = os.path.splitext(input_path)[1].lower()
        
        if ext == '.pkl':
            with open(input_path, 'rb') as f:
                return pickle.load(f)
        elif ext == '.json':
            with open(input_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            raise ValueError(f"Unsupported input format: {ext}")
