# ADR-004: Containerization Strategy with Docker

## Status
Accepted

## Context

The `check.webring.ooo` backend is currently started directly via `uvicorn` (see `Makefile`). While this workflow is ideal for local development, we need a reproducible, environment-agnostic way to deploy to any cloud or edge platform. Containerizing the service makes it easy to:

* Guarantee the correct Python (3.12) runtime and system libraries.
* Bundle the heavy `names-dataset` dependency once, avoiding repeated downloads on every deploy.
* Run the API identically in production, staging, and CI.
* Layer in side-cars (Redis, Nginx) later via Compose or Kubernetes without rewriting startup scripts.

## Decision

We will:

1. **Add a single-stage `Dockerfile`** at repository root that:
   * Uses the official `python:3.12-slim` image as a base.
   * Installs runtime dependencies (`fastapi`, `uvicorn[standard]`, `names-dataset`).
   * Copies the `backend/` source and sets the default command to
     ```bash
     uvicorn app:app --host 0.0.0.0 --port 8000
     ```
2. **Create a `.dockerignore`** to keep the build context minimal (skips Git, caches, IDE folders).
3. **Document usage** (build & run) in the top-level `README.md`.

No `docker-compose.yml` yet – that will arrive once Redis is introduced (see forthcoming ADR-005).

## Consequences

### Positive
* One-command deploy to any container host (Fly.io, Railway, Render, etc.).
* Eliminates "works on my machine" discrepancies.
* Simplifies CI – just `docker build` & `docker run --health-cmd="curl…"`.

### Negative
* Image is ~250 MB compressed due to the `names-dataset` asset bundle.
* Cold-start slightly slower compared to a bare-metal `uvicorn` start (container init).

## Alternatives Considered
1. **Poetry-based multi-stage build** – adds complexity with little gain at current scale.
2. **Using `flyctl deploy` without Dockerfile** – vendor-specific, ties us to one platform.
3. **Serverless (AWS Lambda / Vercel Functions)** – tricky with the 120 MB in-memory dataset and long initialisation time.

## References
* [Docker Official Images – python](https://hub.docker.com/_/python)
* <docs/adr/002-progressive-data-loading-strategy.md>
* <docs/adr/003-names-dataset-integration.md>

---
Generated with AI on 10.06.25. Likely reviewed by a human ꧁༺𓀀༻꧂ 