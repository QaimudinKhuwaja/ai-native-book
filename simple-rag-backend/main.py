from fastapi import FastAPI
from api.chat import router as chat_router, ChatRequest, ChatResponse, Source
from qdrant_client.http import models
from qdrant_client.models import Distance, VectorParams
import qdrant_client
import os
import logging
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Simplified RAG Service",
    description="FastAPI service for Retrieval-Augmented Generation with Qdrant vector database and Cohere embeddings",
    version="1.0.0"
)

# Configuration
VECTOR_SIZE = 1024  # Cohere embeddings size for embed-english-v3.0
DISTANCE_METRIC = Distance.COSINE

# Include the chat router
app.include_router(chat_router, prefix="/api/v1", tags=["chat"])


@app.on_event("startup")
async def startup_event():
    """Initialize the Qdrant collection if it doesn't exist"""
    try:
        # Initialize Qdrant client for startup
        QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
        QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
        QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)

        if QDRANT_API_KEY:
            qdrant_client_instance = qdrant_client.QdrantClient(
                host=QDRANT_HOST,
                port=QDRANT_PORT,
                api_key=QDRANT_API_KEY
            )
        else:
            qdrant_client_instance = qdrant_client.QdrantClient(
                host=QDRANT_HOST,
                port=QDRANT_PORT
            )

        COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "book_content")

        # Check if collection exists
        collections = qdrant_client_instance.get_collections()
        collection_exists = any(collection.name == COLLECTION_NAME for collection in collections.collections)

        if not collection_exists:
            # Create collection
            qdrant_client_instance.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=VECTOR_SIZE, distance=DISTANCE_METRIC),
            )

            # Create payload index for metadata
            try:
                qdrant_client_instance.create_payload_index(
                    collection_name=COLLECTION_NAME,
                    field_name="page_title",
                    field_schema=models.PayloadSchemaType.KEYWORD
                )
            except Exception as e:
                logger.warning(f"Could not create payload index: {e}")

            logger.info(f"Created collection '{COLLECTION_NAME}' with {VECTOR_SIZE}-dimensional vectors")
        else:
            logger.info(f"Collection '{COLLECTION_NAME}' already exists")

    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise


@app.get("/")
def read_root():
    """Root endpoint for health check"""
    return {"message": "Simplified RAG Service is running", "status": "healthy"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    try:
        # Initialize Qdrant client for health check
        QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
        QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
        QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)

        if QDRANT_API_KEY:
            qdrant_client_instance = qdrant_client.QdrantClient(
                host=QDRANT_HOST,
                port=QDRANT_PORT,
                api_key=QDRANT_API_KEY
            )
        else:
            qdrant_client_instance = qdrant_client.QdrantClient(
                host=QDRANT_HOST,
                port=QDRANT_PORT
            )

        COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "book_content")

        # Test connection to Qdrant
        collections = qdrant_client_instance.get_collections()
        collection_exists = any(collection.name == COLLECTION_NAME for collection in collections.collections)

        return {
            "status": "healthy",
            "service": "Simplified RAG Service",
            "qdrant_connection": True,
            "collection_exists": collection_exists,
            "collection_name": COLLECTION_NAME,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@app.get("/stats")
def get_stats():
    """Get collection statistics"""
    try:
        # Initialize Qdrant client for stats
        QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
        QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
        QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)

        if QDRANT_API_KEY:
            qdrant_client_instance = qdrant_client.QdrantClient(
                host=QDRANT_HOST,
                port=QDRANT_PORT,
                api_key=QDRANT_API_KEY
            )
        else:
            qdrant_client_instance = qdrant_client.QdrantClient(
                host=QDRANT_HOST,
                port=QDRANT_PORT
            )

        COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "book_content")

        collection_info = qdrant_client_instance.get_collection(COLLECTION_NAME)
        return {
            "collection_name": COLLECTION_NAME,
            "vector_size": collection_info.config.params.vectors.size,
            "distance_metric": str(collection_info.config.params.vectors.distance),
            "approximate_point_count": collection_info.approximate_vectors_count,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)