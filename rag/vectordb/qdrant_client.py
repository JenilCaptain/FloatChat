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
    
    def collection_exists(self) -> bool:
        """
        Check if collection exists in Qdrant.
        
        Returns:
            True if collection exists, False otherwise
        """
        try:
            collections = self.client.get_collections().collections
            return any(col.name == self.collection_name for col in collections)
        except Exception as e:
            print(f"Error checking collection: {e}")
            return False
    
    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the collection.
        
        Returns:
            Dictionary with collection stats
        """
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                'vectors_count': info.vectors_count,
                'points_count': info.points_count,
                'status': info.status
            }
        except Exception as e:
            print(f"Error getting collection info: {e}")
            return {}
    
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
    
    def index_documents(self, documents: List[Dict[str, Any]], embeddings: np.ndarray, batch_size: int = 100):
        """
        Index documents with their embeddings in batches.
        
        Args:
            documents: List of document dictionaries
            embeddings: Array of embedding vectors
            batch_size: Number of documents to upload per batch (default: 100)
        """
        from qdrant_client.models import PointStruct
        
        total_docs = len(documents)
        print(f"Indexing {total_docs} documents in batches of {batch_size}...")
        
        for i in range(0, total_docs, batch_size):
            batch_docs = documents[i:i + batch_size]
            batch_embeddings = embeddings[i:i + batch_size]
            
            points = []
            for doc, embedding in zip(batch_docs, batch_embeddings):
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
            print(f"  ✓ Indexed batch {i//batch_size + 1}/{(total_docs + batch_size - 1)//batch_size} ({len(points)} documents)")
        
        print(f"✓ Total indexed: {total_docs} documents")
    
    def search(self, query_vector: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar documents.
        
        Args:
            query_vector: Query embedding vector
            top_k: Number of results to return
            
        Returns:
            List of matching documents with scores
        """
        from qdrant_client.models import PointStruct
        
        # For qdrant-client v1.16.x, use query_points method
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector.tolist(),
            limit=top_k
        )
        
        return [
            {
                "score": point.score,
                "document": point.payload
            }
            for point in results.points
        ]
