# ADR-005: In-Memory Caching with Redis

## Status
Accepted

## Context

`/names` and future endpoints need to answer "is *firstname.ooo* free?" quickly. Querying the registrar live for 10 000+ names is slow and rate-limited. We need a shared cache that survives code reloads and can be pre-warmed by background jobs.

Requirements:
* µs-level read latency.
* Persistence across container restarts.
* Easy local development.
* Supported by typical PaaS providers.

## Decision

Adopt **Redis 7.x** as the primary cache.

* Chosen image: `redis:7-alpine` (small, stable).
* Added to `docker-compose.yml` with a named volume `redis-data` for durability.
* Backend will connect via `redis://redis:6379/0`.
* TTL-based scheme: `SET name available|taken EX 604800` (7 days) updated by a nightly job.

## Consequences

### Positive
* Sub-millisecond look-ups for API requests.
* One cache shared by all gunicorn/uvicorn workers.
* Durable between deploys thanks to RDB/AOF + Docker volume.

### Negative
* Extra service to operate (memory + monitoring).
* Local dev needs Docker or a native Redis install.

## Alternatives Considered

1. **SQLite / DuckDB file** – simple but worse concurrency, no network sharing.
2. **In-process `lru_cache`** – per-worker duplication, lost on restart.
3. **Managed KV stores (Upstash, Deno KV)** – vendor lock-in, extra latency.

---
Generated with AI on 10.06.25. Likely reviewed by a human ❦ 