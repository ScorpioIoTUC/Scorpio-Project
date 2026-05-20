from src.domain.exceptions.app_error import AppError
from src.infra import Logging, MQTT
from src.app.services.data_ingest.usecases.ingest_from_lora import IngestFromLoraUseCase
import configs.entrypoints.data_ingest as config


class IngestFromLoraController:
    def __init__(self, mqtt_client: MQTT) -> None:
        self.logger = Logging("ingest_from_lora")
        self.mqtt_client = mqtt_client
        self.use_case = IngestFromLoraUseCase(mqtt_client)

    async def handle(self, payload: str) -> dict:
        self.logger.info(f"Processing message from '{config.MQTT_SUB_TOPIC_1}'")
        try:
            result = await self.use_case.execute(payload)
            self.logger.info("Message ingested and published successfully")
            return result
        except AppError as e:
            self.logger.error(f"Error occurred while processing message: {e}")
            return {"success": False, **e.to_dict()}
