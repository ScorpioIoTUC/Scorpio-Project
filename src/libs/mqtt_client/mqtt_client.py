from .client.paho_client import PahoClient
from .mqtt_client_contract import MQTTClientContract
from .types.mqtt_client_types import (
    MQTTClientInitArgs,
    MQTTConnectArgs,
    MQTTPublishArgs,
    MQTTSubscribeArgs,
)
from .utils import TopicValidator


class MQTTClient(MQTTClientContract):
    CLIENTS = {"paho_client"}

    def __init__(self, args: MQTTClientInitArgs) -> None:
        if args.client_name not in MQTTClient.CLIENTS:
            msg = f"Unsupported client {args.client_name}"
            raise KeyError(msg)
        if args.client_name == "paho_client":
            self.client_obj = PahoClient(args)
        self.client_name = args.client_name
        self._topic_validator = TopicValidator()

    async def connect(self, args: MQTTConnectArgs) -> None:
        return await self.client_obj.connect(args)

    async def close(self) -> None:
        return await self.client_obj.close()

    async def loop_start(self) -> None:
        return await self.client_obj.loop_start()

    async def loop_stop(self) -> None:
        return await self.client_obj.loop_stop()

    async def publish(self, args: MQTTPublishArgs) -> dict:
        self._topic_validator.validate(args.topic, "publish")
        return await self.client_obj.publish(args)

    async def subscribe(self, args: MQTTSubscribeArgs) -> dict:
        self._topic_validator.validate(args.topic, "subscribe")
        return await self.client_obj.subscribe(args)

    async def unsubscribe(self, topic: str) -> dict:
        return await self.client_obj.unsubscribe(topic)

    async def start(self, connect_args: MQTTConnectArgs) -> None:
        return await self.client_obj.start(connect_args)

    async def end_connection(self) -> None:
        return await self.client_obj.end_connection()
