## Decoder

The LoRa decoder is the first input component of the flow. It listens to LoRa frames, decodes them, and publishes the resulting event to `data_ingest`, which then forwards it through the rest of the pipeline shown in the diagram.

![MQTT topics flow](/docs/imgs/mqtt_topics.png)




The example transmitter is in [LoRaTx.ino](LoRaTx.ino). It generates a sample payload so you can test the full flow on an ESP32 board. The sketch is intended to be configurable for Heltec WiFi LoRa 32 (V3), Wireless Shell (V3), and Wireless Stick Lite (V3).

Use the Arduino IDE with RadioLib installed:

```cpp
#include <RadioLib.h>
```