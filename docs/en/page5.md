# 5. LoRa decoder and test transmitter

[← Previous](page4.md) | [Contents](README.md)

The LoRa decoder listens for frames, decodes them, and publishes the event to `data_ingest`, which forwards it through the rest of the pipeline.

<figure>
<img src="../imgs/mqtt_topics.png" alt="Message flow through Scorpio MQTT topics">
<figcaption>Figure 3. Data flow through the MQTT topics.</figcaption>
</figure>

The [LoRaTx.ino](../../scripts/LoRaTx.ino) example generates a test payload to validate the full flow on an ESP32 board. It supports Heltec WiFi LoRa 32 (V3), Wireless Shell (V3), and Wireless Stick Lite (V3).

Open the sketch in Arduino IDE and make sure RadioLib is installed:

    #include <RadioLib.h>
