from src.infra import MQTT, Logging
import asyncio
import os
from configs.entrypoints import data_ingest as config

MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", config.CLIENT_ID)
MQTT_HOST = os.getenv("MQTT_HOST", config.MQTT_BROKER)
MQTT_PORT = int(os.getenv("MQTT_PORT", config.MQTT_PORT))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", config.TOPIC)
MQTT_QOS = int(os.getenv("MQTT_QOS", config.QOS))


async def main():
    # Initialize the decoder with custom config (optional)
    # Initialize MQTT client
    mqtt_client = MQTT(client_id=MQTT_CLIENT_ID)
    logger = Logging(logger_name="data_ingest")
    logger.info("Starting data ingest service...")
    try:
        await mqtt_client.start(host=MQTT_HOST, port=MQTT_PORT)

        while True:
            # Simulate receiving raw data (replace with actual data source)

            # Preprocess the raw data using the decoder
            mock_msg = (
                "Mock PMT message from GNU Radio"  # Replace with actual PMT message
            )

            # Publish the preprocessed data to an MQTT topic
            logger.info(f"Publishing to MQTT topic '{MQTT_TOPIC}': {mock_msg}")
            await mqtt_client.publish(
                topic=MQTT_TOPIC,
                payload=mock_msg,
                qos=MQTT_QOS,
            )

            await asyncio.sleep(5)  # Simulate delay between data processing
    except Exception as e:
        logger.error(f"Error in data ingest: {e}")
    finally:
        await mqtt_client.end_connection()


if __name__ == "__main__":
    asyncio.run(main())
