from src.app.services.data_storage import DataStorageAPI
from configs.entrypoints import data_storage as config
from src.infra import Logging
import asyncio


async def publisher(
    api: DataStorageAPI, interval: int = config.PUBLISH_INTERVAL
) -> None:
    """Periodically publish pending messages to MQTT broker."""
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
    """Listen for MQTT messages and route to appropriate handler."""
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
    logger = Logging(logger_name="entrypoint")
    api = None
    try:
        api = DataStorageAPI()
        logger.info("Starting data storage service...")
        await api.configure()
        api.logger.info("Service configured successfully")
        # Create tasks
        listener_task = asyncio.create_task(listener(api))
        publish_task = asyncio.create_task(publisher(api))
        api.logger.info(
            f"Periodic publish interval set to {config.PUBLISH_INTERVAL} seconds"
        )
        # Wait for either task to fail (they should run forever..)
        await asyncio.gather(listener_task, publish_task)
    except Exception as e:
        logger.error(f"Error in data storage service: {e}")
    finally:
        if api is not None:
            await api.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
