# qdrant_client.py - DB connection & indexing

from typing import List, Dict, Any
import numpy as np
import uuid


class QdrantClient:
    """Handles Qdrant vector database connection and indexing."""
    
    def __init__(self, host: str = "localhost", port: int = 6333, collection_name: str = "documents"):
        """
        Initialize Qdrant client.
        
        Args:
            host: Qdrant server host
            port: Qdrant server port
            collection_name: Name of the collection to use
        """
        self.host = host
        self.port = port
        self.collection_name = collection_name
        self.client = None
        self._connect()
    
    def _connect(self):
        """Establish connection to Qdrant."""
        try:
            from qdrant_client import QdrantClient as QC
            from qdrant_client.models import Distance, VectorParams
            
            self.client = QC(host=self.host, port=self.port)
            print(f"Connected to Qdrant at {self.host}:{self.port}")
        except ImportError:
            print("qdrant-client not installed. Run: pip install qdrant-client")
        except Exception as e:
            print(f"Error connecting to Qdrant: {e}")
    
    def create_collection(self, vector_size: int, distance: str = "Cosine"):
        """
        Create a new collection in Qdrant.
        
        Args:
            vector_size: Dimension of the vectors
            distance: Distance metric (Cosine, Euclidean, Dot)
        """
        from qdrant_client.models import Distance, VectorParams
        
        distance_map = {
            "Cosine": Distance.COSINE,
            "Euclidean": Distance.EUCLID,
            "Dot": Distance.DOT
        }
        
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=vector_size, distance=distance_map[distance])
        )
        print(f"Created collection: {self.collection_name}")
    
    def index_documents(self, documents: List[Dict[str, Any]], embeddings: np.ndarray):
        """
        Index documents with their embeddings.
        
        Args:
            documents: List of document dictionaries
            embeddings: Array of embedding vectors
        """
        from qdrant_client.models import PointStruct
        
        points = []
        for doc, embedding in zip(documents, embeddings):
            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding.tolist(),
                    payload=doc
                )
            )
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        print(f"Indexed {len(points)} documents")
    
    def search(self, query_vector: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar documents.
        
        Args:
            query_vector: Query embedding vector
            top_k: Number of results to return
            
        Returns:
            List of matching documents with scores
        """
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector.tolist(),
            limit=top_k
        )
        
        return [
            {
                "score": result.score,
                "document": result.payload
            }
            for result in results
        ]
