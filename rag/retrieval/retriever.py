# retriever.py - similarity search

from typing import List, Dict, Any
import numpy as np


class Retriever:
    """Handles similarity search and document retrieval."""
    
    def __init__(self, vector_db, embedder):
        """
        Initialize the retriever.
        
        Args:
            vector_db: Vector database client (e.g., QdrantClient)
            embedder: Embedding model (e.g., HuggingFaceEmbedder)
        """
        self.vector_db = vector_db
        self.embedder = embedder
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: Search query text
            top_k: Number of documents to retrieve
            
        Returns:
            List of relevant documents with similarity scores
        """
        # Generate query embedding
        query_embedding = self.embedder.embed_text(query)
        
        # Search in vector database
        results = self.vector_db.search(query_embedding, top_k=top_k)
        
        return results
    
    def retrieve_with_threshold(self, query: str, top_k: int = 5, threshold: float = 0.5) -> List[Dict[str, Any]]:
        """
        Retrieve documents above a similarity threshold.
        
        Args:
            query: Search query text
            top_k: Maximum number of documents to retrieve
            threshold: Minimum similarity score threshold
            
        Returns:
            List of relevant documents with scores above threshold
        """
        results = self.retrieve(query, top_k=top_k)
        
        # Filter by threshold
        filtered_results = [
            result for result in results 
            if result['score'] >= threshold
        ]
        
        return filtered_results
    
    def format_context(self, results: List[Dict[str, Any]]) -> str:
        """
        Format retrieved documents into a context string.
        
        Args:
            results: List of retrieved documents
            
        Returns:
            Formatted context string
        """
        context_parts = []
        
        for idx, result in enumerate(results, 1):
            doc = result['document']
            score = result['score']
            text = doc.get('text', '')
            
            context_parts.append(f"[Document {idx}] (Score: {score:.3f})\n{text}")
        
        return "\n\n".join(context_parts)
