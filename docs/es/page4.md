# 4. Base de datos local y conexión con Scorpio Server

[← Anterior](page3.md) | [Índice](README.md) | [Siguiente: Decodificador LoRa →](page5.md)

## Componentes

- **Stack Docker:** `mqtt`, `data_ingest`, `data_preprocess`, `data_storage`, `data_clean` y `data_export`.
- **Decodificador:** `lora-decoder@<usuario>.service`, que entrega las tramas LoRa a `data_ingest`.

La persistencia usa los volúmenes `mqtt_data`, `mqtt_log` y `sqlite_data`.

## SQLite

    make sqlite-shell

Este comando abre la base de datos local `local_backup.db`.

## Scorpio Server

Coloca `.env` en el directorio principal del proyecto:

    SCORPIO_API_URL=<API_URL>
    SCORPIO_STATION_KEY=<KEY>

Registra primero la estación en el sitio web. El servidor entregará una clave de uso único para enviar datos. En desarrollo local:

    SCORPIO_API_URL=http://api:3000/packets
