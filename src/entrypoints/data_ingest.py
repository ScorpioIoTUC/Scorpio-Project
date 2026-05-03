from src.infra import MQTT, Logging
import asyncio
from configs.entrypoints import data_ingest as config

async def main():
    # Initialize the decoder with custom config (optional)
    # Initialize MQTT client
    mqtt_client = MQTT(client_id=config.MQTT_CLIENT_ID)
    logger = Logging(logger_name="data_ingest")
    logger.info("Starting data ingest service...")
    try:
        await mqtt_client.start(host=config.MQTT_HOST, port=config.MQTT_PORT)

        while True:
            # Simulate receiving raw data (replace with actual data source)

            # Preprocess the raw data using the decoder
            mock_msg = (
                "Mock PMT message from GNU Radio"  # Replace with actual PMT message
            )

            # Publish the preprocessed data to an MQTT topic
            logger.info(f"Publishing to MQTT PUB topic '{config.MQTT_PUB_TOPIC}': {mock_msg}")
            await mqtt_client.publish(
                topic=config.MQTT_PUB_TOPIC,
                payload=mock_msg,
                qos=config.MQTT_QOS,
            )

            await asyncio.sleep(15)  # Simulate delay between data processing
    except Exception as e:
        logger.error(f"Error in data ingest: {e}")
    finally:
        await mqtt_client.end_connection()


if __name__ == "__main__":
    asyncio.run(main())
