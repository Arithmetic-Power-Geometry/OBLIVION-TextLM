.PHONY: install test lint demo run docker
install:
	python -m pip install -e ".[dev]"
test:
	pytest
lint:
	ruff check src tests
demo:
	oblivion-textlm demo
run:
	uvicorn oblivion_textlm.api:app --host 0.0.0.0 --port 8080
docker:
	docker compose up --build
