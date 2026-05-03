"""Controller for storing preprocess messages."""

from src.app.services.data_storage.usecases.store_preprocess import (
    StorePreprocessUseCase,
)
from src.domain.exceptions.app_error import AppError
from src.infra import Database, Logging


class StorePreprocessController:
    """Handle preprocess messages: validate input and execute use case."""

    def __init__(self, db: Database):
        self.logger = Logging(logger_name='store_preprocess')
        self.use_case = StorePreprocessUseCase(db)

    async def handle(self, topic: str, payload: str) -> dict:
        self.logger.info(f"Handling preprocess message from {topic}")
        try:
            await self.use_case.execute(topic, payload)
            return {
                "success": True,
                "message": "Preprocess message stored successfully",
            }
        except AppError as e:
            return {"success": False, **e.to_dict()}
