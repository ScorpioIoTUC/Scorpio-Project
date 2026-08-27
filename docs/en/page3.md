# 3. Running and monitoring the services

[← Previous](page2.md) | [Contents](README.md) | [Next: Database and server →](page4.md)

## Start

    make start

This command builds the Docker stack and configures the LoRa decoder service. To watch the build and live logs:

    docker compose -f deploy/docker-compose.yml up --build

To install the decoder manually:

    bash decoder/install_decoders.sh

## Logs

    make logs
    make save-logs

The second command saves logs in `logs/`. To inspect Mosquitto:

    docker compose -f deploy/docker-compose.yml exec mqtt sh -c 'tail -f /mosquitto/log/mosquitto.log'

## Stop

    make stop

This keeps the volumes. To remove containers, volumes, and networks:

    make delete-all

Run `make help` to see all available commands.
