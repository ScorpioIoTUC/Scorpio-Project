from src.app.services.data_clean.usecases.delete_uploaded_records import (
    DeleteUploadedRecordsUseCase,
)
from src.infra import Logging, Database
from src.domain.exceptions.app_error import AppError

class DeleteUploadedRecordsController:
    def __init__(self, db: Database, logger: Logging):
        self.logger = logger
        self.use_case = DeleteUploadedRecordsUseCase(db, logger)

    async def handle(self) -> dict:
        self.logger.debug("Deleting uploaded records from the database")
        try:
            result = await self.use_case.execute()
            return result
        except AppError as e:
            return {
                "success": False,
                **e.to_dict(),
            }
