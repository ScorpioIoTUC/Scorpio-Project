"""Controller for handling uploaded messages."""

from src.app.services.data_storage.usecases.handle_uploaded import HandleUploadedUseCase
from src.infra import Logging, Database
from src.domain.exceptions.app_error import AppError


class HandleUploadedController:
    """Handle uploaded confirmation messages: validate input and execute use case."""

    def __init__(self, db: Database, logger: Logging):
        self.logger = logger
        self.use_case = HandleUploadedUseCase(db)

    async def handle(self, topic: str, payload: str) -> dict:
        self.logger.info(f"Handling uploaded confirmation from {topic}")
        try:
            result = await self.use_case.execute(payload)
            return result
        except AppError as e:
            return {
                "success": False,
                **e.to_dict(),
            }
