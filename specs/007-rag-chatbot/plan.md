# Implementation Plan: RAG Chatbot

**Branch**: `007-rag-chatbot` | **Date**: 2025-12-14 | **Spec**: [specs/007-rag-chatbot/spec.md](spec.md)

## Summary
This plan outlines the technical approach for building and integrating a Retrieval-Augmented Generation (RAG) chatbot into the Docusaurus technical book website. The chatbot will provide answers to user questions based on the book's content, with a strong emphasis on accuracy, traceability, and privacy.

## Technical Context

**Language/Version**:
-   Backend: Python 3.11+ (FastAPI)
-   Frontend: TypeScript (React/Docusaurus)

**Primary Dependencies**:
-   **Backend**:
    -   `fastapi`: For building the REST API.
    -   `uvicorn`: As the ASGI server.
    -   `cohere`: The Cohere Python SDK for embeddings and generation.
    -   `qdrant-client`: The Qdrant Python client.
    -   `beautifulsoup4`: For web scraping the Docusaurus site.
    -   `langchain`: For semantic chunking and document processing.
    -   `psycopg2-binary`: For connecting to Neon Serverless Postgres.
    -   `sqlalchemy`: As the ORM for interacting with the database.
-   **Frontend**:
    -   Docusaurus 3, React 19, Tailwind CSS.

**Storage**:
-   **Vector Store**: Qdrant Cloud (Free Tier).
-   **Database**: Neon Serverless Postgres (for chat history, optional).

**Testing**:
-   Backend: `pytest`.
-   Frontend: Jest / React Testing Library.

**Target Platform**: Modern Web Browsers.

**Project Type**:
-   Backend: Containerized FastAPI application.
-   Frontend: Static Site Generator (Docusaurus) with a custom React component.

**Performance Goals**:
-   P95 latency for chat responses < 3 seconds.

**Constraints**:
-   Answers must be generated *only* from the book content.
-   Strictly use Cohere for embeddings.
-   Stateless backend API.
-   Secrets managed via environment variables.

## Constitution Check

- [X] **Core Vision**: Aligns with the vision of a premium educational book by enhancing the learning experience.
- [X] **Core Philosophy**: Represents AI as an embodied intelligence expert on the book.
- [X] **UI Principles**: The UI will be designed to be consistent with the existing site.
- [X] **Technology Standards**: Uses approved technologies (FastAPI, React).
- [X] **Structure**: Adds a new component to the existing structure.
- [X] **Navigation**: The chat UI will be easily accessible.
- [X] **Performance**: Aims for low-latency responses.
- [X] **Accessibility**: The chat UI will be accessible.
- [X] **Deployment**: The backend will be containerized, and the frontend integrated into the static site.
- [X] **RAG Chatbot**: Adheres to all RAG chatbot principles.

## Project Structure

### Documentation (this feature)

```text
specs/007-rag-chatbot/
├── plan.md              # This file
├── spec.md              # The feature specification
└── tasks.md             # The implementation tasks
```

### Source Code (repository root)

```text
# Backend (new directory)
rag-chatbot-backend/
├── app/
│   ├── main.py          # FastAPI application
│   ├── api/             # API endpoints
│   ├── services/        # Business logic
│   ├── models/          # Pydantic models
│   └── core/            # Configuration and settings
├── data_ingestion/
│   ├── ingest.py        # Data ingestion script
│   └── chunking.py      # Semantic chunking logic
├── tests/
│   ├── ...
├── Dockerfile
└── requirements.txt

# Frontend (modifications to existing structure)
src/
├── components/
│   └── custom/
│       └── RAGChatbot/
│           ├── index.tsx        # The main chatbot component
│           └── ChatUI.tsx       # The chat interface
└── ...
```

**Structure Decision**: A new directory will be created for the FastAPI backend to keep it separate from the Docusaurus frontend. The frontend will be integrated as a new custom React component.

## Complexity Tracking
N/A - The plan is aligned with the constitution.
