from src.domain.exceptions.app_error import AppError
from src.infra import Logging, HTTP, MQTT
from src.app.services.data_export.usecases.send_pending import SendPendingUseCase


class SendPendingController:
    def __init__(self, mqtt_client: MQTT, http_client: HTTP) -> None:
        self.logger = Logging(logger_name="send_pending")
        self.use_case = SendPendingUseCase(mqtt_client, http_client)

    async def handle(self, uploaded_topic: str, payload: str) -> dict:
        self.logger.info(f"Sending record to Scorpio Server")
        try:
            result = await self.use_case.execute(uploaded_topic, payload)
            return result
        except AppError as e:
            return {"success": False, **e.to_dict()}
