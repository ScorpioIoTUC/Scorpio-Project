from src.infra import MQTT, Logging, HTTP
from configs.entrypoints import data_export as config
from .controllers import SendPendingController


class DataExportAPI:
    def __init__(self) -> None:
        # Infrastructure
        self.mqtt_client = MQTT(config.MQTT_CLIENT_ID)
        self.mqtt_host = config.MQTT_HOST
        self.mqtt_port = config.MQTT_PORT
        self.logger = Logging(logger_name="api")
        self.http_client = HTTP(url=config.API_URL, credentials=config.CREDENTIALS)
        # Controllers
        self.send_pending_controller = SendPendingController(
            self.mqtt_client, self.http_client
        )

    def _parse_response(self, result: dict) -> dict:
        if result["success"]:
            self.logger.info(result["message"])
        else:
            self.logger.error(
                f"{result['error_code']}: {result.get('message')} - {result.get('details', '')}"
            )
        return result

    async def configure(self) -> None:
        try:
            # Connect to MQTT broker
            await self.mqtt_client.start(host=self.mqtt_host, port=self.mqtt_port)
            self.logger.info("Connected to MQTT broker")
            # Subscribe to topics
            await self.mqtt_client.subscribe(
                topic=config.TOPIC_SEND, qos=config.TOPIC_SEND_QOS
            )
            self.logger.info(f"Subscribed to {config.TOPIC_SEND}")
        except Exception as e:
            self.logger.error(f"Error during MQTT configuration: {e}")
            raise

    async def handle_message(self, topic: str, payload: str) -> dict:
        if topic == config.TOPIC_SEND:
            self.logger.debug(f"Received message on topic '{config.TOPIC_SEND}'")
            result = await self.send_pending_controller.handle(
                uploaded_topic=config.TOPIC_UPLOADED, payload=payload
            )
        else:
            self.logger.warning(f"Received message on unhandled topic: {topic}")
            return {"success": False, "error": f"Unknown topic: {topic}"}
        return self._parse_response(result)

    async def flush_pending(self) -> dict:
        result = await self.send_pending_controller.flush_pending(
            uploaded_topic=config.TOPIC_UPLOADED
        )
        return self._parse_response(result)

    async def shutdown(self) -> None:
        try:
            await self.mqtt_client.end_connection()
            self.logger.info("Data export service stopped")
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
