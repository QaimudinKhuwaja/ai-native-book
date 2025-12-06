# Tasks: AI-Native Book Website

**Input**: Design documents from `specs/001-ai-native-book-website/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions
Assuming a Next.js App Router structure:

## Phase 1: Setup (Project Initialization, Tailwind, shadcn)

**Purpose**: Initialize the Next.js project and configure core styling/UI libraries.

- [ ] T001 Initialize Next.js 15 project with TypeScript and App Router in `/`
- [ ] T002 Install and configure Tailwind CSS in `tailwind.config.ts`, `postcss.config.js`, `app/globals.css`
- [ ] T003 Install and configure shadcn/ui. Run `npx shadcn-ui@latest init` and select appropriate settings.
- [ ] T004 Add initial components using shadcn/ui. Run `npx shadcn-ui@latest add button` in `components/ui/button.tsx`

## Phase 2: Foundational (Layout, Navigation, Theme Provider)

**Purpose**: Establish global layout, navigation, and theme toggling functionality.

- [ ] T005 Create a basic `app/layout.tsx` for the root layout.
- [ ] T006 Create `app/components/layout/theme-provider.tsx` component for Dark/Light mode toggle (NFR-003, US5).
- [ ] T007 Implement global `app/components/layout/header.tsx` with navigation links (Home, Book, About, Contact).
- [ ] T008 Implement global `app/components/layout/footer.tsx` component.
- [ ] T009 Integrate ThemeProvider into `app/layout.tsx`.

## Phase 3: User Story 1 - View Home Page (Priority: P1) 🎯 MVP

**Goal**: Display a compelling home page with a hero section, book preview, and CTA.

**Independent Test**: Verify the home page renders correctly with mock data.

### Implementation for User Story 1

- [ ] T010 [US1] Create `app/(pages)/(home)/page.tsx` for the Home page.
- [ ] T011 [P] [US1] Design and implement Hero section component in `app/components/home/hero-section.tsx`.
- [ ] T012 [P] [US1] Design and implement Book Preview component (e.g., featuring chapter cards) in `app/components/home/book-preview.tsx`.
- [ ] T013 [US1] Integrate Hero and Book Preview components into `app/(pages)/(home)/page.tsx`.
- [ ] T014 [US1] Add a clear Call-to-Action (CTA) to the Home page, linking to the Book page.

## Phase 4: User Story 2 - Read the Book (Priority: P1)

**Goal**: Enable seamless reading of the book with navigation and progress tracking.

**Independent Test**: Verify book content loads, scrolls smoothly, and progress bar/TOC function.

### Implementation for User Story 2

- [ ] T015 [US2] Create `app/(pages)/book/page.tsx` for the Book page.
- [ ] T016 [P] [US2] Create `lib/mdx.ts` to handle MDX parsing and data extraction.
- [ ] T017 [P] [US2] Create placeholder MDX files for 5 chapters, each with 2 topics in `content/chapters/`. Example: `content/chapters/01-introduction.mdx`.
- [ ] T018 [US2] Implement MDX content loading and rendering on `app/(pages)/book/page.tsx`.
- [ ] T019 [P] [US2] Create `app/components/book/chapter-navigation.tsx` component for table of contents.
- [ ] T020 [P] [US2] Create `app/components/book/progress-bar.tsx` component.
- [ ] T021 [US2] Integrate chapter navigation and progress bar into `app/(pages)/book/page.tsx`.
- [ ] T022 [US2] Implement smooth scrolling functionality and synchronize with chapter navigation/progress bar.

## Phase 5: User Story 3 - Learn About the Author (Priority: P2)

**Goal**: Provide an "About" page with author information.

**Independent Test**: Verify the "About" page displays author bio and vision.

### Implementation for User Story 3

- [ ] T023 [US3] Create `app/(pages)/about/page.tsx` for the About page.
- [ ] T024 [US3] Add author's biography and vision content to `app/(pages)/about/page.tsx`.

## Phase 6: User Story 4 - Join the Waitlist (Priority: P2)

**Goal**: Implement a "Contact" page with a waitlist form that saves data locally.

**Independent Test**: Verify the contact form saves data to local storage.

### Implementation for User Story 4

- [ ] T025 [US4] Create `app/(pages)/contact/page.tsx` for the Contact page.
- [ ] T026 [US4] Design and implement a waitlist form on `app/(pages)/contact/page.tsx` using shadcn/ui components.
- [ ] T027 [US4] Implement client-side logic to save form submissions to `localStorage`.
- [ ] T028 [US4] Add user feedback for form submission (e.g., success message).

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final review and improvements that affect multiple user stories, ensuring constitutional alignment.

- [ ] T029 [P] Accessibility Audit: Manually test all new UI components for keyboard navigation, screen reader compatibility, and ARIA compliance.
- [ ] T030 [P] Performance Audit: Profile the application using Lighthouse/PageSpeed Insights. Ensure FCP is < 1.5s and bundle size is within the 150KB limit.
- [ ] T031 [P] Responsive UI/UX Review: Test the application on various devices (mobile, tablet, desktop) to confirm mobile-first design and consistent UX.
- [ ] T032 [P] Theming Review: Verify that all new components work correctly in both dark and light modes.
- [ ] T033 [P] Code Refactoring & Reusability: Review new components for potential refactoring into more reusable parts. Ensure TypeScript strict mode is enforced.
- [ ] T034 [P] Documentation: Update `README.md` or any relevant developer documentation for new components or features.
- [ ] T035 Security Hardening: Review for common web vulnerabilities (XSS, CSRF, etc.).
- [ ] T036 Run `quickstart.md` validation: Ensure the project's quickstart guide is up-to-date and works as expected.

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1 - View Home Page)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1 - Read the Book)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2 - Learn About the Author)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2 - Join the Waitlist)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P1 - Mobile and Dark Mode Experience)**: Cross-cutting, tasks integrated throughout, especially in Foundational and Polish phases.

### Within Each User Story

- Implementation tasks are generally sequential within a story.
- Components (e.g., `theme-provider`, `chapter-navigation`) should be created before integration into pages.
- MDX parsing (`lib/mdx.ts`) should be set up before implementing book content rendering.

### Parallel Opportunities

- All Setup tasks in Phase 1 can run in parallel where possible (e.g., installing dependencies, configuring Tailwind/shadcn).
- Foundational tasks in Phase 2 can be worked on in parallel (e.g., layout, navigation, theme provider).
- Once Foundational phase completes, User Stories 1, 2, 3, and 4 can theoretically be worked on in parallel by different team members.
- Within User Story phases, tasks marked with [P] can be parallelized.

## Implementation Strategy

### MVP First (User Story 1 + Key Foundational)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Home Page)
4. **STOP and VALIDATE**: Test Home Page independently with foundational elements.
5. Deploy/demo if ready (minimal viable product).

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together.
2. Once Foundational is done:
   - Developer A: User Story 1 (Home Page)
   - Developer B: User Story 2 (Book Page)
   - Developer C: User Story 3 (About Page) and User Story 4 (Contact Page)
3. Stories complete and integrate independently.

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
