from src.infra import MQTT, Geospatial
from src.domain.exceptions.app_error import AppError
from src.app.services.data_preprocess.entities.packet import Packet
import json
from dataclasses import asdict, replace


class PreprocessSatDataUseCase:
    def __init__(
        self,
        mqtt_client: MQTT,
        geospatial_client: Geospatial,
        topic_to_publish: str,
        station_location: dict,
    ) -> None:
        self.mqtt_client = mqtt_client
        self.geospatial_client = geospatial_client
        self.topic_to_publish = topic_to_publish
        self.station_location = station_location

    def _preprocess_payload(self, payload: str) -> Packet:
        data = json.loads(payload)
        packet = Packet(
            noradId=data.get("noradId"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            altitude=data.get("altitude"),
            rssi=data.get("rssi"),
            snr=data.get("snr"),
            frequencyError=data.get("frequencyError"),
            crc=data.get("crc"),
            rawPayload=json.dumps(data),
        )
        return packet

    def _add_derived_metrics(self, packet: Packet) -> Packet:
        lat = packet.latitude
        lon = packet.longitude
        alt = packet.altitude
        if any(v is None for v in [lat, lon, alt]):
            return packet
        args = {
            "target_latitude": lat,
            "target_longitude": lon,
            "target_altitude": alt,
            "observer_latitude": self.station_location["latitude"],
            "observer_longitude": self.station_location["longitude"],
            "observer_altitude": self.station_location["altitude"],
        }
        # Calculate elevation angle
        elevation_angle = self.geospatial_client.get_elevation_angle(**args)
        # Calculate slant range
        slant_range = self.geospatial_client.get_slant_range(**args)
        # Add metrics
        packet.elevationAngle = elevation_angle
        packet.slantDistance = slant_range

        return replace(
            packet,
            elevationAngle=elevation_angle,
            slantDistance=slant_range,
        )

    async def execute(self, payload: str) -> dict:
        try:
            # Extract main attributes
            packet = self._add_derived_metrics(self._preprocess_payload(payload))
            crc = packet.crc
            # Publish preprocessed data
            await self.mqtt_client.publish(
                topic=self.topic_to_publish, payload=json.dumps(asdict(packet))
            )
            return {"success": True, "crc": crc}
        except json.JSONDecodeError as e:
            raise AppError.deserialization_error(f"Invalid JSON payload: {e}")
        except Exception as e:
            raise AppError.unknown_error(
                f"An unexpected error occurred during preprocessing: {e}"
            )
