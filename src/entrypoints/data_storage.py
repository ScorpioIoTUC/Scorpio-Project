from src.app.services.data_storage import DataStorageAPI
from configs.entrypoints import data_storage as config
import asyncio
import os

MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", config.MQTT_CLIENT_ID)
MQTT_HOST = os.getenv("MQTT_HOST", config.MQTT_HOST)
MQTT_PORT = int(os.getenv("MQTT_PORT", config.MQTT_PORT))
DB_PATH = os.getenv("DB_PATH", "data/local_backup.db")
PUBLISH_INTERVAL = int(os.getenv("PUBLISH_INTERVAL", config.PUBLISH_INTERVAL))


async def publisher(
    api: DataStorageAPI, interval: int = config.PUBLISH_INTERVAL
) -> None:
    """Periodically publish pending messages to MQTT broker.
    """
    while True:
        try:
            await asyncio.sleep(interval)
            await api.publish_pending(config.TOPIC_SEND)
            # Result already logged by controller
        except asyncio.CancelledError:
            break
        except Exception as e:
            api.logger.error(f"Error in periodic publish task: {e}")


async def listener(api: DataStorageAPI) -> None:
    """Listen for MQTT messages and route to appropriate handler.
    """
    loop = asyncio.get_running_loop()

    def handle_message(topic: str, payload: str) -> None:
        """Synchronous callback from MQTT library."""
        # Schedule async handler in the event loop
        coro = api.handle_message(topic, payload)
        asyncio.run_coroutine_threadsafe(coro, loop)

    # Register the message callback
    api.mqtt_client.set_message_callback(handle_message)
    api.logger.info("Message listener registered")

    # Keep listening (infinite loop)
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass


async def main() -> None:
    api = DataStorageAPI()
    api.logger.info("Starting data storage service...")
    try:
        await api.configure()
        api.logger.info("Service configured successfully")
        # Create tasks
        listener_task = asyncio.create_task(listener(api))
        publish_task = asyncio.create_task(publisher(api))
        api.logger.info(f"Periodic publish interval set to {PUBLISH_INTERVAL} seconds")
        # Wait for either task to fail (they should run forever..)
        await asyncio.gather(listener_task, publish_task)
    except Exception as e:
        api.logger.error(f"Error in data storage service: {e}")
    finally:
        await api.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
