---
id: 004
title: Update Constitution for RAG Chatbot
stage: constitution
date: 2025-12-14
surface: agent
model: gemini
feature: none
branch: main
user: unknown
command: /sp.constitution
labels: [constitution, rag, chatbot]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - .specify/templates/plan-template.md
 - .specify/templates/spec-template.md
 - .specify/templates/tasks-template.md
tests:
 - none
---

## Prompt

/sp.constitution Integrated RAG Chatbot for a deployed Docusaurus technical book with strict RAG rules: answers generated ONLY from retrieved book content with zero hallucination and privacy safety; use Cohere embeddings only (no OpenAI), vectors in Qdrant Clou

## Response snapshot

I have updated the constitution to version 2.1.0, adding a new principle for the RAG Chatbot. I also updated the plan, spec, and tasks templates to reflect this new principle.

## Outcome

- ✅ Impact: The project constitution has been updated to include guidelines for a new RAG chatbot feature. This ensures that the new feature will be developed in alignment with the project's principles.
- 🧪 Tests: none
- 📁 Files: 
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/spec-template.md
  - .specify/templates/tasks-template.md
- 🔁 Next prompts: none
- 🧠 Reflection: The user provided a clear and concise description of the new principles, which made it easy to update the constitution. The process of updating the dependent templates was also straightforward.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
