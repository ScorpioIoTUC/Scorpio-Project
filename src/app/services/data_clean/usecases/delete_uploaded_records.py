from src.domain.exceptions.app_error import AppError
from src.infra import Database


class DeleteUploadedRecordsUseCase:
    def __init__(self, db: Database):
        self.db = db
        
    async def execute(self) -> None:
        try:
            await self.db.delete_uploaded(uploaded=True)
        except RuntimeError:
            raise AppError.db_operation_failed(
                "Failed to delete uploaded records from DB"
            )
        except ConnectionError:
            raise AppError.db_connection_failed(
                "Failed to connect to DB while deleting uploaded records"
            )
        except Exception as e:
            raise AppError.unknown_error(
                f"An unexpected error occurred while deleting uploaded records: {e}"
            )