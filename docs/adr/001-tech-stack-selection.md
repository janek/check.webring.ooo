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

## Concerns
### Hosting Implications
The decision to use separate FastAPI backend and Svelte frontend has significant implications for free hosting options:

- **Deployment complexity**: Requires two separate deployments instead of a single Next.js deployment
- **Free hosting limitations**: 
  - Frontend (Svelte): Can be deployed to Netlify, Vercel, GitHub Pages easily as static files
  - Backend (FastAPI): Limited free Python hosting options compared to Node.js
  - Vercel/Netlify serverless functions have limitations for Python backends
  - Railway, Render, or Fly.io free tiers may be needed for the Python backend
- **Cost implications**: May need paid hosting sooner than with a unified Next.js approach on Vercel free tier
- **Environment management**: Need to manage separate environment variables and configurations for two deployments
- **API endpoint coordination**: Frontend needs to know backend URL, complicating environment-specific deployments

Alternative Next.js approach would have offered simpler deployment to Vercel free tier with API routes, but sacrifices the Python ecosystem benefits and Svelte's lightweight nature.

## Implementation Notes
- Backend: FastAPI with `uv` for dependency management, `ruff` for linting
- Frontend: Svelte with `prettier` for formatting
- API-first approach with clear separation of concerns

---
Generated with AI on 20.12.24. Likely reviewed by a human ◉‿◉ 