import asyncio
import json

from src.app.services.data_ingest.api import DataIngestAPI
from src.infra import Logging


async def listener(api: DataIngestAPI) -> None:
    loop = asyncio.get_running_loop()

    def handle_message(topic: str, payload: str) -> None:
        try:
            parsed_payload = json.loads(payload)
        except (TypeError, json.JSONDecodeError):
            parsed_payload = payload
        event = {"topic": topic, "payload": parsed_payload}
        api.logger.info(
            f"MQTT message received: {json.dumps(event, ensure_ascii=False, separators=(',', ':'))}"
        )
        future = asyncio.run_coroutine_threadsafe(
            api.handle_message(topic, payload), loop
        )

        def log_future_result(done_future):
            try:
                done_future.result()
            except Exception as exc:
                api.logger.error(f"Error handling MQTT message: {exc}")

        future.add_done_callback(log_future_result)

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
        api = DataIngestAPI()
        logger.info("Starting data ingest service...")
        await api.configure()
        logger.info("Service configured successfully")
        # Create tasks
        listener_task = asyncio.create_task(listener(api))
        await asyncio.gather(listener_task)
    except Exception as e:
        logger.error(f"Error in data ingest service: {e}")
    finally:
        if api is not None:
            await api.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
