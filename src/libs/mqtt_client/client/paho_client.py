import asyncio
from typing import Any, Callable, Optional

import paho.mqtt.client as mqtt

from src.libs.mqtt_client.mqtt_client_contract import MQTTClientContract
from src.libs.mqtt_client.types.mqtt_client_types import (
    MQTTClientInitArgs,
    MQTTConnectArgs,
    MQTTPublishArgs,
    MQTTSubscribeArgs,
)


class PahoClient(MQTTClientContract):
    def __init__(self, args: MQTTClientInitArgs) -> None:
        self._client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION1,  # type: ignore
            client_id=args.client_id,
            clean_session=args.clean_session,
            protocol=args.protocol,  # type: ignore
            transport=args.transport,  # type: ignore
        )
        self._message_callback: Optional[Callable[[str, str], None]] = None

    @property
    def client(self) -> mqtt.Client:
        return self._client

    async def connect(self, args: MQTTConnectArgs) -> None:
        await asyncio.to_thread(
            self._client.connect,
            args.host,
            args.port,
            args.keepalive,
            args.bind_address,
            args.bind_port,
        )

    async def close(self) -> None:
        await asyncio.to_thread(self._client.disconnect)

    async def loop_start(self) -> None:
        await asyncio.to_thread(self._client.loop_start)

    async def loop_stop(self) -> None:
        await asyncio.to_thread(self._client.loop_stop)

    async def publish(self, args: MQTTPublishArgs) -> dict[str, Any]:
        msg_info = await asyncio.to_thread(
            self._client.publish,
            args.topic,
            args.payload,
            args.qos,
            args.retain,
            args.properties,
        )
        return {"rc": msg_info.rc, "mid": msg_info.mid}

    async def subscribe(self, args: MQTTSubscribeArgs) -> dict[str, Any]:
        result, mid = await asyncio.to_thread(
            self._client.subscribe,
            args.topic,
            args.qos,
            args.options,
            args.properties,
        )
        return {"result": result, "mid": mid}

    async def unsubscribe(self, topic: str) -> dict[str, Any]:
        result, mid = await asyncio.to_thread(self._client.unsubscribe, topic)
        return {"result": result, "mid": mid}

    async def start(self, connect_args: MQTTConnectArgs) -> None:
        await self.connect(connect_args)
        await self.loop_start()

    async def end_connection(self) -> None:
        await self.loop_stop()
        await self.close()

    def set_message_callback(self, callback: Callable[[str, str], None]) -> None:
        """Register a callback function to handle incoming MQTT messages.
        
        Args:
            callback: Function that accepts (topic: str, payload: str) parameters
        """
        self._message_callback = callback
        
        def on_message_wrapper(client, userdata, msg):
            """Internal wrapper for paho's message callback."""
            try:
                payload = msg.payload.decode('utf-8') if isinstance(msg.payload, bytes) else msg.payload
                if self._message_callback:
                    self._message_callback(msg.topic, payload)
            except Exception as e:
                print(f"Error in MQTT message callback: {e}")
        
        self._client.on_message = on_message_wrapper
