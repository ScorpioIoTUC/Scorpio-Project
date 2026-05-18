from src.infra import MQTT, Logging
import asyncio
from configs.entrypoints import data_ingest as config
from random import choice
import json 

async def main():
    # Initialize the decoder with custom config (optional)
    # Initialize MQTT client
    mqtt_client = MQTT(client_id=config.MQTT_CLIENT_ID)
    logger = Logging(logger_name="entrypoint")
    logger.info("Starting data ingest service...")
    try:
        await mqtt_client.start(host=config.MQTT_HOST, port=config.MQTT_PORT)

        while True:
            # Simulate receiving raw data (replace with actual data source)

            # Preprocess the raw data using the decoder
            packet = {
                "timestamp": "3/22/2025 3:42:48 PM",
                "crc_ok": choice([True, False]),  # Simulate CRC check result
                "lat": 37.7749,
                "lon": -122.4194,
                "alt": 550,
                "starlink_id": "1604",
                "rssi": -113.75,
                "snr": -8.5,
                "frec_error": 10515.13672,
            }
            if not packet["crc_ok"]:
                packet["lat"] = 0
                packet["lon"] = 0
                packet["alt"] = 0
                packet["starlink_id"] = 0
            mock_msg = json.dumps(packet)

            # Publish the preprocessed data to an MQTT topic
            logger.info(f"Publishing to MQTT PUB topic '{config.MQTT_PUB_TOPIC}': {mock_msg}")
            await mqtt_client.publish(
                topic=config.MQTT_PUB_TOPIC,
                payload=mock_msg,
                qos=config.MQTT_QOS,
            )

            await asyncio.sleep(30)  # Simulate delay between data processing
    except Exception as e:
        logger.error(f"Error in data ingest: {e}")
    finally:
        await mqtt_client.end_connection()


if __name__ == "__main__":
    asyncio.run(main())
