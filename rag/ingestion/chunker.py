# chunker.py - text splitting logic

from typing import List, Dict, Any
import tiktoken


class TextChunker:
    """Handles token-based text splitting for document chunking."""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100, encoding_name: str = "cl100k_base"):
        """
        Initialize the text chunker with token-based splitting.
        
        Args:
            chunk_size: Maximum number of tokens per chunk
            chunk_overlap: Number of tokens to overlap between chunks
            encoding_name: Tokenizer encoding to use (cl100k_base for GPT-4, p50k_base for GPT-3)
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoding_name = encoding_name
        self.tokenizer = None
        self._initialize_tokenizer()
    
    def _initialize_tokenizer(self):
        """Initialize the tiktoken tokenizer."""
        try:
            self.tokenizer = tiktoken.get_encoding(self.encoding_name)
        except Exception as e:
            print(f"Error loading tokenizer: {e}")
            print("Install tiktoken: pip install tiktoken")
            raise
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks based on tokens.
        
        Args:
            text: Input text to be chunked
            
        Returns:
            List of text chunks
        """
        if not self.tokenizer:
            raise RuntimeError("Tokenizer not initialized")
        
        # Encode text into tokens
        tokens = self.tokenizer.encode(text)
        chunks = []
        
        start = 0
        while start < len(tokens):
            # Get chunk of tokens
            end = start + self.chunk_size
            chunk_tokens = tokens[start:end]
            
            # Decode tokens back to text
            chunk_text = self.tokenizer.decode(chunk_tokens)
            chunks.append(chunk_text)
            
            # Move start position with overlap
            start += self.chunk_size - self.chunk_overlap
        
        return chunks
    
    def chunk_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Chunk multiple documents while preserving metadata.
        
        Args:
            documents: List of document dictionaries with 'text' and 'metadata' fields
            
        Returns:
            List of chunked documents with metadata
        """
        chunked_docs = []
        
        for doc in documents:
            text = doc.get('text', '')
            metadata = doc.get('metadata', {})
            
            chunks = self.chunk_text(text)
            
            for idx, chunk in enumerate(chunks):
                chunked_docs.append({
                    'text': chunk,
                    'metadata': {
                        **metadata,
                        'chunk_id': idx,
                        'total_chunks': len(chunks)
                    }
                })
        
        return chunked_docs
