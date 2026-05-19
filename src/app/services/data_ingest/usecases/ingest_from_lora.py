from src.infra import MQTT
from src.domain.exceptions.app_error import AppError
import configs.entrypoints.data_ingest as config


class IngestFromLoraUseCase:
    def __init__(self, mqtt_client: MQTT) -> None:
        self.mqtt_client = mqtt_client

    async def execute(self, payload: str) -> dict:
        try:
            # publish message to decode/lora topic
            await self.mqtt_client.publish(
                topic=config.MQTT_PUB_TOPIC_1,
                payload=payload,
                qos=config.MQTT_PUB_TOPIC_1_QOS,
                retain=config.RETAIN,
            )
            return {
                "success": True,
                "message": "Message ingested and published successfully",
            }
        except Exception as e:
            raise AppError.lora_decoder_error(details=str(e))
