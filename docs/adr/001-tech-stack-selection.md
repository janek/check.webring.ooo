# ADR-001: Tech Stack Selection

## Status
Accepted

## Context
For check.webring.ooo, we need to choose a tech stack that aligns with the project's goals:
- Simple, fast domain availability checking
- Clean, minimal UI that matches webring.ooo's "simple HTML vibe"
- Quick development and deployment
- Good performance for API calls to check domain availability

Two main options were considered:
- **Option A**: FastAPI (Python) backend + Svelte frontend
- **Option B**: React + Next.js full-stack

## Decision
We will use **Option A**: FastAPI backend with Svelte frontend.

## Rationale
- **FastAPI**: Excellent for rapid API development, built-in OpenAPI docs, great async support for domain checking operations, and familiar Python ecosystem
- **Svelte**: Lightweight, fast, produces minimal bundle sizes, and has a clean syntax that matches the project's simple aesthetic
- **Tooling alignment**: Python tooling with `uv` and `ruff` provides excellent DX, `prettier` for Svelte formatting
- **Performance**: Both FastAPI and Svelte are known for excellent performance characteristics
- **Simplicity**: Matches the project's goal of keeping things simple and clean

## Consequences
- Separate frontend/backend deployment (vs. unified Next.js deployment)
- Need to manage CORS configuration
- Two different development servers during local development
- Python backend knowledge required alongside JavaScript frontend skills

## Implementation Notes
- Backend: FastAPI with `uv` for dependency management, `ruff` for linting
- Frontend: Svelte with `prettier` for formatting
- API-first approach with clear separation of concerns 