import json
from src.infra import Database
from src.domain.exceptions.app_error import AppError


class HandleUploadedUseCase:
    """Mark messages as uploaded when confirmation arrives from the sender."""

    def __init__(self, db: Database):
        self.db = db

    async def execute(self, payload: str) -> dict:
        payload_json = json.loads(payload)
        ids = payload_json.get("ids", [])
        if not ids:
            return {
                "success": False,
                "message": "No IDs found in payload to mark as uploaded",
            }
        try:
            await self.db.update_many(ids=ids, uploaded=True)
        except Exception:
            raise AppError.db_operation_failed(
                "Failed to update messages as uploaded in the database."
            )
        return {
            "success": True,
            "message": f"Marked {len(ids)} messages as uploaded in the database.",
        }
