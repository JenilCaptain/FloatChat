# embedder.py - HuggingFace embeddings

from typing import List
import numpy as np

 
class HuggingFaceEmbedder:
    """Generates embeddings using HuggingFace models."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the embedder with a HuggingFace model.
        
        Args:
            model_name: Name of the HuggingFace model to use
        """
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the embedding model."""
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name)
            print(f"Loaded embedding model: {self.model_name}")
        except ImportError:
            print("sentence-transformers not installed. Run: pip install sentence-transformers")
        except Exception as e:
            print(f"Error loading model: {e}")
    
    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector as numpy array (normalized)
        """
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        return self.model.encode(text, normalize_embeddings=True)
    
    def embed_batch(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """
        Generate embeddings for a batch of texts.
        
        Args:
            texts: List of input texts
            batch_size: Batch size for encoding
            
        Returns:
            Array of embedding vectors (normalized)
        """
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        return self.model.encode(texts, batch_size=batch_size, show_progress_bar=True, normalize_embeddings=True)
