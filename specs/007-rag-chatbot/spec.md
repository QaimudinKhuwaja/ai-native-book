# Feature Specification: RAG Chatbot

**Feature Branch**: `007-rag-chatbot`
**Created**: 2025-12-14
**Status**: Draft

## User Scenarios & Testing

### User Story 1 - Ask a question about the book (Priority: P1)
As a reader, I want to ask a question in natural language and get a concise answer generated from the book's content, so that I can quickly find information without reading through the entire text.

**Why this priority**: This is the core functionality of the RAG chatbot.

**Independent Test**: Can be tested by asking a question and verifying that the answer is relevant, accurate, and sourced from the book.

**Acceptance Scenarios**:
1.  **Given** I am on the book's website, **When** I ask a question that is covered in the book, **Then** I should receive a relevant and accurate answer with a link to the source chapter/section.
2.  **Given** I am on the book's website, **When** I ask a question that is not covered in the book, **Then** I should receive a polite refusal to answer.
3.  **Given** I am on the book's website, **When** I ask a question, **Then** the answer should be generated solely from the content of `/docs`, `/about`, and `/contact`.

### User Story 2 - Ask a question about selected text (Priority: P2)
As a reader, I want to select a portion of the text and ask a question about it, so that I can get a more focused answer.

**Why this priority**: This provides a more contextual and powerful way to interact with the content.

**Independent Test**: Can be tested by selecting text, asking a question, and verifying that the answer is based only on the selected text.

**Acceptance Scenarios**:
1.  **Given** I have selected a piece of text, **When** I ask a question about the selected text, **Then** I should receive an answer that is only based on the content of the selected text.

## Requirements

### Functional Requirements

-   **FR-001**: The system MUST provide a chat interface embedded within the Docusaurus website.
-   **FR-002**: The system MUST generate answers to user queries using a Retrieval-Augmented Generation (RAG) model.
-   **FR-003**: The system MUST use Cohere for generating embeddings. The use of OpenAI is strictly prohibited.
-   **FR-004**: The system MUST use Qdrant Cloud (Free Tier) as the vector store.
-   **FR-005**: The system MUST use a FastAPI backend to handle chat requests.
-   **FR-006**: The system MUST use Neon Serverless Postgres for any required persistent storage.
-   **FR-007**: The system MUST only use content from `/docs`, `/about`, and `/contact` pages as the knowledge source.
-   **FR-008**: The system MUST implement semantic chunking for the ingested content.
-   **FR-009**: The system MUST provide traceable answers with links to the source document.
-   **FR-010**: The system MUST support both global (full-book) and selected-text search modes.
-   **FR-011**: The system MUST politely decline to answer questions that are out of scope.
-   **FR-012**: The backend API MUST be stateless.
-   **FR-013**: Secrets MUST be managed via environment variables.
-   **FR-014**: The system MUST be production-ready.
-   **FR-015**: Authentication is NOT required unless a specific need is identified.

### Key Entities

-   **Document Chunk**: A piece of text extracted from the source documents, along with its metadata.
-   **Metadata**: Information about a document chunk, including the source (e.g., chapter, section, route).

### Non-Functional Requirements (Constitution Alignment)

-   **NFR-001 (Core Vision)**: The feature must align with the vision of a premium, mobile-first educational book on Physical AI. The chatbot will enhance the educational experience.
-   **NFR-002 (Core Philosophy)**: The chatbot will represent AI as an embodied intelligence that is an expert on the book's content.
-   **NFR-003 (UI Principles)**: The chat UI must be designed with mobile-first principles and be consistent with the overall look and feel of the website.
-   **NFR-004 (Technology Standards)**: The feature will be built with FastAPI for the backend, and integrated into the Docusaurus/React frontend.
-   **NFR-005 (Structure)**: The feature will be an addition to the existing site structure, primarily as an embedded UI component.
-   **NFR-006 (Navigation)**: The chat UI should be easily accessible.
-   **NFR-007 (Performance)**: The chatbot should be responsive and provide answers with low latency.
-   **NFR-008 (Accessibility)**: The chat UI must be accessible.
-   **NFR-009 (Deployment)**: The FastAPI backend will be deployed as a containerized application, and the frontend will be part of the static site deployment.
-   **NFR-010 (RAG Chatbot)**: The feature must adhere to the RAG chatbot principles (zero hallucination, privacy, Cohere embeddings, Qdrant Cloud).

## Success Criteria

### Measurable Outcomes

-   **SC-001**: 95% of in-scope questions receive a relevant and accurate answer.
-   **SC-002**: 100% of out-of-scope questions are politely declined.
-   **SC-003**: The P95 latency for a chat response is less than 3 seconds.
-   **SC-004**: All answers provide a link to the source document.
