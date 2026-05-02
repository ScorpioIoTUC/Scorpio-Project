"""Controller for publishing pending messages periodically."""

from src.app.services.data_storage.usecases.publish_pending import PublishPendingUseCase
from src.domain.exceptions.app_error import AppError
from src.infra import Logging, Database, MQTT


class PublishPendingController:
    """Handle periodic publishing of pending messages."""

    def __init__(self, db: Database, logger: Logging, mqtt_client: MQTT):
        self.logger = logger
        self.use_case = PublishPendingUseCase(db, mqtt_client)

    async def handle(self, target_topic: str) -> dict:
        self.logger.debug(f"Publishing pending messages to {target_topic}")
        try:
            result = await self.use_case.execute(target_topic)
            return result
        except AppError as e:
            return {
                "success": False,
                **e.to_dict(),
            }
