from src.app.services.data_export.api import DataExportAPI
from src.infra import Logging
import asyncio


async def listener(api: DataExportAPI) -> None:
    loop = asyncio.get_running_loop()

    def handle_message(topic: str, payload: str) -> None:
        coro = api.handle_message(topic, payload)
        asyncio.run_coroutine_threadsafe(coro, loop)

    api.mqtt_client.set_message_callback(handle_message)
    api.logger.info("Message listener registered")
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass


async def main() -> None:
    logger = Logging(logger_name="entrypoint")
    api = None
    try:
        api = DataExportAPI()
        logger.info("Starting data export service...")
        await api.configure()
        api.logger.info("Service configured successfully")
        # Create tasks
        listener_task = asyncio.create_task(listener(api))
        await asyncio.gather(listener_task)
    except Exception as e:
        logger.error(f"Error in data export service: {e}")
    finally:
        if api is not None:
            await api.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
