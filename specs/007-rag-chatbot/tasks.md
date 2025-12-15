# Tasks: RAG Chatbot

**Input**: Design documents from `specs/007-rag-chatbot/`

## Path Conventions
-   Backend: `rag-chatbot-backend/`
-   Frontend: `src/`

## Phase 1: Setup

-   [X] T001 [P] Create the `rag-chatbot-backend` directory and initialize a Python project with a virtual environment.
-   [X] T002 [P] Create the basic FastAPI application structure in `rag-chatbot-backend/app`.
-   [X] T003 [P] Add backend dependencies (`fastapi`, `uvicorn`, `cohere`, `qdrant-client`, `beautifulsoup4`, `langchain`, `psycopg2-binary`, `sqlalchemy`) to `rag-chatbot-backend/requirements.txt`.
-   [X] T004 [P] Create the `src/components/custom/RAGChatbot` directory for the frontend component.
-   [ ] T005 [P] Set up accounts for Qdrant Cloud and Neon Serverless Postgres. (User's responsibility)
-   [X] T006 [P] Configure environment variables for Cohere API key, Qdrant Cloud URL and API key, and Neon database URL.

## Phase 2: Data Ingestion

-   [X] T007 Create a web scraping script in `rag-chatbot-backend/data_ingestion/ingest.py` to crawl the `/docs`, `/about`, and `/contact` pages of the Docusaurus site.
-   [X] T008 Implement semantic chunking logic in `rag-chatbot-backend/data_ingestion/chunking.py` using LangChain.
-   [X] T009 In `ingest.py`, use the Cohere API to generate embeddings for the document chunks.
-   [X] T010 In `ingest.py`, store the embeddings and metadata (chapter, section, route) in Qdrant Cloud.
-   [X] T011 Create a command-line interface to run the ingestion script.

## Phase 3: Backend (FastAPI)

-   [X] T012 [P] Implement Pydantic models in `rag-chatbot-backend/app/models/` for chat requests and responses.
-   [X] T013 Create a service in `rag-chatbot-backend/app/services/` to connect to Qdrant Cloud.
-   [X] T014 Implement the chat API endpoint in `rag-chatbot-backend/app/api/chat.py`. This endpoint will:
    -   Generate an embedding for the user's query.
    -   Perform a similarity search in Qdrant.
    -   Generate an answer using the Cohere generation model.
    -   Return the answer and the sources.
-   [ ] T015 [P] If chat history is desired, implement a service to connect to Neon Serverless Postgres and store chat messages.
-   [X] T016 [P] Add comprehensive unit tests for the backend using `pytest`.
-   [X] T017 [P] Create a `Dockerfile` for the backend application.

## Phase 4: Frontend (Docusaurus/React)

-   [X] T018 [US1] Create the chat UI component in `src/components/custom/RAGChatbot/ChatUI.tsx`.
-   [X] T019 [US1] In `src/components/custom/RAGChatbot/index.tsx`, implement the logic to:
    -   Handle user input.
    -   Call the backend chat API.
    -   Display the response and sources.
-   [X] T020 [US1] Integrate the `RAGChatbot` component into the Docusaurus layout.
-   [X] T021 [US2] Implement the "selected-text-only" mode.

## Phase 5: Polish & Cross-Cutting Concerns

-   [ ] T022 [P] **Core Vision Alignment**: Review the implemented chatbot to ensure it aligns with the project's core vision.
-   [ ] T023 [P] **Core Philosophy Alignment**: Ensure the chatbot's persona is that of an expert on the book.
-   [ ] T024 [P] **UI Principles Audit**: Test the chat UI for mobile-first responsiveness and consistency with the site's design.
-   [ ] T025 [P] **Technology Standards Audit**: Verify that the implementation adheres to the technology standards (FastAPI, React).
-   [ ] T026 [P] **Structure Audit**: Verify the project structure is clean and well-organized.
-   [ ] T027 [P] **Navigation Audit**: Ensure the chat UI is easily accessible.
-   [ ] T028 [P] **Performance Audit**: Test the chatbot's responsiveness and latency.
-   [ ] T029 [P] **Accessibility Audit**: Test the chat UI for accessibility.
-   [ ] T030 [P] **Deployment Audit**: Deploy the backend and frontend to a staging environment for end-to-end testing.
-   [ ] T031 [P] **RAG Chatbot Audit**: Verify that the chatbot adheres to all RAG principles (zero hallucination, privacy, etc.).