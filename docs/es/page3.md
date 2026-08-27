# 3. Ejecución y monitoreo de los servicios

[← Anterior](page2.md) | [Índice](README.md) | [Siguiente: Base de datos y servidor →](page4.md)

## Iniciar

    make start

Este comando construye el stack de Docker y configura el servicio del decodificador LoRa. Para ver la compilación y los registros en tiempo real:

    docker compose -f deploy/docker-compose.yml up --build

Para instalar manualmente el decodificador:

    bash decoder/install_decoders.sh

## Registros

    make logs
    make save-logs

El segundo comando guarda los registros en `logs/`. Para consultar Mosquitto:

    docker compose -f deploy/docker-compose.yml exec mqtt sh -c 'tail -f /mosquitto/log/mosquitto.log'

## Detener

    make stop

Conserva los volúmenes. Para eliminar contenedores, volúmenes y redes:

    make delete-all

Ejecuta `make help` para ver todos los comandos disponibles.
