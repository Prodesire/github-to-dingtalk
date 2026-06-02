.DEFAULT_GOAL := help
.PHONY: help install dev test lint format build deploy clean

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies and git hooks
	uv sync
	cp hooks/pre-commit .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

dev: ## Start dev server with hot reload
	uv run uvicorn github_to_dingtalk.app:app --host 0.0.0.0 --port 9000 --reload

test: ## Run tests
	uv run pytest -v

lint: ## Run linter and type checker
	uv run ruff check src tests
	uv run ty check src

format: ## Format code
	uv run ruff format src tests

build: ## Build deployment package
	deploy/aliyun-fc/build.sh

deploy: build ## Build and deploy to Aliyun FC
	s -t deploy/aliyun-fc/s.yml github-notification deploy -y

clean: ## Clean build artifacts
	rm -rf build/ dist/ .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
