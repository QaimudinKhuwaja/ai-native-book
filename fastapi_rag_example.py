from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.models import Distance, VectorParams
import cohere
import uuid
import asyncio
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG Service with Qdrant and Cohere", 
              description="FastAPI service for Retrieval-Augmented Generation with Qdrant vector database and Cohere embeddings",
              version="1.0.0")

# Initialize clients
qdrant_client = QdrantClient(host="localhost", port=6333)
co = cohere.Client(api_key="YOUR_COHERE_API_KEY")  # Replace with your Cohere API key

# Configuration
COLLECTION_NAME = "book_content"
VECTOR_SIZE = 1024  # Cohere embeddings size
DISTANCE_METRIC = Distance.COSINE

# Pydantic models
class Document(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    metadata: Dict[str, Any] = Field(default={})
    chapter_title: Optional[str] = None
    section: Optional[str] = None
    page_number: Optional[int] = None

class DocumentBatch(BaseModel):
    documents: List[Document]

class QueryRequest(BaseModel):
    query: str
    top_k: int = Field(default=5, le=20)
    include_payload: bool = True
    min_score: float = Field(default=0.0, ge=0.0, le=1.0)

class QueryResponse(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    total_found: int
    execution_time: float

class HybridQueryRequest(BaseModel):
    query: str
    top_k: int = Field(default=5, le=20)
    semantic_weight: float = Field(default=0.7, ge=0.0, le=1.0)
    keyword_weight: float = Field(default=0.3, ge=0.0, le=1.0)

@app.on_event("startup")
async def startup_event():
    """Initialize the Qdrant collection if it doesn't exist"""
    try:
        collections = qdrant_client.get_collections()
        collection_exists = any(collection.name == COLLECTION_NAME for collection in collections.collections)
        
        if not collection_exists:
            qdrant_client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=VECTOR_SIZE, distance=DISTANCE_METRIC),
            )
            
            # Create payload index for metadata
            qdrant_client.create_payload_index(
                collection_name=COLLECTION_NAME,
                field_name="chapter_title",
                field_schema=models.PayloadSchemaType.KEYWORD
            )
            
            logger.info(f"Created collection '{COLLECTION_NAME}' with {VECTOR_SIZE}-dimensional vectors")
        else:
            logger.info(f"Collection '{COLLECTION_NAME}' already exists")
            
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise

@app.post("/documents/batch", 
          summary="Add multiple documents to the vector database",
          description="Upload multiple documents to be indexed in the Qdrant vector database")
async def add_documents_batch(batch: DocumentBatch):
    """Add a batch of documents to the vector database"""
    try:
        # Prepare points for insertion
        points = []
        for doc in batch.documents:
            # Generate embeddings using Cohere
            embeddings_response = co.embed(
                texts=[doc.content],
                model="embed-english-v3.0",
                input_type="search_document"
            )
            
            embedding = embeddings_response.embeddings[0]
            
            point = models.PointStruct(
                id=doc.id,
                vector=embedding,
                payload={
                    "content": doc.content,
                    "metadata": doc.metadata,
                    "chapter_title": doc.chapter_title,
                    "section": doc.section,
                    "page_number": doc.page_number,
                    "created_at": datetime.utcnow().isoformat()
                }
            )
            points.append(point)

        # Upload points to Qdrant
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        
        logger.info(f"Successfully added {len(points)} documents to collection")
        return {"message": f"Successfully added {len(points)} documents", "ids": [p.id for p in points]}
        
    except Exception as e:
        logger.error(f"Error adding documents: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add documents: {str(e)}")

@app.post("/documents/{doc_id}", 
          summary="Add a single document to the vector database",
          description="Upload a single document to be indexed in the Qdrant vector database")
async def add_document(doc_id: str, document: Document):
    """Add a single document to the vector database"""
    try:
        # Override ID with the one provided in the path
        document.id = doc_id
        
        # Generate embeddings using Cohere
        embeddings_response = co.embed(
            texts=[document.content],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        
        embedding = embeddings_response.embeddings[0]
        
        # Create and upload point to Qdrant
        point = models.PointStruct(
            id=document.id,
            vector=embedding,
            payload={
                "content": document.content,
                "metadata": document.metadata,
                "chapter_title": document.chapter_title,
                "section": document.section,
                "page_number": document.page_number,
                "created_at": datetime.utcnow().isoformat()
            }
        )
        
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=[point]
        )
        
        logger.info(f"Successfully added document {document.id}")
        return {"message": f"Successfully added document {document.id}"}
        
    except Exception as e:
        logger.error(f"Error adding document: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add document: {str(e)}")

@app.post("/query", 
          summary="Semantic search in the vector database",
          description="Perform semantic search using Cohere embeddings to find relevant content")
async def query_documents(request: QueryRequest):
    """Perform semantic search in the vector database"""
    try:
        import time
        start_time = time.time()
        
        # Generate embedding for the query using Cohere
        query_embeddings = co.embed(
            texts=[request.query],
            model="embed-english-v3.0",
            input_type="search_query"
        )
        
        query_embedding = query_embeddings.embeddings[0]
        
        # Perform similarity search in Qdrant
        search_result = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding,
            limit=request.top_k,
            with_payload=request.include_payload
        )
        
        # Filter results by minimum score if specified
        filtered_results = [
            hit for hit in search_result 
            if hit.score >= request.min_score
        ]
        
        execution_time = time.time() - start_time
        
        return QueryResponse(
            query=request.query,
            results=[
                {
                    "id": hit.id,
                    "score": hit.score,
                    "payload": hit.payload if request.include_payload else {},
                    "content": hit.payload.get("content") if request.include_payload else ""
                }
                for hit in filtered_results
            ],
            total_found=len(filtered_results),
            execution_time=execution_time
        )
        
    except Exception as e:
        logger.error(f"Error querying documents: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to query documents: {str(e)}")

@app.post("/hybrid-query", 
          summary="Hybrid search combining semantic and keyword search",
          description="Perform hybrid search combining vector similarity and keyword matching")
async def hybrid_query(request: HybridQueryRequest):
    """Perform hybrid search combining semantic and keyword search"""
    try:
        import time
        start_time = time.time()
        
        # Generate embedding for the semantic part using Cohere
        query_embeddings = co.embed(
            texts=[request.query],
            model="embed-english-v3.0",
            input_type="search_query"
        )
        
        query_embedding = query_embeddings.embeddings[0]
        
        # Perform hybrid search in Qdrant
        search_result = qdrant_client.query_points(
            collection_name=COLLECTION_NAME,
            prefetch=[
                models.Prefetch(
                    query=query_embedding,
                    using="text_vector",
                    limit=int(request.top_k * 2)  # Get more results for hybrid fusion
                )
            ],
            query=models.FusionQuery(
                fusion=models.Fusion.RRF  # Reciprocal Rank Fusion
            ),
            limit=request.top_k,
            with_payload=True
        )
        
        execution_time = time.time() - start_time
        
        return QueryResponse(
            query=request.query,
            results=[
                {
                    "id": hit.id,
                    "score": hit.score,
                    "payload": hit.payload,
                    "content": hit.payload.get("content", "")
                }
                for hit in search_result.points
            ],
            total_found=len(search_result.points),
            execution_time=execution_time
        )
        
    except Exception as e:
        logger.error(f"Error in hybrid query: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to perform hybrid query: {str(e)}")

@app.delete("/documents/{doc_id}",
            summary="Delete a document from the vector database",
            description="Remove a specific document from the Qdrant collection")
async def delete_document(doc_id: str):
    """Delete a document from the vector database"""
    try:
        # Delete the point from Qdrant
        qdrant_client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=models.PointIdsList(
                points=[doc_id]
            )
        )
        
        logger.info(f"Successfully deleted document {doc_id}")
        return {"message": f"Successfully deleted document {doc_id}"}
        
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")

@app.get("/health",
         summary="Service health check",
         description="Check if the RAG service is running properly")
async def health_check():
    """Health check endpoint"""
    try:
        # Test connection to Qdrant
        collections = qdrant_client.get_collections()
        collection_exists = any(collection.name == COLLECTION_NAME for collection in collections.collections)
        
        if not collection_exists:
            return {"status": "warning", "message": f"Collection {COLLECTION_NAME} not found"}
        
        return {
            "status": "healthy",
            "service": "RAG Service with Qdrant and Cohere",
            "collection_exists": collection_exists,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.get("/stats",
         summary="Get collection statistics",
         description="Retrieve information about the vector database collection")
async def get_stats():
    """Get statistics about the collection"""
    try:
        collection_info = qdrant_client.get_collection(COLLECTION_NAME)
        return {
            "collection_name": COLLECTION_NAME,
            "vector_size": collection_info.config.params.vectors.size,
            "distance_metric": collection_info.config.params.vectors.distance,
            "approximate_point_count": collection_info.approximate_vectors_count,
            "segments_count": len(collection_info.segments),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)