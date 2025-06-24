ifneq (,$(wildcard .env))
    include .env
    $(eval export $(shell sed -ne 's/ *#.*$$//; /./ s/=.*$$// p' .env))
endif

.PHONY: help
help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

.PHONY: install
install:         ## Install the dependencies.
	@uv sync

.PHONY: clean
clean:            ## Clean unused files.
	@find ./ -path './.venv' -prune -o -name '*.pyc' -exec rm -f {} \;
	@find ./ -path './.venv' -prune -o -name '__pycache__' -exec rm -rf {} \;
	@find ./ -path './.venv' -prune -o -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -path './.venv' -prune -o -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf .coverage
	@rm -rf .ruff_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build

.PHONY: format
format:           ## Format the code.
	@ruff check --fix
	@ruff format

.PHONY: lint
lint:             ## Lint the code.
	@ruff check

.PHONY: docker-up
docker-up:        ## Start the Docker containers.
	@docker compose -f 'docker/dev/compose.yml' up -d --build

.PHONY: docker-down
docker-down:      ## Stop the Docker containers.
	@docker compose -f 'docker/dev/compose.yml' down

.PHONY: dev
dev: docker-up    ## Run the development server with Docker.
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "❌ Error: Please activate your virtual environment before running this command."; \
		echo "💡 Tip: Run 'source .venv/bin/activate' or 'uv venv --seed && source .venv/bin/activate'"; \
		exit 1; \
	fi
	@echo "✅ Virtual environment detected: $$VIRTUAL_ENV"
	@echo "🚀 Starting development server..."
	@fastapi dev src/app/main.py
