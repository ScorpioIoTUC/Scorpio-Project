MQTT_CLIENT_ID = "scorpio_lora_decoder"
MQTT_HOST = "0.0.0.0"
MQTT_PORT = 1883
MQTT_TOPIC = "scorpio/decoded/lora"

DECODER_CONFIG = {
    "samp_rate": 2_000_000,
    "center_freq": 915e6,
    "bw": 250_000,
    "sf": 7,
    "gain": 35,
    "cr": 1,
    "pay_len": 128,
    "sync_word": 0x34,
    "client_name": "gnuradio_client",
}
