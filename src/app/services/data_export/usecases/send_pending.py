from src.infra import MQTT, HTTP
from src.domain.exceptions.app_error import AppError
import asyncio
import json


class SendPendingUseCase:
    def __init__(self, mqtt_client: MQTT, http_client: HTTP) -> None:
        self.mqtt_client = mqtt_client
        self.http_client = http_client
        self.buffer_size = 10  # Number of ids to send in each batch to uplaoded topic.
        self.buffer = []
        self._lock = asyncio.Lock()  # To ensure thread-safe access to the buffer

    async def execute(self, uploaded_topic: str, payload: str) -> dict:
        json_payload = json.loads(payload)
        local_id = json_payload["local_id"]
        async with self._lock:
            if local_id in self.buffer:  # Avoid duplicates in the buffer
                return {
                    "success": False,
                    "message": f"Duplicate local_id '{local_id}' ignored",
                }
            self.buffer.append(local_id)
            if len(self.buffer) < self.buffer_size:
                return {
                    "success": True,
                    "message": f"Added id to buffer. Current buffer size: {len(self.buffer)}",
                }
            # Atomic snapshot before publishing
            batch_ids = self.buffer[:]
            self.buffer.clear()
        try:
            batch_payload = json.dumps({"ids": batch_ids})
            # TODO: Wait until the scorpio service is ready
            # response = await self.http_client.post(headers=headers, json=json_payload)
            # if not response["ok"]:
            #     raise AppError.cloud_send_error(
            #         f"Failed to send record to Scorpio Server: {response.get('payload', 'Unknown error')}"
            #     )
            await self.mqtt_client.publish(uploaded_topic, payload=batch_payload, qos=0)
            return {
                "success": True,
                "message": f"Published batch of {len(batch_ids)} ids to '{uploaded_topic}'",
            }
        except Exception as e:
            # If publish fails, we should re-add the batch_ids back to the buffer
            async with self._lock:
                self.buffer = (
                    batch_ids + self.buffer
                )  # Re-add failed batch to the front of the buffer
            raise AppError.publish_error(
                f"Failed to publish batch to MQTT topic {uploaded_topic}: {e}"
            )
