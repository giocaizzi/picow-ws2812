.DEFAULT_GOAL := help
.PHONY: help lint test check

help: ## Show this help
	@grep -E '^[a-z]+:.*## ' $(MAKEFILE_LIST) | awk -F ':.*## ' '{printf "  %-8s %s\n", $$1, $$2}'

lint: ## Lint and check formatting with ruff, type-check with mypy
	uv run ruff check
	uv run ruff format --check
	uv run mypy

test: ## Run the host-side test suite
	uv run pytest

check: lint test ## lint + test
