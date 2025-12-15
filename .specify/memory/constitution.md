<!--
---
sync_impact_report:
  version_change: "2.0.0 → 2.1.0"
  modified_principles: []
  added_sections:
    - "X. RAG Chatbot"
  removed_sections: []
  updated_templates:
    - path: ".specify/templates/plan-template.md"
      status: "pending"
    - path: ".specify/templates/spec-template.md"
      status: "pending"
    - path: ".specify/templates/tasks-template.md"
      status: "pending"
  todos: []
---
-->
# Physical AI & Humanoid Robotics AI-Native Book Platform Constitution

## Core Principles

### I. Core Vision
To create a premium, mobile-first educational book focused on Physical AI, Embodied Intelligence, and Humanoid Robotics, providing a smooth, distraction-free reading experience.

### II. Core Philosophy
AI is to be represented as intelligence inside a physical body, grounded in real-world movement, perception, and interaction.

### III. UI Principles
The user interface will adhere to mobile-first layouts, utilizing glassmorphism with soft gradients. It will feature a sticky mobile bottom navigation, smooth chapter transitions, dark/light modes, large readable typography, and soft blur code backgrounds.

### IV. Technology Standards
The project will be built on a Docusaurus base, with Tailwind CSS for all styling. Book chapters will be MDX-driven, composed of reusable UI blocks, and located in `docs/`.

### V. Structure
The website will consist of only four pages: Home, Book, About, and Contact. The book itself will be composed of five chapters, with each chapter containing two topics.

### VI. Navigation
Navigation will be handled by a bottom sticky navbar on mobile devices and a sidebar for chapter navigation on desktop. The entire structure must be keyboard-accessible.

### VII. Performance
The application must ensure a fast initial load by lazy-loading chapters and minimizing the use of scripts.

### VIII. Accessibility
The platform must adhere to the highest accessibility standards, including semantic HTML, full screen reader support, visible focus indicators, and a reduced-motion mode.

### IX. Deployment
The project will be deployed as a static site on Vercel's free tier.

### X. RAG Chatbot
An integrated RAG (Retrieval-Augmented Generation) chatbot will be provided. It MUST adhere to the following rules:
-   **Zero Hallucination**: Answers MUST be generated *only* from the retrieved book content.
-   **Privacy**: The chatbot MUST be designed to protect user privacy.
-   **Embedding Model**: The chatbot MUST use Cohere embeddings. The use of OpenAI models is prohibited.
-   **Vector Store**: The chatbot MUST use Qdrant Cloud for all vector storage.

## Governance
All pull requests and code reviews must verify compliance with this constitution. Any deviation requires an explicit exemption documented in an Architectural Decision Record (ADR).

**Version**: 2.1.0 | **Ratified**: 2025-12-10 | **Last Amended**: 2025-12-14
