.PHONY: help test-names run-api install clean

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install backend dependencies
	cd backend && uv sync

test-names: ## Test the names dataset library
	cd backend && uv run python test_names.py

run-api: ## Start the FastAPI development server
	cd backend && uv run uvicorn app:app --reload --host 0.0.0.0 --port 8000

clean: ## Clean up cache files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

check: ## Run linting checks
	cd backend && uv run ruff check . 