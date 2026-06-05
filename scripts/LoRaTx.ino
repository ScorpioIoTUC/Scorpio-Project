#include <RadioLib.h>

// Heltec WiFi LoRa 32 V3 (SX1262)
SX1262 radio = new Module(8, 14, 12, 13);

#define RF_FREQUENCY          915.0
#define LORA_BANDWIDTH        250.0
#define LORA_SPREADING_FACTOR 7
#define LORA_CODINGRATE       5
#define TX_OUTPUT_POWER       5

char txpacket[512];

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

  uint32_t noradId = 32783;

  double latitude = -33.4489;
  double longitude = -70.6693;
  double altitude = 692.4;

  int rssi = -118;
  double snr = 7.3;

  double slantDistance = 1245.8;
  double elevationAngle = 42.7;

  int frequencyError = -185;

  bool crc = true;

  const char* rawPayload =
      "Q0FSVE9TQVQtMkF8VEVMRU1FVFJZfDE3NDkwNjYwMDA=";

  snprintf(
    txpacket,
    sizeof(txpacket),
    "{\"noradId\":%lu,"
    "\"latitude\":%.4f,"
    "\"longitude\":%.4f,"
    "\"altitude\":%.1f,"
    "\"rssi\":%d,"
    "\"snr\":%.1f,"
    "\"slantDistance\":%.1f,"
    "\"elevationAngle\":%.1f,"
    "\"frequencyError\":%d,"
    "\"crc\":%s,"
    "\"rawPayload\":\"%s\"}",
    noradId,
    latitude,
    longitude,
    altitude,
    rssi,
    snr,
    slantDistance,
    elevationAngle,
    frequencyError,
    crc ? "true" : "false",
    rawPayload
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

  long randomDelay = random(500, 2001);

  Serial.print("Delay: ");
  Serial.println(randomDelay);

  delay(randomDelay);
}