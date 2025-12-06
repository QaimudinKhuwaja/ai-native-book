# Research: AI-Native Book Website

## Decisions

- **Framework**: Next.js 15 with App Router
- **Styling**: Tailwind CSS with shadcn/ui
- **Content**: MDX
- **Deployment**: Vercel

## Rationale

- **Next.js 15**: Provides a robust, full-stack framework with excellent performance and developer experience. The App Router enables a modern, flexible routing and layout system.
- **Tailwind CSS & shadcn/ui**: Offers a utility-first CSS framework for rapid UI development and a set of beautifully designed, accessible components that can be easily customized. This aligns with the "Zero External UI Libraries" principle.
- **MDX**: Allows for writing content in Markdown and embedding interactive React components directly within the content, which is ideal for a book website. It also aligns with the "MDX for All Book Content" principle.
- **Vercel**: As the creators of Next.js, Vercel provides a seamless and optimized deployment experience for Next.js applications.

## Alternatives Considered

- **Gatsby**: A powerful static site generator, but can be more complex to set up and maintain than Next.js for this project's needs.
- **Astro**: Another excellent static site generator with a focus on performance, but Next.js provides a more integrated full-stack experience.
- **Vanilla React with a static site generator**: Would require more manual setup and configuration for routing, content loading, and deployment.
