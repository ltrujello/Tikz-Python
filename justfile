install-dev:
    uv sync --all-groups 
    pre-commit install

lint:
    uv run black . && uv run ruff check --fix .

test: 
    uv run pytest tests
