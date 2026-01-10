# config.py - Configuration settings

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class EmbeddingConfig:
    """Configuration for embedding model."""
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    batch_size: int = 32


@dataclass
class VectorDBConfig:
    """Configuration for vector database."""
    host: str = "localhost"
    port: int = 6333
    collection_name: str = "documents"
    vector_size: int = 384  # Default for all-MiniLM-L6-v2
    distance_metric: str = "Cosine"


@dataclass
class LLMConfig:
    """Configuration for language model."""
    model_name: str = "mistral:7b-instruct-q4_0"
    base_url: str = "http://localhost:11434"
    temperature: float = 0.7
    max_tokens: Optional[int] = None


@dataclass
class ChunkerConfig:
    """Configuration for token-based text chunking."""
    chunk_size: int = 500  # Maximum number of tokens per chunk
    chunk_overlap: int = 100  # Number of tokens to overlap between chunks
    encoding_name: str = "cl100k_base"  # Tokenizer encoding (cl100k_base for GPT-4, p50k_base for GPT-3)


@dataclass
class RetrievalConfig:
    """Configuration for retrieval."""
    top_k: int = 5
    similarity_threshold: float = 0.5


@dataclass
class RAGConfig:
    """Main RAG system configuration."""
    embedding: EmbeddingConfig = EmbeddingConfig()
    vectordb: VectorDBConfig = VectorDBConfig()
    llm: LLMConfig = LLMConfig()
    chunker: ChunkerConfig = ChunkerConfig()
    retrieval: RetrievalConfig = RetrievalConfig()
    
    # Data paths
    data_path: str = "data/processed"
    
    @classmethod
    def from_env(cls):
        """Load configuration from environment variables."""
        return cls(
            embedding=EmbeddingConfig(
                model_name=os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"),
                batch_size=int(os.getenv("EMBEDDING_BATCH_SIZE", "32"))
            ),
            vectordb=VectorDBConfig(
                host=os.getenv("QDRANT_HOST", "localhost"),
                port=int(os.getenv("QDRANT_PORT", "6333")),
                collection_name=os.getenv("COLLECTION_NAME", "documents"),
                vector_size=int(os.getenv("VECTOR_SIZE", "384"))
            ),
            llm=LLMConfig(
                model_name=os.getenv("LLM_MODEL", "mistral:7b-instruct-q4_0"),
                base_url=os.getenv("OLLAMA_URL", "http://localhost:11434"),
                temperature=float(os.getenv("LLM_TEMPERATURE", "0.7"))
            ),
            chunker=ChunkerConfig(
                chunk_size=int(os.getenv("CHUNK_SIZE", "500")),
                chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "100")),
                encoding_name=os.getenv("ENCODING_NAME", "cl100k_base")
            ),
            retrieval=RetrievalConfig(
                top_k=int(os.getenv("TOP_K", "5")),
                similarity_threshold=float(os.getenv("SIMILARITY_THRESHOLD", "0.5"))
            ),
            data_path=os.getenv("DATA_PATH", "data/processed")
        )
