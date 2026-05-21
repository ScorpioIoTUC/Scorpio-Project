from src.infra import MQTT, HTTP
from src.infra.zero_dependency import DateTimeUtils as dt
from src.domain.exceptions.app_error import AppError
import asyncio
import json
import configs.entrypoints.data_export as config


class SendPendingUseCase:
    def __init__(self, mqtt_client: MQTT, http_client: HTTP) -> None:
        self.mqtt_client = mqtt_client
        self.http_client = http_client
        self.buffer_size = config.BUFFER_SIZE
        self.buffer = []
        self._lock = asyncio.Lock()  # To ensure thread-safe access to the buffer
        self._buffer_started_at = None

    async def execute(self, uploaded_topic: str, payload: str) -> dict:
        json_payload = json.loads(payload)
        local_id = json_payload["local_id"]
        current_time = dt.now()
        async with self._lock:
            if local_id in self.buffer:  # Avoid duplicates in the buffer
                raise AppError.duplicated_local_id(
                    f"Local ID '{local_id}' is already in the buffer"
                )
            buffer_was_empty = not self.buffer
            self.buffer.append(local_id)
            if buffer_was_empty:
                self._buffer_started_at = current_time
            buffer_started_at = self._buffer_started_at or current_time
            buffer_full = len(self.buffer) >= self.buffer_size
            time_gap_reached = (
                dt.diff_seconds(buffer_started_at, current_time) >= config.MAX_TIME_GAP
            )
            if not buffer_full and not time_gap_reached:
                return {
                    "success": True,
                    "message": f"Added id to buffer. Current buffer size: {len(self.buffer)}",
                }
            # Atomic snapshot before publishing
            batch_ids = self.buffer[:]
            batch_started_at = self._buffer_started_at
            self.buffer.clear()
            self._buffer_started_at = None

        return await self._publish_batch(
            uploaded_topic=uploaded_topic,
            batch_ids=batch_ids,
            batch_started_at=batch_started_at,
            action_message="Published",
        )

    async def flush_pending(self, uploaded_topic: str) -> dict:
        current_time = dt.now()
        async with self._lock:
            if not self.buffer or not self._buffer_started_at:
                return {
                    "success": True,
                    "message": "No pending ids to flush",
                }

            time_gap_reached = (
                dt.diff_seconds(self._buffer_started_at, current_time)
                >= config.MAX_TIME_GAP
            )
            if not time_gap_reached:
                return {
                    "success": True,
                    "message": f"Pending ids still waiting in buffer. Current buffer size: {len(self.buffer)}",
                }

            batch_ids = self.buffer[:]
            batch_started_at = self._buffer_started_at
            self.buffer.clear()
            self._buffer_started_at = None

        return await self._publish_batch(
            uploaded_topic=uploaded_topic,
            batch_ids=batch_ids,
            batch_started_at=batch_started_at,
            action_message="Flushed",
        )

    async def _publish_batch(
        self,
        uploaded_topic: str,
        batch_ids: list,
        batch_started_at,
        action_message: str,
    ) -> dict:
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
                "message": f"{action_message} batch of {len(batch_ids)} ids to '{uploaded_topic}'",
            }
        except Exception as e:
            # If publish fails, we should re-add the batch_ids back to the buffer
            async with self._lock:
                # Re-add failed batch to the front of the buffer
                self.buffer = batch_ids + self.buffer
                self._buffer_started_at = batch_started_at
            raise AppError.publish_error(
                f"Failed to publish batch to MQTT topic {uploaded_topic}: {e}"
            )
