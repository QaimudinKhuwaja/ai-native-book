# Simplified RAG Backend

A clean, minimal RAG (Retrieval-Augmented Generation) backend using FastAPI, Cohere, and Qdrant.

## Features

- FastAPI-based REST API with automatic Swagger documentation
- Cohere embeddings using `embed-english-v3.0` model
- Qdrant vector database for efficient similarity search
- Custom text chunking function (no LangChain dependency)
- Strict RAG implementation - answers only from retrieved context
- Returns "I don't know" when information is not available in context

## Requirements

- Python 3.8+
- Qdrant vector database (can run locally or remotely)
- Cohere API key

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the environment file and add your API keys:
   ```bash
   cp .env.example .env
   # Edit .env and add your Cohere API key
   ```

## Running Qdrant

To run Qdrant locally using Docker:
```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

## Ingesting Data

To populate the vector database with content from a sitemap:
```bash
python ingest.py
```

This will:
- Scrape all pages from the sitemap URL
- Chunk the content using the custom chunking function
- Generate embeddings using Cohere
- Store the vectors in Qdrant

## Running the API Server

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The API will be available at:
- http://localhost:8000
- Swagger UI at http://localhost:8000/docs

## API Endpoints

- `POST /api/v1/chat` - Main chat endpoint with RAG
- `GET /` - Health check
- `GET /health` - Detailed health check
- `GET /stats` - Collection statistics

## Environment Variables

- `QDRANT_HOST` - Qdrant host (default: localhost)
- `QDRANT_PORT` - Qdrant port (default: 6333)
- `QDRANT_API_KEY` - Qdrant API key (optional)
- `QDRANT_COLLECTION_NAME` - Collection name (default: book_content)
- `COHERE_API_KEY` - Cohere API key (required)

## Architecture

This is a simplified backend that strictly follows RAG principles:
1. User query comes in
2. Query is embedded using Cohere
3. Vector search is performed in Qdrant
4. Top-k relevant chunks are retrieved
5. Context is built from retrieved chunks
6. LLM (via Cohere) generates response based only on provided context
7. Response is returned with source information