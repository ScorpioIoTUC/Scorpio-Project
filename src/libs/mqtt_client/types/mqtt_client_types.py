from dataclasses import dataclass
from typing import Any


@dataclass
class MQTTClientInitArgs:
    """Initialization arguments for the MQTT client facade.

    Attributes:
            client_id: MQTT client identifier used by the broker.
            client_name: Concrete backend client implementation.
            clean_session: Whether a persistent session should be used.
            protocol: paho-mqtt protocol version integer.
            transport: Transport type, usually "tcp" or "websockets".
    """

    client_id: str
    client_name: str = "paho_client"
    clean_session: bool = True
    protocol: int = 4
    transport: str = "tcp"


@dataclass
class MQTTConnectArgs:
    """Connection settings for the MQTT broker.

    Attributes:
            host: Broker hostname or IP.
            port: Broker TCP port.
            keepalive: Keepalive timeout in seconds.
            bind_address: Optional local bind address.
            bind_port: Optional local bind port.
    """

    host: str = "mqtt"
    port: int = 1883
    keepalive: int = 60
    bind_address: str = ""
    bind_port: int = 0


@dataclass
class MQTTPublishArgs:
    """Publish arguments for a single MQTT message.

    Attributes:
            topic: Topic to publish to.
            payload: Message payload.
            qos: QoS level.
            retain: Retain flag.
            properties: Optional MQTT v5 properties.
    """

    topic: str
    payload: str | bytes | bytearray | None = None
    qos: int = 0
    retain: bool = False
    properties: Any = None


@dataclass
class MQTTSubscribeArgs:
    """Subscribe arguments for a topic.

    Attributes:
            topic: Topic filter to subscribe to.
            qos: Requested QoS level.
            options: Optional MQTT v5 subscribe options.
            properties: Optional MQTT v5 properties.
    """

    topic: str
    qos: int = 0
    options: Any = None
    properties: Any = None
