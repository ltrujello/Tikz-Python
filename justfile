install-dev:
    uv sync --all-groups 
    pre-commit install

lint:
    uv run black -t py314 src/ tests/ && uv run ruff check --fix src/ tests/

test: 
    uv run pytest tests/unit

test-integration:
    uv run pytest tests/integration
