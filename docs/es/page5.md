# 5. Decodificador LoRa y transmisor de prueba

[← Anterior](page4.md) | [Índice](README.md)

El decodificador LoRa escucha tramas, las decodifica y publica el evento en `data_ingest`, que lo envía al resto del pipeline.

<figure>
<img src="../imgs/mqtt_topics.png" alt="Flujo de mensajes entre los tópicos MQTT de Scorpio">
<figcaption>Figura 3. Flujo de datos a través de los tópicos MQTT.</figcaption>
</figure>

El ejemplo [LoRaTx.ino](../../scripts/LoRaTx.ino) genera un payload de prueba para validar el flujo en una placa ESP32. Es compatible con Heltec WiFi LoRa 32 (V3), Wireless Shell (V3) y Wireless Stick Lite (V3).

Abre el sketch con Arduino IDE y asegúrate de tener instalada RadioLib:

    #include <RadioLib.h>
