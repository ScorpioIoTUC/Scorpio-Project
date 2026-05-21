from src.app.services.data_export.api import DataExportAPI
from src.infra import Logging
from configs.entrypoints import data_export as config
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


async def flusher(api: DataExportAPI) -> None:
    while True:
        try:
            await asyncio.sleep(config.MAX_TIME_GAP)
            await api.flush_pending()
        except asyncio.CancelledError:
            break
        except Exception as e:
            api.logger.error(f"Error in periodic flush task: {e}")


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
        flusher_task = asyncio.create_task(flusher(api))
        api.logger.info(
            f"Periodic flush interval set to {config.MAX_TIME_GAP} seconds"
        )
        await asyncio.gather(listener_task, flusher_task)
    except Exception as e:
        logger.error(f"Error in data export service: {e}")
    finally:
        if api is not None:
            await api.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
