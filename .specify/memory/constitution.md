<!--
---
sync_impact_report:
  version_change: "1.0.0 → 1.0.1"
  modified_principles:
    - old: "I. Zero External UI Libraries"
      new: "I. Zero External UI Libraries Except Tailwind"
    - old: "III. MDX for All Book Content"
      new: "III. MDX for All Book Content (with structure details)"
    - old: "VII. Code Quality and Reusability"
      new: "VII. TypeScript Strict Mode & Reusable Components"
  added_sections:
    - "Constraints"
  removed_sections:
    - "Technology Stack (Previous: Next.js 15, shadcn/ui)"
  updated_templates:
    - path: ".specify/templates/plan-template.md"
      status: "updated"
    - path: ".specify/templates/spec-template.md"
      status: "updated"
    - path: ".specify/templates/tasks-template.md"
      status: "updated"
  todos: []
---
-->
# AI-Native Driven Development – Premium Book Website (Docusaurus 3 + Tailwind + MDX) Constitution

## Core Principles

### I. Zero External UI Libraries Except Tailwind
Rely only on Tailwind CSS for styling. No other component libraries or UI frameworks are permitted. This ensures a consistent and lightweight frontend.

### II. Mobile-First, Glassmorphism + Gradient Design
All UI must be responsive, starting with mobile screens. Implement glassmorphism and gradient effects for a modern, visually appealing aesthetic.

### III. MDX for All Book Content
All book chapters and content must be written in MDX to allow for easy updates and component embedding. The book must have exactly 5 chapters, each with 2 topics. Chapter content must be located in `/content/chapters/`.

### IV. Dark/Light Mode Toggle
The entire application must support both dark and light themes, with a user-toggle. This is a mandatory accessibility and user experience feature.

### V. Lightning Fast Performance
First Contentful Paint (FCP) must be under 1.5 seconds. Total bundle size (excluding images) must not exceed 150KB. Performance is a key feature, not an afterthought.

### VI. 100% Accessible (ARIA + Keyboard Nav)
Strict adherence to ARIA standards and ensure full keyboard navigation.

### VII. TypeScript Strict Mode & Reusable Components
TypeScript's strict mode must be enabled and enforced. All components must be designed for reusability.

## Technology Stack
The project will exclusively use the following technologies:
- Docusaurus 3
- Tailwind CSS
- MDX

## Constraints
The website must contain exactly 4 pages: Home, Book, About, and Contact. The book content must be structured into 5 chapters, each containing 2 topics. Deployment must target Vercel (free tier).

## Governance
All pull requests and code reviews must verify compliance with this constitution. Any deviation requires an explicit exemption documented in an Architectural Decision Record (ADR).

**Version**: 1.0.1 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06