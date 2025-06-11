.PHONY: help install format lint lint-fix check-all test dev run-api docker-build docker-up docker-down clean

# === Dependency management ===
install: ## Sync Python dependencies with uv
	cd backend && uv sync

# === Quality ===
format: ## Format backend code with ruff
	cd backend && uv run ruff format .

lint: ## Lint backend code with ruff
	cd backend && uv run ruff check .

lint-fix: ## Auto-fix lint issues
	cd backend && uv run ruff check . --fix

check-all: format lint-fix ## Format then fix lint issues

# === Tests ===
test: ## Run pytest suite
	cd backend && uv run pytest -q

# === Dev server ===
dev: ## Start Redis, backend (reload) & SvelteKit frontend
	# Ensure Redis side-car is running
	docker compose up -d redis
	# Start backend in background
	(cd backend && uv run uvicorn app:app --reload --host 0.0.0.0 --port 8000 &)
	# Start frontend in background
	cd frontend && bun run dev
	# Open docs and frontend in browser (macOS `open`)
	open http://localhost:8000/docs >/dev/null 2>&1 || true
	open http://localhost:5173 >/dev/null 2>&1 || true
	# Open Medis (macOS GUI Redis browser)
	open /Applications/Medis.app 

run-api: dev ## Alias for dev

# === Docker ===
docker-build: ## Build local images via compose
	docker compose build

docker-up: ## Start stack (backend + redis) in background
	docker compose up -d

docker-down: ## Stop stack and remove containers
	docker compose down

# === Misc ===
clean: ## Remove Python cache files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}' 