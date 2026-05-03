from src.domain.exceptions.app_error import AppError
from src.infra import Database


class DeleteUploadedRecordsUseCase:
    def __init__(self, db: Database):
        self.db = db

    async def execute(self) -> dict:
        try:
            await self.db.delete_uploaded(uploaded=True)
            non_uploaded_records = await self.db.find_all(uploaded=False)
            non_uploaded_count = len(non_uploaded_records) # type: ignore
            return {
                "success": True,
                "message": f"Uploaded records deleted successfully. Remaining non-uploaded records: {non_uploaded_count}",
            }
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