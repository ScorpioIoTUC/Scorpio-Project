COMPOSE_FILE := deploy/docker-compose.yml
COMPOSE := docker compose -f $(COMPOSE_FILE)
COMPOSE_SUDO := sudo docker compose -f $(COMPOSE_FILE)
SHELL := /bin/bash

.PHONY:  up down down-v build ps logs app-shell sqlite-schema sqlite-last help setup-host setup-docker setup-all

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

help:
	@printf '%s\n' "Available targets:" \
	  "  make up            Build and start the stack" \
	  "  make down-v        Stop the stack and remove volumes" \
	  "  make build         Build images only" \
	  "  make ps            Show container status" \
	  "  make logs          Follow app logs" \
	  "  make app-shell     Open a shell in the app container" \
	  "  make sqlite-schema Print the SQLite schema for heartbeats" \
	  "  make sqlite-last    Print the last 5 heartbeats" \
	  "  make setup-host    Install host dependencies and reboot" \
	  "  make setup-docker  Install/check Docker and start infrastructure services" \
	  "  make setup-all     Run host setup, reboot, then continue with Docker after login"

up:
	$(call RUN_COMPOSE,up -d --build)

down:
	$(call RUN_COMPOSE,down -v)

build:
	$(call RUN_COMPOSE,build)

ps:
	$(call RUN_COMPOSE,ps)

logs:
	$(call RUN_COMPOSE,logs -f app)

app-shell:
	$(call RUN_COMPOSE,exec app sh)

sqlite-schema:
	$(call RUN_COMPOSE,exec app python -c "import sqlite3; c=sqlite3.connect('/data/infra_check.db'); print(c.execute(\"SELECT sql FROM sqlite_master WHERE type='table' AND name='heartbeats'\").fetchone()[0])")

sqlite-last:
	$(call RUN_COMPOSE,exec app python -c "import sqlite3; c=sqlite3.connect('/data/infra_check.db'); rows=c.execute(\"SELECT id, ts_utc, topic, payload FROM heartbeats ORDER BY id DESC LIMIT 5\").fetchall(); [print(row) for row in rows]")

setup-host:
	@echo "[setup-host] Installing host dependencies (system will reboot when complete)..."
	bash ./dependencies.sh

setup-docker:
	bash ./scripts/bootstrap.sh --docker-only

setup-all:
	@$(MAKE) setup-host
	@echo ""
	@echo "After login, run: make setup-docker"