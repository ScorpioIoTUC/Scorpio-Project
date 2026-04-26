COMPOSE_FILE := deploy/docker-compose.yml
COMPOSE := docker compose -f $(COMPOSE_FILE)
COMPOSE_SUDO := sudo docker compose -f $(COMPOSE_FILE)
SHELL := /bin/bash
VENV_DIR := .venv
VENV_PY := $(VENV_DIR)/bin/python

.PHONY: up down down-v down-all build ps logs app-shell sqlite-schema sqlite-last help setup-host setup-docker setup-all setup-dev lint

define RUN_COMPOSE
	@set +e; \
	output="$$( $(COMPOSE) $(1) 2>&1 )"; status=$$?; set -e; \
	if [ $$status -eq 0 ]; then \
		printf '%s\n' "$$output"; \
	elif printf '%s\n' "$$output" | grep -qi 'permission denied while trying to connect to the docker API'; then \
		echo 'Docker permission denied; retrying with sudo...'; \
		$(COMPOSE_SUDO) $(1); \
	else \
		printf '%s\n' "$$output"; \
		exit $$status; \
	fi
endef

define RUN_COMPOSE_DIRECT
	@set +e; \
	check_out="$$(docker info 2>&1)"; check_status=$$?; set -e; \
	if [ $$check_status -eq 0 ]; then \
		$(COMPOSE) $(1); \
	elif printf '%s\n' "$$check_out" | grep -qi 'permission denied'; then \
		echo 'Docker permission denied; retrying with sudo...'; \
		$(COMPOSE_SUDO) $(1); \
	else \
		printf '%s\n' "$$check_out"; \
		exit $$check_status; \
	fi
endef

help:
	@printf '%s\n' "Available targets:" \
	  "  make up            Build and start the stack" \
	  "  make down          Stop services (keep volumes/data)" \
	  "  make down-v        Stop services and remove volumes/data" \
	  "  make down-all      Alias of down-v" \
	  "  make build         Build images only" \
	  "  make ps            Show container status" \
	  "  make logs          Follow data-ingest logs" \
	  "  make app-shell     Open a shell in the app container" \
	  "  make sqlite-schema Print the SQLite schema for heartbeats" \
	  "  make sqlite-last    Print the last 5 heartbeats" \
	  "  make setup-dev     Create a local virtualenv and install Python tools" \
	  "  make lint           Run Ruff lint checks" \
	  "  make setup-host    Install host dependencies and reboot" \
	  "  make setup-docker  Install/check Docker and start infrastructure services" \
	  "  make setup-all     Run host setup, reboot, then continue with Docker after login"

up:
	$(call RUN_COMPOSE,up -d --build)

down:
	$(call RUN_COMPOSE,down)

down-v:
	$(call RUN_COMPOSE,down -v)

down-all: down-v

build:
	$(call RUN_COMPOSE,build)

ps:
	$(call RUN_COMPOSE,ps)

logs:
	$(call RUN_COMPOSE_DIRECT,logs -f data_ingest)

app-shell:
	$(call RUN_COMPOSE_DIRECT,exec app sh)

sqlite-schema:
	$(call RUN_COMPOSE,exec app python -c "import sqlite3; c=sqlite3.connect('/data/infra_check.db'); print(c.execute(\"SELECT sql FROM sqlite_master WHERE type='table' AND name='heartbeats'\").fetchone()[0])")

sqlite-last:
	$(call RUN_COMPOSE,exec app python -c "import sqlite3; c=sqlite3.connect('/data/infra_check.db'); rows=c.execute(\"SELECT id, ts_utc, topic, payload FROM heartbeats ORDER BY id DESC LIMIT 5\").fetchall(); [print(row) for row in rows]")

setup-host:
	@echo "[setup-host] Installing host dependencies (system will reboot when complete)..."
	bash ./dependencies.sh --no-reboot

setup-docker:
	bash ./scripts/bootstrap.sh --docker-only

setup-all:
	@$(MAKE) setup-host
	@echo ""
	@echo "After login, run: make setup-docker"

setup-dev:
	python3 -m venv $(VENV_DIR)
	$(VENV_PY) -m pip install --upgrade pip
	$(VENV_PY) -m pip install -r requirements.txt

lint:
	@if [ ! -x "$(VENV_PY)" ]; then \
		echo "Create the dev environment first: make setup-dev"; \
		exit 1; \
	fi
	$(VENV_PY) -m ruff check . --fix
	