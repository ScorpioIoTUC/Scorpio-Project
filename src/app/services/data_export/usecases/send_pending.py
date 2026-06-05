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
        data = json.loads(json_payload["payload"])
        current_time = dt.now()
        async with self._lock:
            buffer_ids = [item[0] for item in self.buffer]
            if local_id in buffer_ids:  # Avoid duplicates in the buffer
                raise AppError.duplicated_local_id(
                    f"Local ID '{local_id}' is already in the buffer"
                )
            buffer_was_empty = not self.buffer
            self.buffer.append((local_id, data))
            if buffer_was_empty:
                self._buffer_started_at = current_time
            # Last time update
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
            buffer_items = self.buffer[:]
            batch_started_at = self._buffer_started_at
            self.buffer.clear()
            self._buffer_started_at = None

        return await self._publish_batch(
            uploaded_topic=uploaded_topic,
            buffer_items=buffer_items,
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

            buffer_items = self.buffer[:]
            batch_started_at = self._buffer_started_at
            self.buffer.clear()
            self._buffer_started_at = None

        return await self._publish_batch(
            uploaded_topic=uploaded_topic,
            buffer_items=buffer_items,
            batch_started_at=batch_started_at,
            action_message="Flushed",
        )

    async def _publish_batch(
        self,
        uploaded_topic: str,
        buffer_items: list[tuple],
        batch_started_at,
        action_message: str,
    ) -> dict:
        try:
            batch_payloads = [item[1] for item in buffer_items]
            batch_ids = json.dumps({"ids": [item[0] for item in buffer_items]})
            json_payload: dict
            uploaded_to_server = 0
            for json_payload in batch_payloads:
                data = {
                    "noradId": json_payload.get("noradId"),
                    "latitude": json_payload.get("latitude"),
                    "longitude": json_payload.get("longitude"),
                    "altitude": json_payload.get("altitude"),
                    "rssi": json_payload.get("rssi"),
                    "snr": json_payload.get("snr"),
                    "slantDistance": json_payload.get("slantDistance"),
                    "elevationAngle": json_payload.get("elevationAngle"),
                    "frequencyError": json_payload.get("frequencyError"),
                    "crc": json_payload.get("crc"),
                    "rawPayload": json_payload.get("rawPayload"),
                }
                response = await self.http_client.post(json=data)
                if not response["ok"]:
                    raise AppError.cloud_send_error(
                        f"Failed to send record to Scorpio Server: {response.get('payload', 'Unknown error')}"
                    )
                uploaded_to_server += 1
            msg_server = f"{action_message} batch of {uploaded_to_server} payloads to Scorpio Server"
            msg_mqtt = f"{action_message} batch of {len(buffer_items)} ids to '{uploaded_topic}'"
            await self.mqtt_client.publish(uploaded_topic, payload=batch_ids, qos=0)
            return {
                "success": True,
                "message": f"{msg_server}. {msg_mqtt}",
            }
        except Exception as e:
            # If publish fails, we should re-add the batch_ids back to the buffer
            async with self._lock:
                # Re-add failed batch to the front of the buffer
                self.buffer = buffer_items + self.buffer
                self._buffer_started_at = batch_started_at
            raise AppError.publish_error(f"Failed to publish batch : {e}")
