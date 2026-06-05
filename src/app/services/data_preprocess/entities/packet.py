from dataclasses import dataclass

@dataclass
class Packet:
    noradId: int | None
    latitude: float | None
    longitude: float | None
    altitude: float | None
    rssi: float | None
    snr: float | None
    frequencyError: float | None
    crc: bool | None
    rawPayload: str | None
    slantDistance: float | None = 0.0
    elevationAngle: float | int | None = 0.0
