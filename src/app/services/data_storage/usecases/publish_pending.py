"""Use case for publishing pending messages every 30 seconds."""

import json
from src.infra import MQTT, Database
from src.domain.exceptions.app_error import AppError


class PublishPendingUseCase:
    """Periodically read pending messages from local backup and publish them."""

    def __init__(self, db: Database, mqtt_client: MQTT):
        self.db = db
        self.mqtt_client = mqtt_client

    async def execute(self, target_topic: str) -> dict:
        # Fetch all messages not yet uploaded
        try:
            result = await self.db.find_all(uploaded=False)
        except RuntimeError:
            raise AppError.db_operation_failed(
                "Failed to fetch pending messages from DB"
            )
        except ConnectionError:
            raise AppError.db_connection_failed(
                "Failed to connect to DB while fetching pending messages"
            )

        rows = result if isinstance(result, list) else []

        if not rows:
            return {
                "success": True,
                "message": "No pending messages to publish",
                "data": {"published_count": 0},
            }
        published_count = 0
        max_error_count = 10
        last_error = None
        for row in rows:
            if max_error_count <= 0:
                raise AppError.too_many_publish_errors(
                    f"Too many errors while publishing pending messages: {last_error}"
                )
            try:
                message = {
                    "local_id": row.get("id") if isinstance(row, dict) else row[0],
                    "topic": row.get("topic") if isinstance(row, dict) else row[1],
                    "payload": row.get("payload") if isinstance(row, dict) else row[2],
                }
                await self.mqtt_client.publish(
                    topic=target_topic,
                    payload=json.dumps(message),
                    qos=1,
                )
                published_count += 1
            except Exception as e:
                max_error_count -= 1
                last_error = e
                continue

        return {
            "success": True,
            "message": f"Published {published_count} pending messages",
            "data": {"published_count": published_count},
        }
