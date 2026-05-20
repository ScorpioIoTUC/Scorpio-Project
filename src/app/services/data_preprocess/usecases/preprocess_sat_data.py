from src.infra import MQTT, Geospatial
from src.domain.exceptions.app_error import AppError
from src.app.services.data_preprocess.types import (
    SatelliteAdapter,
    StarlinkAdapter,
)
import json


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
        self.adapters: list[SatelliteAdapter] = [
            StarlinkAdapter(),
        ]

    def _find_adapter(self, data: dict) -> SatelliteAdapter:
        """Auto-detects the appropriate satellite adapter based on payload structure"""
        for adapter in self.adapters:
            if adapter.can_adapt(data):
                return adapter
        raise AppError.unidentified_satellite("No matching adapter found")

    def _preprocess_payload(self, payload: str) -> dict:
        data = json.loads(payload)
        adapter = self._find_adapter(data)
        return adapter.adapt(data)

    def _add_derived_metrics(self, data: dict) -> dict:
        lat = data.get("latitude")
        lon = data.get("longitude")
        alt = data.get("altitude")
        if any(v is None for v in [lat, lon, alt]):
            return data
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
        return {**data, "elevation_angle": elevation_angle, "slant_range": slant_range}

    async def execute(self, payload: str) -> dict:
        try:
            # Extract main attributes
            data = self._add_derived_metrics(self._preprocess_payload(payload))
            crc = data.get("crc", None)
            # Publish preprocessed data
            await self.mqtt_client.publish(
                topic=self.topic_to_publish, payload=json.dumps(data)
            )
            return {"success": True, "crc": crc}
        except json.JSONDecodeError as e:
            raise AppError.deserialization_error(f"Invalid JSON payload: {e}")
        except Exception as e:
            raise AppError.unknown_error(
                f"An unexpected error occurred during preprocessing: {e}"
            )
