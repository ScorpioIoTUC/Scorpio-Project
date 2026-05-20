#include <RadioLib.h>

// Heltec WiFi LoRa 32 V3 (SX1262)
SX1262 radio = new Module(8, 14, 12, 13);

#define RF_FREQUENCY          915.0
#define LORA_BANDWIDTH        250.0
#define LORA_SPREADING_FACTOR 7
#define LORA_CODINGRATE       5
#define TX_OUTPUT_POWER       5

char txpacket[256];

void setup() {
  Serial.begin(115200);

  Serial.println("Inicializando LoRa...");

  int state = radio.begin(
    RF_FREQUENCY,
    LORA_BANDWIDTH,
    LORA_SPREADING_FACTOR,
    LORA_CODINGRATE,
    0x34,
    TX_OUTPUT_POWER,
    8
  );

  if(state == RADIOLIB_ERR_NONE) {
    Serial.println("LoRa inicializado correctamente");
  } else {
    Serial.print("Error inicializando LoRa: ");
    Serial.println(state);
    while(true);
  }
}

void loop() {

  const char* satelliteId = "1604";
  bool crcOk = true;
  double latitude = 37.7749;
  double longitude = -122.4194;
  double altitude = 550.0;
  double rssi = -113.75;
  double snr = -8.5;
  double freqError = 10515.13672;

  snprintf(
    txpacket,
    sizeof(txpacket),
    "{\"starlink_id\":\"%s\",\"crc_ok\":%s,\"lat\":%.4f,\"lon\":%.4f,\"alt\":%.1f,\"rssi\":%.2f,\"snr\":%.1f,\"freq_error\":%.5f}",
    satelliteId,
    crcOk ? "true" : "false",
    latitude,
    longitude,
    altitude,
    rssi,
    snr,
    freqError
  );

  Serial.println("Enviando paquete:");
  Serial.println(txpacket);

  int state = radio.transmit(txpacket);

  if(state == RADIOLIB_ERR_NONE) {
    Serial.println("TX OK");
  } else {
    Serial.print("TX Error: ");
    Serial.println(state);
  }

  delay(30000);
}