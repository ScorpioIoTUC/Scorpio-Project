#!/usr/bin/env python3
"""Simple infrastructure checker for MQTT + SQLite.

This container publishes heartbeat messages to Mosquitto and stores each
heartbeat in a SQLite database file mounted on a Docker volume.
"""

import json
import os
import signal
import sqlite3
import sys
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt


MQTT_HOST = os.getenv("MQTT_HOST", "mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "infra/heartbeat")
DB_PATH = os.getenv("SQLITE_DB_PATH", "/data/infra_check.db")
INTERVAL_SEC = int(os.getenv("HEARTBEAT_INTERVAL_SEC", "10"))

running = True


def stop_handler(signum, frame):
    del signum, frame
    global running
    running = False


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS heartbeats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts_utc TEXT NOT NULL,
            topic TEXT NOT NULL,
            payload TEXT NOT NULL
        )
        """
    )
    conn.commit()


def main() -> int:
    signal.signal(signal.SIGINT, stop_handler)
    signal.signal(signal.SIGTERM, stop_handler)

    client_id = f"infra-checker-{int(time.time())}"
    mqtt_client = mqtt.Client(client_id=client_id)

    def on_connect(client, userdata, flags, reason_code, properties=None):
        del client, userdata, flags, properties
        print(f"[mqtt] connected with code: {reason_code}")

    mqtt_client.on_connect = on_connect

    print(f"[startup] MQTT broker: {MQTT_HOST}:{MQTT_PORT}")
    print(f"[startup] SQLite file: {DB_PATH}")

    mqtt_client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    mqtt_client.loop_start()

    conn = sqlite3.connect(DB_PATH)
    init_db(conn)

    try:
        while running:
            ts_utc = datetime.now(timezone.utc).isoformat()
            payload_obj = {
                "service": "infra-checker",
                "status": "ok",
                "ts_utc": ts_utc,
            }
            payload = json.dumps(payload_obj)

            result = mqtt_client.publish(MQTT_TOPIC, payload=payload, qos=0, retain=False)
            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                print(f"[mqtt] publish failed with rc={result.rc}")

            conn.execute(
                "INSERT INTO heartbeats (ts_utc, topic, payload) VALUES (?, ?, ?)",
                (ts_utc, MQTT_TOPIC, payload),
            )
            conn.commit()

            print(f"[ok] heartbeat published and stored at {ts_utc}")
            time.sleep(INTERVAL_SEC)
    finally:
        conn.close()
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        print("[shutdown] infra-checker stopped cleanly")

    return 0


if __name__ == "__main__":
    sys.exit(main())
