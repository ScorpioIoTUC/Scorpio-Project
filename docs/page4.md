
## Acceso a base de datos local y conexión al servidor de Scorpio

Scorpio pipeline with two runtime parts:

- Docker stack: `mqtt`, `data_ingest`, `data_preprocess`, `data_storage`, `data_clean`, `data_export`
- Decoder service: `lora-decoder@<user>.service`, which listens to LoRa and forwards messages into `data_ingest`

Persistence uses Docker volumes: `mqtt_data`, `mqtt_log`, and `sqlite_data`.

### SQlite CLI
To access the SQLite database local_backup.db, you can use the following command:

```bash
make sqlite-shell
```

## Server connection
You need an environment file (`.env`) to send packets to the Scorpio Server.

The server requires authentication, so you must first register a station on the website. Once the station is registered, the server will provide a **one-time key that allows you to send data**.

In this project, the `.env` file must be placed in the main directory.

```bash
SCORPIO_API_URL=<API_URL>
SCORPIO_STATION_KEY=<KEY>
```

For **local development**, the API URL should be:

```bash
SCORPIO_API_URL=http://api:3000/packets
```