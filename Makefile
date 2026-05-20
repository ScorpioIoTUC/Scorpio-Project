COMPOSE_FILE := deploy/docker-compose.yml
COMPOSE := docker compose -f $(COMPOSE_FILE)
COMPOSE_SUDO := sudo docker compose -f $(COMPOSE_FILE)
SHELL := /bin/bash
VENV_DIR := .venv
VENV_PY := $(VENV_DIR)/bin/python

.PHONY: start stop delete-all build ps logs app-shell sqlite-shell sqlite-schema help setup-host setup-docker setup-all setup-dev lint save-logs

.PHONY: docker-logs decoder-logs

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
	  "  make start         Build and start the stack" \
	  "  make stop          Stop services (keep volumes/data)" \
	  "  make delete-all    Stop services and remove volumes/data" \
	  "  make build         Build images only" \
	  "  make ps            Show container status" \
	  "  make app-shell     Open a shell in the data_storage container" \
	  "  make sqlite-shell  Open an interactive SQLite shell" \
	  "  make sqlite-schema Print the SQLite schema for heartbeats" \
	  "  make setup-dev     Create a local virtualenv and install Python tools" \
	  "  make lint          Run Ruff lint checks" \
	  "  make logs          Preview the logs from all the containers in real-time" \
	  "  make save-logs     Save the logs in a external file" \
	  "  make setup-host    Install host dependencies and reboot" \
	  "  make setup-docker  Install/check Docker and start infrastructure services" \
	  "  make setup-all     Run host setup, reboot, then continue with Docker after login"

start:
	@echo "Starting Docker stack..."
	$(call RUN_COMPOSE,up -d --build)
	@echo ""
	@echo "Installing LoRa Decoder service..."
	bash decoder/install_decoders.sh

stop:
	@echo "Stopping Docker stack..."
	$(call RUN_COMPOSE,down)
	@echo ""
	@echo "Stopping LoRa Decoder service..."
	sudo systemctl stop lora-decoder@scorpio.service

delete-all:
	$(call RUN_COMPOSE,down -v)


build:
	$(call RUN_COMPOSE,build)

ps:
	$(call RUN_COMPOSE,ps)

logs:
	docker compose -f deploy/docker-compose.yml logs -f

docker-logs: logs

decoder-logs:
	@echo "Tailing lora-decoder service logs (may require sudo)"
	@sudo journalctl -u lora-decoder@$(shell whoami).service -f

save-logs:
	bash scripts/save_logs.sh

app-shell:
	$(call RUN_COMPOSE_DIRECT,exec data_storage sh)

sqlite-shell:
	$(call RUN_COMPOSE_DIRECT,exec data_storage python -m sqlite3 /data/sat_data.db)

sqlite-schema:
	$(call RUN_COMPOSE,exec data_storage python -c "import sqlite3; c=sqlite3.connect('/data/sat_data.db'); print(c.execute(\"SELECT sql FROM sqlite_master WHERE type='table' AND name='local_backup'\").fetchone()[0])")

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
	