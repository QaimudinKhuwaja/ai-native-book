from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import Optional
import os

class QdrantConfig:
    """Configuration class for Qdrant vector database"""
    
    def __init__(self):
        # Get configuration from environment variables or use defaults
        self.host = os.getenv("QDRANT_HOST", "localhost")
        self.port = int(os.getenv("QDRANT_PORT", "6333"))
        self.https = os.getenv("QDRANT_HTTPS", "false").lower() == "true"
        self.api_key = os.getenv("QDRANT_API_KEY", None)
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "book_content")
        
    def get_client(self) -> QdrantClient:
        """Create and return a Qdrant client instance"""
        if self.api_key:
            return QdrantClient(
                url=self.host,
                port=self.port,
                https=self.https,
                api_key=self.api_key
            )
        else:
            return QdrantClient(
                host=self.host,
                port=self.port
            )

# Default configuration instance
default_config = QdrantConfig()

# Predefined collection configurations
COLLECTION_CONFIGS = {
    "book_content": {
        "vector_size": 1024,  # Cohere embeddings size
        "distance": models.Distance.COSINE,
        "hnsw_config": {
            "m": 16,
            "ef_construct": 100,
            "full_scan_threshold": 10000,
            "max_indexing_threads": 0,
            "quantization_config": None,
            "optimizers_config": {
                "deleted_threshold": 0.2,
                "vacuum_min_vector_number": 1000,
                "default_segment_number": 0,
                "max_segment_size": None,
                "memmap_threshold": None,
                "indexing_threshold": 20000,
                "flush_interval_sec": 10,
                "max_optimization_threads": 1,
            },
        },
        "optimizer_config": {
            "deleted_threshold": 0.2,
            "vacuum_min_vector_number": 1000,
            "default_segment_number": 2,
            "max_segment_size": 100000,
            "memmap_threshold": 50000,
            "indexing_threshold": 20000,
            "flush_interval_sec": 5,
            "max_optimization_threads": 1,
        },
        "wal_config": {
            "wal_capacity_mb": 32,
            "wal_segments_ahead": 0,
        }
    }
}

def create_collection_if_not_exists(
    client: QdrantClient, 
    collection_name: str, 
    config_name: str = "book_content"
) -> bool:
    """
    Create a collection with predefined configuration if it doesn't exist.
    
    Args:
        client: Qdrant client instance
        collection_name: Name of the collection to create
        config_name: Name of the configuration to use
    
    Returns:
        True if collection was created, False if it already existed
    """
    try:
        # Check if collection exists
        collections = client.get_collections()
        collection_exists = any(collection.name == collection_name for collection in collections.collections)
        
        if collection_exists:
            return False
        
        # Get configuration
        if config_name not in COLLECTION_CONFIGS:
            raise ValueError(f"Configuration '{config_name}' not found")
        
        config = COLLECTION_CONFIGS[config_name]
        
        # Create collection
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=config["vector_size"],
                distance=config["distance"]
            ),
            hnsw_config=config["hnsw_config"],
            optimizer_config=config["optimizer_config"],
            wal_config=config["wal_config"]
        )
        
        # Create payload indexes for common metadata fields
        client.create_payload_index(
            collection_name=collection_name,
            field_name="chapter_title",
            field_schema=models.PayloadSchemaType.KEYWORD
        )
        
        client.create_payload_index(
            collection_name=collection_name,
            field_name="section",
            field_schema=models.PayloadSchemaType.KEYWORD
        )
        
        client.create_payload_index(
            collection_name=collection_name,
            field_name="page_number",
            field_schema=models.PayloadSchemaType.INTEGER
        )
        
        print(f"Created collection '{collection_name}' with optimized configuration")
        return True
        
    except Exception as e:
        print(f"Error creating collection: {e}")
        raise