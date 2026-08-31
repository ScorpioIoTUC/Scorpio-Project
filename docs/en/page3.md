# 3. Running and monitoring with Scorpio CLI

[← Previous](page2.md) | [Contents](README.md) | [Next: Scorpio Developers →](page4.md)

Scorpio CLI provides a single interface for installing, running, and managing the local infrastructure.

## Available commands

```text
scorpio ui             Start the setup interface
scorpio setup          Install host dependencies
scorpio setup-docker   Configure and start Docker infrastructure
scorpio start          Start Scorpio services
scorpio stop           Stop Scorpio services and preserve data
scorpio status         Show service status
scorpio logs           Follow service logs
scorpio build          Build Docker images
scorpio reset          Stop services and permanently remove Docker data
```

## Common operations

Start the services:

```bash
scorpio start
```

Inspect their status or follow their logs:

```bash
scorpio status
scorpio logs
```

Stop the services without deleting persistent data:

```bash
scorpio stop
```

`scorpio reset` removes the Docker volumes containing MQTT data, logs, and the SQLite database. It requires explicit confirmation.

## Upgrade or uninstall Scorpio CLI

```bash
pipx upgrade scorpio-cli
pipx uninstall scorpio-cli
```
