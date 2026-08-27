# 4. Local database and Scorpio Server connection

[← Previous](page3.md) | [Contents](README.md) | [Next: LoRa decoder →](page5.md)

## Components

- **Docker stack:** `mqtt`, `data_ingest`, `data_preprocess`, `data_storage`, `data_clean`, and `data_export`.
- **Decoder:** `lora-decoder@<username>.service`, which forwards LoRa frames to `data_ingest`.

Persistence uses the `mqtt_data`, `mqtt_log`, and `sqlite_data` volumes.

## SQLite

    make sqlite-shell

This opens the local `local_backup.db` database.

## Scorpio Server

Place `.env` in the project’s main directory:

    SCORPIO_API_URL=<API_URL>
    SCORPIO_STATION_KEY=<KEY>

Register the station on the website first. The server will provide a one-time key for sending data. For local development:

    SCORPIO_API_URL=http://api:3000/packets
