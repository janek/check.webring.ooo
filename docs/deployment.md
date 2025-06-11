# Deployment Guide

This document collects the practical steps and decisions for shipping **check.webring.ooo** beyond local development. It complements:

* ADR-001 (Tech-stack),
* ADR-002 (Progressive data loading),
* ADR-004 (Containerisation),
* ADR-005 (Redis caching).

---

## Current status (11-06-25)

* **Backend** – FastAPI served via `uvicorn`, already containerised (`Dockerfile`) and managed together with Redis by `docker-compose.yml`.
* **Frontend** – Svelte SPA, _not_ yet containerised. Developers run `bun run dev` locally, Vite proxies `localhost:8000` for API calls.

## Deployment targets

| Layer      | Local DX | Staging / Prod Option A | Staging / Prod Option B |
|------------|----------|-------------------------|-------------------------|
| Backend    | bare `uvicorn` or `make run-backend` | Docker image (Python slim) | same |
| Redis      | Docker (compose) | Docker (compose) | same |
| Frontend   | `bun` + Vite HMR | **Separate** `frontend` image (nginx) | **Bundled** inside backend image |

Notes:
1. Option A keeps static files in a lightweight nginx container – good for CDNs, clear separation.
2. Option B bakes the static `dist/` folder into the backend image – one moving part, fine at our scale.

## Building the frontend image (Option A)

```Dockerfile
FROM oven/bun:1 AS build
WORKDIR /app
COPY frontend/ .
RUN bun install --frozen-lockfile && bun run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
```

Compose stanza:
```yaml
frontend:
  build: ./frontend
  ports:
    - "3000:80"
  depends_on:
    - backend
```

## Bundling into backend (Option B)

1. Add a **builder** stage identical to the snippet above at the top of the existing `Dockerfile`.
2. In the final stage:
   ```Dockerfile
   COPY --from=build /app/dist /app/static
   ```
3. Mount the folder in FastAPI:
   ```python
   from fastapi.staticfiles import StaticFiles
   app.mount("/", StaticFiles(directory="static", html=True), name="static")
   ```

## Environment variables

| Var                    | Example                     | Used by |
|------------------------|-----------------------------|---------|
| `VITE_API_BASE`        | `https://api.webring.ooo`   | Frontend |
| `REDIS_URL`            | `redis://redis:6379/0`      | Backend  |

## Roll-out hints

* Fly.io / Render: run `fly deploy` or `render.yaml` with the two images.
* Netlify / Vercel: host the contents of `frontend/dist` directly if you choose Option A.
* GitHub Actions: cache Bun's layer for faster builds: `bun install --cache`.

---
Generated with AI on 11.06.25. Likely reviewed by a human ✯◡✯ 