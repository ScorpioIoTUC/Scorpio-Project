#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import signal
import sys
import time
from datetime import datetime

import paho.mqtt.client as mqtt

from decoder.libs.decoder import Decoder
from lora_decoder_config import (
    DECODER_CONFIG,
    MQTT_HOST,
    MQTT_PORT,
    MQTT_TOPIC,
    MQTT_CLIENT_ID,
)


class LoraDecoderPublisher:
    def __init__(self) -> None:
        self.decoder = Decoder(**DECODER_CONFIG)
        self.mqtt_host = MQTT_HOST
        self.mqtt_port = MQTT_PORT
        self.mqtt_topic = MQTT_TOPIC
        self.mqtt_connected = False
        self.mqtt_client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION1,  # type: ignore[attr-defined]
            client_id=MQTT_CLIENT_ID,
        )

        self.mqtt_client.on_connect = self._on_mqtt_connect
        self.mqtt_client.on_disconnect = self._on_mqtt_disconnect

    def _on_mqtt_connect(self, client, userdata, flags, rc):
        self.mqtt_connected = rc == 0
        if self.mqtt_connected:
            print(f"[MQTT] Connected to {self.mqtt_host}:{self.mqtt_port}")
        else:
            print(f"[MQTT] Connection error: {rc}")

    def _on_mqtt_disconnect(self, client, userdata, rc):
        self.mqtt_connected = False
        if rc != 0:
            print(f"[MQTT] Unexpected disconnect: {rc}")

    def start(self) -> None:
        self.decoder.start()
        print("[*] LoRa receiver initialized")
        print("[*] Listening for decoded messages and publishing to MQTT")

    def stop(self) -> None:
        self.decoder.stop()
        try:
            self.mqtt_client.loop_stop()
        finally:
            if self.mqtt_connected:
                self.mqtt_client.disconnect()

    def connect_mqtt(self) -> None:
        try:
            self.mqtt_client.connect(self.mqtt_host, self.mqtt_port, keepalive=60)
            self.mqtt_client.loop_start()
        except Exception as exc:
            print(f"[MQTT] No se pudo conectar: {exc}")
            print("[WARN] Continuando sin MQTT; solo se procesarán mensajes localmente")

    def publish_message(self, message: str) -> None:
        timestamp = datetime.now().isoformat()
        print(f"[RECEIVED {timestamp}] {message}")

        if not self.mqtt_connected:
            return

        payload = message
        msg_info = self.mqtt_client.publish(
            self.mqtt_topic, payload, qos=1
        )
        if msg_info.rc != mqtt.MQTT_ERR_SUCCESS:
            print(
                f"[MQTT] Publish error: rc={msg_info.rc}, mid={msg_info.mid}, topic={self.mqtt_topic}"
            )
            return

        msg_info.wait_for_publish(timeout=5)
        if not msg_info.is_published():
            print(
                f"[MQTT] Publish not confirmed after 5s: mid={msg_info.mid}, topic={self.mqtt_topic}"
            )
            return

        print(
            f"[PUBLISHED] {message} -> {self.mqtt_topic} (rc={msg_info.rc}, mid={msg_info.mid})"
        )

    def run(self) -> None:
        self.connect_mqtt()
        self.start()

        processed_messages = 0

        try:
            while True:
                total_messages = self.decoder.get_total_messages()
                if total_messages > processed_messages:
                    while processed_messages < total_messages:
                        msg = self.decoder.get_message(processed_messages)
                        decoded = self.decoder.preprocess_data(msg)
                        if decoded:
                            self.publish_message(decoded)
                        processed_messages += 1

                time.sleep(0.2)
        except KeyboardInterrupt:
            print("\n[!] Interrupt detected...")
        finally:
            self.stop()


def main() -> None:
    try:
        publisher = LoraDecoderPublisher()
    except RuntimeError as exc:
        if "No RTL-SDR devices found" in str(exc):
            print(
                "[WARN] No RTL-SDR connected; decoder will exit cleanly and systemd will not restart it."
            )
            return
        raise

    def signal_handler(sig, frame):
        publisher.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    publisher.run()


if __name__ == "__main__":
    main()
