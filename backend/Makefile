.PHONY: format lint lint-fix dev check-all help

format:
	@echo "⟐ Formatting code with ruff..."
	uv run ruff format .

lint:
	@echo "⟢ Checking code with ruff..."
	uv run ruff check .

lint-fix:
	@echo "⟡ Auto-fixing linting issues..."
	uv run ruff check . --fix

dev:
	@echo "ᚖ Starting development server..."
	uv run uvicorn app:app --reload

check-all: format lint-fix
	@echo "✯ All formatting and linting complete!"

help:
	@echo "Available commands:"
	@echo "  format     - Format code with ruff"
	@echo "  lint       - Check code with ruff"
	@echo "  lint-fix   - Auto-fix linting issues"
	@echo "  dev        - Start development server"
	@echo "  check-all  - Format and fix all issues" 