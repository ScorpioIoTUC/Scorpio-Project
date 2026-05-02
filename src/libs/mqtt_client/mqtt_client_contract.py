from abc import ABC, abstractmethod

from typing import Callable
from .types.mqtt_client_types import MQTTConnectArgs, MQTTPublishArgs, MQTTSubscribeArgs


class MQTTClientContract(ABC):
    @abstractmethod
    async def connect(self, args: MQTTConnectArgs) -> None:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

    @abstractmethod
    async def loop_start(self) -> None:
        pass

    @abstractmethod
    async def loop_stop(self) -> None:
        pass

    @abstractmethod
    async def publish(self, args: MQTTPublishArgs) -> dict:
        """Publish a message to a topic."""
        pass

    @abstractmethod
    async def subscribe(self, args: MQTTSubscribeArgs) -> dict:
        """Subscribe to a topic."""
        pass

    @abstractmethod
    async def unsubscribe(self, topic: str) -> dict:
        """Unsubscribe from a topic."""
        pass

    @abstractmethod
    async def start(self, connect_args: MQTTConnectArgs) -> None:
        """Method to connect and start the MQTT client loop."""

        pass

    @abstractmethod
    async def end_connection(self) -> None:
        """Method to stop the MQTT client loop and disconnect."""
        pass

    @abstractmethod
    def set_message_callback(self, callback: Callable[[str, str], None]) -> None:
        """Register a callback function to handle incoming MQTT messages."""
        pass
