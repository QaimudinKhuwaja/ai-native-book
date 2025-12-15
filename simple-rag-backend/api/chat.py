from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import os
import cohere
import qdrant_client
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


class ChatRequest(BaseModel):
    query: str
    top_k: int = 5
    min_score: float = 0.0


class Source(BaseModel):
    url: str
    page_title: str
    chunk_index: int
    content: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]
    query: str
    retrieved_chunks: int


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Chat endpoint that retrieves context from Qdrant and generates response"""
    try:
        # Initialize clients
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

        cohere_client = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))
        COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "book_content")

        # Generate embedding for the query using Cohere
        query_embeddings = cohere_client.embed(
            texts=[request.query],
            model="embed-english-v3.0",
            input_type="search_query"
        )
        query_embedding = query_embeddings.embeddings[0]

        # Perform similarity search in Qdrant
        search_result = qdrant_client_instance.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding,
            limit=request.top_k,
            with_payload=True
        )

        # Filter results by minimum score if specified
        filtered_results = [
            hit for hit in search_result
            if hit.score >= request.min_score
        ]

        if not filtered_results:
            # If no content is found, return "I don't know"
            return ChatResponse(
                answer="I don't know. The requested information is not available in the book content.",
                sources=[],
                query=request.query,
                retrieved_chunks=0
            )

        # Build context from retrieved chunks
        retrieved_texts = []
        sources_list = []

        for hit in filtered_results:
            payload = hit.payload
            retrieved_texts.append(payload.get("content", ""))

            # Create source objects
            source = Source(
                url=payload.get("url", ""),
                page_title=payload.get("page_title", ""),
                chunk_index=payload.get("chunk_index", 0),
                content=payload.get("content", "")
            )
            sources_list.append(source)

        # Join the retrieved texts to form the context
        context = "\n\n".join(retrieved_texts)

        # Create a strict RAG prompt that forces the agent to only use provided context
        system_prompt = """You are an AI assistant that strictly answers questions based only on the provided context from the book.
        If the information is not available in the provided context, respond with 'I don't know'.
        Do not make up information or use general knowledge. Only answer based on the specific context provided."""

        user_prompt = f"""
        Context:
        {context}

        Question: {request.query}

        Answer: """

        # Use Cohere to generate response based on retrieved context
        response = cohere_client.generate(
            prompt=f"{system_prompt}\n\n{user_prompt}",
            model="command-r-plus",  # Using Cohere Command-R Plus model for better accuracy
            temperature=0.3,
            max_tokens=500
        )

        answer = response.generations[0].text.strip()

        return ChatResponse(
            answer=answer,
            sources=sources_list,
            query=request.query,
            retrieved_chunks=len(filtered_results)
        )

    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process chat request: {str(e)}")