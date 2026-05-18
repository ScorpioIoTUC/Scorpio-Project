from src.infra import MQTT, Logging
from configs.entrypoints import data_preprocess as config
from .controllers import PreprocessSatDataController


class DataPreprocessAPI:
    def __init__(self) -> None:
        # Infrastructure
        self.mqtt_client = MQTT(config.MQTT_CLIENT_ID)
        self.mqtt_host = config.MQTT_HOST
        self.mqtt_port = config.MQTT_PORT
        self.logger = Logging(logger_name="api")
        # Controllers
        self.preprocess_sat_data_controller = PreprocessSatDataController(
            self.mqtt_client
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
                topic=config.MQTT_SUB_TOPIC_1, qos=config.MQTT_SUB_TOPIC_1_QOS
            )
            self.logger.info(f"Subscribed to {config.MQTT_SUB_TOPIC_1}")
        except Exception as e:
            self.logger.error(f"Error during MQTT configuration: {e}")
            raise

    async def handle_message(self, topic: str, payload: str) -> dict:
        if topic == config.MQTT_SUB_TOPIC_1:
            self.logger.info(f"Received message on topic '{config.MQTT_SUB_TOPIC_1}'")
            result = await self.preprocess_sat_data_controller.handle(payload)
        else:
            self.logger.warning(f"Received message on unhandled topic: {topic}")
            return {"success": False, "error": f"Unknown topic: {topic}"}
        return self._parse_response(result)

    async def shutdown(self) -> None:
        try:
            await self.mqtt_client.end_connection()
            self.logger.info("Data export service stopped")
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
