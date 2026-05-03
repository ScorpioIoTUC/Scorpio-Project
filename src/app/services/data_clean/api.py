from src.infra import Logging, Database
from configs.entrypoints import data_clean as config
from src.app.services.data_clean.controllers import DeleteUploadedRecordsController


class DataCleanAPI:
    def __init__(self):
        # Infrastructure
        self.logger = Logging(logger_name="data_clean.api")
        self.db = Database(db_path=config.SQLITE_DB_PATH)
        # Controllers
        self.delete_uploaded_records_controller = DeleteUploadedRecordsController(
            self.db
        )

    def _parse_response(self, result: dict) -> dict:
        """ Helper to log results in a consistent format. """
        if result["success"]:
            self.logger.info(result["message"])
        else:
            self.logger.error(
                f"{result['error_code']}: {result.get('message')} - {result.get('details', '')}"
            )
        return result

    async def delete_uploaded_records(self):
        """ Delete records marked as 'uploaded' from the database. """
        result = await self.delete_uploaded_records_controller.handle()
        return self._parse_response(result)
