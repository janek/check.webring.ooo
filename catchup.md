# Project Catchup - check.webring.ooo

## 🎯 What We're Building

A tool to check if `.ooo` domain names (especially first names) are available and if they're part of the webring. Simple, fast, with that nostalgic internet vibe.

## ✅ What's Done

- **Tech Stack**: FastAPI backend (ADR-001) – frontend on hold
- **Containerisation**: Single-stage `Dockerfile` + `.dockerignore` (ADR-004)
- **Orchestration**: `docker-compose.yml` runs API + Redis 7 side-car
- **Caching**: Redis chosen for domain availability cache (ADR-005)
- **Project Structure**: `backend/`, `docs/`, Makefile all tidy
- **Basic API**: Hello world at `/`, `/names` endpoint powered by `names-dataset`
- **Names Data**: Integrated `names-dataset` (top names logic) – see ADR-003
- **Dev Tools**: `make dev`, `ruff`, and minimal four-line `README.md`

## 🧪 Current State

```bash
docker compose up -d   # start API + Redis
docker compose down    # stop stack
make dev               # hot-reload server outside Docker (optional)
```

**API Status**: `/names` working with top-name sampling; dataset initialises once per process.
**Infrastructure**: Redis is running but not yet wired into the Python code.

## 🚀 Next Session Priorities

1. **Wire Redis cache**
   - Dependency: `redis.asyncio` client
   - FastAPI dependency to read/write `firstname.ooo` availability with TTL
2. **Background refresh worker**
   - Nightly job to re-populate cache for top 10 k names
3. **Autocomplete endpoint**
   - `dataset.auto_complete()` exposed at `/autocomplete`
4. **Frontend revival** (low priority)

## 📁 Key Files to Remember

- `backend/app.py` - Main FastAPI app (currently basic)
- `backend/test_names.py` - Names dataset testing (working examples)
- `Makefile` - Your friend for common tasks
- `docs/adr/` - All architectural decisions documented

## 🤔 Open Questions

- What registrar/API will we use for reliable `.ooo` availability checks?
- How often should "taken" domains be re-checked compared to "free" ones?
- Do we need rate-limit protection on public endpoints?

## 🎪 Fun Facts Discovered

- Names dataset has auto-complete that works amazingly well
- Top names vary wildly by country (محمد vs John vs 영수)
- Library loads 727k first names + 983k last names
- Ali autocompletes to: Ali, Alicia, Alice, Alina, Alison

---

**TL;DR**: Backend foundation solid, names data working great, next = build real API endpoints with the rich name data. Start with `/names` endpoint replacement! ∾◡∾
