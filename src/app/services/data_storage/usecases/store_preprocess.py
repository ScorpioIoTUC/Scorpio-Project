"""Use case for storing preprocess messages in the local backup database."""

from src.domain.exceptions.app_error import AppError
from src.infra import Database


class StorePreprocessUseCase:
    """Store incoming preprocess messages from MQTT topic."""

    def __init__(self, db: Database):
        self.db = db

    async def execute(self, topic: str, payload: str) -> None:
        try:
            await self.db.insert(topic=topic, payload=payload)
        except RuntimeError:
            raise AppError.db_operation_failed(
                "Failed to store preprocess message in DB"
            )
        except ConnectionError:
            raise AppError.db_connection_failed(
                "Failed to connect to DB while storing preprocess message"
            )

        except Exception as e:
            raise AppError.unknown_error(
                f"An unexpected error occurred while storing preprocess message: {e}"
            )
