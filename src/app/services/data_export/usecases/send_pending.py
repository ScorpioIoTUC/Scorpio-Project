from src.infra import MQTT, HTTP
from src.domain.exceptions.app_error import AppError
import json


class SendPendingUseCase:
    def __init__(self, mqtt_client: MQTT, http_client: HTTP) -> None:
        self.mqtt_client = mqtt_client
        self.http_client = http_client
        self.buffer_size = 10  # Number of ids to send in each batch to uplaoded topic.
        self.buffer = []

    async def execute(self, uploaded_topic: str, payload: str) -> dict:
        try:
            # headers = {}
            json_payload = json.loads(payload)
            local_id = json_payload["local_id"]
            if local_id in self.buffer:  # Avoid duplicates in the buffer
                return {
                    "success": True,
                    "message": f"Duplicate local_id '{local_id}' ignored. Current buffer size: {len(self.buffer)}",
                }
            # TODO: Wait until the scorpio service is ready
            # response = await self.http_client.post(headers=headers, json=json_payload)
            # if not response["ok"]:
            #     raise AppError.cloud_send_error(
            #         f"Failed to send record to Scorpio Server: {response.get('payload', 'Unknown error')}"
            #     )
            self.buffer.append(local_id)
            
        except Exception as e:
            raise AppError.unknown_error(
                f"An unexpected error occurred while storing preprocess message: {e}"
            )
        if len(self.buffer) >= self.buffer_size:
            batch_payload = json.dumps({"ids": self.buffer})
            try:
                await self.mqtt_client.publish(
                    uploaded_topic, payload=batch_payload, qos=0
                )
                self.buffer.clear()  # Clear the buffer after successful publish
                return {
                    "success": True,
                    "message": f"Published batch of {self.buffer_size} ids to '{uploaded_topic}'",
                }
            except Exception as e:
                raise AppError.publish_error(
                    f"Failed to publish batch to MQTT topic {uploaded_topic}: {e}"
                )
        else:
            return {
                "success": True,
                "message": f"Added id to buffer. Current buffer size: {len(self.buffer)}",
            }
