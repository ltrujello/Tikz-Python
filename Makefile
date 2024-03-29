.PHONY: default
default: black lint test

.PHONY: black
black:
	black tests src

.PHONY: lint
lint:
	ruff check src/tikzpy/*.py        

.PHONY: test
test:
	pytest tests
