# config.py - Configuration settings

import os
from dataclasses import dataclass, field
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
    collection_name: str = "FloatChat-Data_embeddings"
    vector_size: int = 384  # Default for all-MiniLM-L6-v2
    distance_metric: str = "Cosine"


@dataclass
class LLMConfig:
    """Configuration for language model."""
    model_name: str = "phi3"  # Ollama auto-detects GPU
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
    embedding: EmbeddingConfig = field(default_factory=EmbeddingConfig)
    vectordb: VectorDBConfig = field(default_factory=VectorDBConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)
    chunker: ChunkerConfig = field(default_factory=ChunkerConfig)
    retrieval: RetrievalConfig = field(default_factory=RetrievalConfig)
    
    # Data paths
    data_path: str = "data"  # Path to Parquet files (argo_profiles_master.parquet, argo_profiles_reduced.parquet)
    logs_path: str = "logs"  # Path to store RAG pipeline logs
    vectordb_path: str = "vectordb"  # Path to Qdrant database (for in-memory or persistent storage)
    
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
                model_name=os.getenv("LLM_MODEL", "phi3"),
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
            data_path=os.getenv("DATA_PATH", "data"),
            logs_path=os.getenv("LOGS_PATH", "logs"),
            vectordb_path=os.getenv("VECTORDB_PATH", "vectordb")
        )
