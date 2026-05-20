from src.libs.mqtt_client import (
    MQTTClient,
    MQTTClientInitArgs,
    MQTTConnectArgs,
    MQTTPublishArgs,
    MQTTSubscribeArgs,
)
from typing import Callable, Literal

CLIENT_NAME = "paho_client"


class MQTT:
    def __init__(
        self,
        client_id: str,
        clean_session: bool = True,
        protocol: int = 4,
        transport: Literal["tcp", "websockets", "unix"] = "tcp",
    ) -> None:
        self.client = MQTTClient(
            MQTTClientInitArgs(
                client_id=client_id,
                client_name=CLIENT_NAME,
                clean_session=clean_session,
                protocol=protocol,
                transport=transport,
            )
        )

    async def connect(
        self,
        host: str,
        port: int = 1883,
        keepalive: int = 60,
        bind_address: str = "",
        bind_port: int = 0,
    ) -> None:
        await self.client.connect(
            MQTTConnectArgs(
                host=host,
                port=port,
                keepalive=keepalive,
                bind_address=bind_address,
                bind_port=bind_port,
            )
        )

    async def close(self) -> None:
        await self.client.close()

    async def loop_start(self) -> None:
        await self.client.loop_start()

    async def loop_stop(self) -> None:
        await self.client.loop_stop()

    async def publish(
        self,
        topic: str,
        payload: str | bytes | bytearray | None = None,
        qos: int = 0,
        retain: bool = False,
    ) -> dict:
        return await self.client.publish(
            MQTTPublishArgs(topic=topic, payload=payload, qos=qos, retain=retain)
        )

    async def subscribe(self, topic: str, qos: int = 0) -> dict:
        return await self.client.subscribe(MQTTSubscribeArgs(topic=topic, qos=qos))

    async def unsubscribe(self, topic: str) -> dict:
        return await self.client.unsubscribe(topic)

    async def start(
        self,
        host: str,
        port: int = 1883,
        keepalive: int = 60,
        bind_address: str = "",
        bind_port: int = 0,
    ) -> None:
        return await self.client.start(
            MQTTConnectArgs(
                host=host,
                port=port,
                keepalive=keepalive,
                bind_address=bind_address,
                bind_port=bind_port,
            )
        )

    async def end_connection(self) -> None:
        return await self.client.end_connection()

    def set_message_callback(self, callback: Callable[[str, str], None]) -> None:
        """Register a callback function to handle incoming MQTT messages.
        
        Args:
            callback: Function that accepts (topic: str, payload: str) parameters
        """
        return self.client.set_message_callback(callback)
