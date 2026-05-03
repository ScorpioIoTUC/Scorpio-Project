"""DataStorageAPI - Main service API that coordinates all operations."""

from src.infra import MQTT, Logging, Database
from configs.entrypoints import data_storage as config
from src.app.services.data_storage.controllers import (
    StorePreprocessController,
    HandleUploadedController,
    PublishPendingController,
)


class DataStorageAPI:
    """Facade that provides high-level operations for data storage service."""

    def __init__(self) -> None:
        # Infrastructure
        self.mqtt_client = MQTT(config.MQTT_CLIENT_ID)
        self.logger = Logging(logger_name="data_storage.api")
        self.db = Database(db_path=config.SQLITE_DB_PATH)
        self.mqtt_host = config.MQTT_HOST
        self.mqtt_port = config.MQTT_PORT

        # Controllers
        self.store_preprocess_controller = StorePreprocessController(
            self.db
        )
        self.publish_pending_controller = PublishPendingController(
            self.db, self.mqtt_client
        )
        self.handle_uploaded_controller = HandleUploadedController(self.db)

    def _parse_response(self, result: dict) -> dict:
        """Helper to log results in a consistent format."""
        if result["success"]:
            self.logger.info(result["message"])
        else:
            self.logger.error(
                f"{result['error_code']}: {result.get('message')} - {result.get('details', '')}"
            )
        return result

    async def configure(self) -> None:
        """Configure services (e.g. DB, MQTT connection, subscriptions)"""
        try:
            # Initialize database
            await self.db.create()
            self.logger.info("Database initialized")

            # Connect to MQTT broker
            await self.mqtt_client.start(host=self.mqtt_host, port=self.mqtt_port)
            self.logger.info("Connected to MQTT broker")

            # Subscribe to topics
            await self.mqtt_client.subscribe(
                topic=config.TOPIC_PREPROCESS, qos=config.TOPIC_PREPROCESS_QOS
            )
            self.logger.info(f"Subscribed to {config.TOPIC_PREPROCESS}")

            await self.mqtt_client.subscribe(
                topic=config.TOPIC_UPLOADED, qos=config.TOPIC_UPLOADED_QOS
            )
            self.logger.info(f"Subscribed to {config.TOPIC_UPLOADED}")
        except Exception as e:
            self.logger.error(f"Error during configuration: {e}")
            raise

    async def handle_message(self, topic: str, payload: str) -> dict:
        """Route incoming MQTT message to appropriate controller.
        This is the main entry point for message processing.
        """
        if topic == config.TOPIC_PREPROCESS:
            result = await self.store_preprocess_controller.handle(topic, payload)
        elif topic == config.TOPIC_UPLOADED:
            result = await self.handle_uploaded_controller.handle(topic, payload)
        else:
            self.logger.warning(f"Unknown topic received: {topic}")
            return {"success": False, "error": f"Unknown topic: {topic}"}
        return self._parse_response(result)

    async def publish_pending(self, target_topic: str) -> dict:
        """Publish pending messages from database.
        Call this periodically (e.g., every 30 seconds).
        """
        result = await self.publish_pending_controller.handle(target_topic)
        return self._parse_response(result)

    async def shutdown(self) -> None:
        """Gracefully shutdown all the services."""
        try:
            await self.mqtt_client.end_connection()
            await self.db.end_connection()
            self.logger.info("Data storage service stopped")
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
