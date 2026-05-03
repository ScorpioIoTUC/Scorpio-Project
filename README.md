# Scorpio-Project

## Recommended installation flow (Raspberry Pi + Docker)

Use this command to start the full installation flow:

```bash
make setup-all
```

What it does:

1. Installs host dependencies (GNU Radio, SDR rules, system libs).
2. Reboots the Raspberry Pi automatically.

After reboot and login, continue with:

```bash
make setup-docker
```

## Docker starter infrastructure

This project now includes a minimal Docker deployment to validate infrastructure:

- `mqtt`: Mosquitto broker (`eclipse-mosquitto:2`)
- `app`: Python checker service that publishes MQTT heartbeats and stores them in SQLite
- Named volumes for persistence (`mqtt_data`, `mqtt_log`, `sqlite_data`)

### Files added/updated

- `deploy/docker-compose.yml`
- `Makefile`
- `docker/base/Dockerfile.base`
- `docker/mosquitto/mosquitto.conf`
- `requirements.txt`
- `src/app/infra_check.py`
- `.dockerignore`

### Start the stack

```bash
make up
```

The Makefile retries with `sudo` automatically if Docker socket permissions are denied.

### Check containers and logs

```bash
make ps
make logs
```

Expected app log line every 10 seconds:

```text
[ok] heartbeat published and stored at <timestamp>
```

### Local linting

Ruff is installed into a local virtual environment so it does not depend on system Python packages:

```bash
make setup-dev
make lint
```

### Verify SQLite data is persisted

```bash
make sqlite-schema
```

### Stop the stack

```bash
make down
```

To also remove persisted volumes:

```bash
make down-v
```

## Docker permission fix (Linux)

If you get `permission denied while trying to connect to the docker API at unix:///var/run/docker.sock`, add your user to the `docker` group one time:

```bash
sudo usermod -aG docker $USER
```

Then log out and log back in. `newgrp docker` only fixes the current terminal session; a full re-login is what makes new terminals work.

If you do not want to restart your session right now, `make up` will fall back to `sudo` automatically.

### Inspect the SQLite schema

```bash
make sqlite-schema
```

### Inspect the latest rows

```bash
make sqlite-last
```

# Logs
```bash
docker compose -f deploy/docker-compose.yml logs -f
```