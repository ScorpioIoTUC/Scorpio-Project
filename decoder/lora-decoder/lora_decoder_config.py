MQTT_CLIENT_ID = "scorpio_data_ingest"
MQTT_HOST = "mqtt"
MQTT_PORT = 1883
MQTT_TOPIC = "scorpio/decoded/lora"

DECODER_CONFIG = {
    "samp_rate": 1_000_000,
    "center_freq": 915e6,
    "bw": 250_000,
    "sf": 7,
    "gain": 5,
    "cr": 1,
    "pay_len": 64,
    "sync_word": 0x12,
    "client_name": "gnuradio_client",
}
