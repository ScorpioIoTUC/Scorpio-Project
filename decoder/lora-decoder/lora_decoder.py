#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import signal
import sys
import time
from datetime import datetime

import paho.mqtt.client as mqtt

from decoder.libs.decoder import Decoder
from .lora_decoder_config import (
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
        self.mqtt_client = mqtt.Client(client_id=MQTT_CLIENT_ID)

        self.mqtt_client.on_connect = self._on_mqtt_connect
        self.mqtt_client.on_disconnect = self._on_mqtt_disconnect

    def _on_mqtt_connect(self, client, userdata, flags, rc, properties=None):
        self.mqtt_connected = rc == 0
        if self.mqtt_connected:
            print(f"[MQTT] Conectado a {self.mqtt_host}:{self.mqtt_port}")
        else:
            print(f"[MQTT] Error de conexión: {rc}")

    def _on_mqtt_disconnect(self, client, userdata, rc, properties=None):
        self.mqtt_connected = False
        if rc != 0:
            print(f"[MQTT] Desconexión inesperada: {rc}")

    def start(self) -> None:
        self.decoder.start()
        print("[*] Receptor LoRa inicializado")
        print("[*] Escuchando mensajes decodificados y publicando en MQTT")

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
        print(f"[RECIBIDO] {message}")

        if not self.mqtt_connected:
            return

        payload = {"timestamp": timestamp, "message": message}
        self.mqtt_client.publish(self.mqtt_topic, json.dumps(payload), qos=1)
        print(f"[PUBLISHED] {message} -> {self.mqtt_topic}")

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
            print("\n[!] Interrupción detectada...")
        finally:
            self.stop()


def main() -> None:
    publisher = LoraDecoderPublisher()

    def signal_handler(sig, frame):
        publisher.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    publisher.run()


if __name__ == "__main__":
    main()
