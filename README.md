# Scorpio-Project

Docker-based stack for the Scorpio pipeline:

- `mqtt`: Mosquitto broker
- `data_ingest`: publishes mock MQTT traffic
- `data_storage`: stores and republishes pending data
- `data_clean`: removes uploaded records

## Quick Start

```bash
make setup-all
```

After reboot:

```bash
make setup-docker
```

Start the stack locally:

```bash
make start
```

`make start` falls back to `sudo` if Docker permissions are missing.

## Useful Commands

Stop the stack keeping the volumes:

```bash
make down
```
If you need to stop and remove all containers, volumes, and networks:

```bash
make down-all
```

For more commands, execute the command `make help` to see the full list of available commands and their descriptions.

## Logs

Preview the logs of all services in real-time

```bash
make logs
```

Save them to a file (ordered by timestamp):

```bash
make save-logs
```

The result file will contain all logs from the services, and saved in the logs/ directory as *<timestamp>_all_containers.log*. 

Read Mosquitto’s file log:

```bash
docker compose -f deploy/docker-compose.yml exec mqtt sh -c 'tail -f /mosquitto/log/mosquitto.log'
```

## Data

Persistence uses Docker volumes: `mqtt_data`, `mqtt_log`, and `sqlite_data`.

### SQlite CLI
To access the SQLite database local_backup.db, you can use the following command:

```bash
make sqlite-shell
```

## Development

```bash
make setup-dev
make lint
```

If Docker access fails on Linux, add your user once:

```bash
sudo usermod -aG docker $USER
```

Then log out and back in.
