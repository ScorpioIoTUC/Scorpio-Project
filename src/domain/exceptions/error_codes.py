from enum import Enum


class ErrorCode(Enum):
    DEC01 = ("DEC01", "LoRa decoding failed", 500)
    DB01 = ("DB01", "Database operation failed", 500)
    DB02 = ("DB02", "Database connection failed", 503)
    DB03 = ("DB03", "Database max error count exceeded", 500)
    VAL01 = ("VAL01", "Invalid topic received", 400)
    VAL02 = ("VAL02", "Invalid payload received", 400)
    PUB01 = ("PUB01", "MQTT publish failed", 500)
    PUB02 = ("PUB02", "Too many MQTT publish errors", 500)
    CS01 = ("CS01", "Could not send the payload to the cloud server", 500)
    PR01 = (
        "PR01",
        "The payload of the current satellite data packet cannot be preprocessed.",
        500,
    )
    PR02 = (
        "PR02",
        "The current payload could not be deserialized.",
        500,
    )

    UNKNOWN = ("UNKNOWN", "Unknown error", 500)

    def __init__(self, code: str, description: str, http_status: int):
        self.code = code
        self.description = description
        self.http_status = http_status
