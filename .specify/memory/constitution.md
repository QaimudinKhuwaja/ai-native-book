<!--
---
sync_impact_report:
  version_change: "none → 1.0.0"
  modified_principles: []
  added_sections:
    - "Core Principles"
    - "Technology Stack"
    - "Governance"
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
# AI-Native Driven Development – Premium Book Website Constitution

## Core Principles

### I. Zero External UI Libraries
Rely only on shadcn/ui and Tailwind CSS. No other component libraries are permitted. This ensures a consistent and lightweight frontend.

### II. Mobile-First, Modern Design
All UI must be responsive, starting with mobile screens. Implement glassmorphism and gradient effects for a modern, visually appealing aesthetic.

### III. MDX for All Book Content
All book chapters and content must be written in MDX. This allows for easy updates, component embedding, and keeps content separate from presentation. Chapter content must be located in `/content/chapters/`.

### IV. Dark/Light Mode
The entire application must support both dark and light themes, with a user-controlled toggle. This is a mandatory accessibility and user experience feature.

### V. Performance First
First Contentful Paint (FCP) must be under 1.5 seconds. Total bundle size (excluding images) must not exceed 150KB. Performance is a key feature, not an afterthought.

### VI. Accessibility as a Requirement
The application must be 100% accessible. This includes strict adherence to ARIA standards and ensuring full keyboard navigation support for all interactive elements.

### VII. Code Quality and Reusability
All components must be designed for reusability. TypeScript's strict mode must be enabled and enforced across the entire codebase to ensure type safety and code quality.

## Technology Stack
The project will exclusively use the following technologies:
- Next.js 15
- Tailwind CSS
- shadcn/ui
- MDX

## Governance
All pull requests and code reviews must verify compliance with this constitution. Any deviation requires an explicit exemption documented in an Architectural Decision Record (ADR).

**Version**: 1.0.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06