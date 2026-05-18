from abc import ABC, abstractmethod


class SatelliteAdapter(ABC):
    """Abstract base class for satellite data adapters"""

    @abstractmethod
    def can_adapt(self, data: dict) -> bool:
        """Check if this adapter can handle the given satellite data"""
        pass

    @abstractmethod
    def adapt(self, data: dict) -> dict:
        """Transform satellite-specific data to normalized format"""
        pass


class StarlinkAdapter(SatelliteAdapter):
    """Adapter for Starlink satellite data"""

    SATELLITE_ID_FIELD = "starlink_id"

    def can_adapt(self, data: dict) -> bool:
        return self.SATELLITE_ID_FIELD in data

    def adapt(self, data: dict) -> dict:
        return {
            "satellite_id": data.get(self.SATELLITE_ID_FIELD),
            "satellite_type": "starlink",
            "crc": data.get("crc_ok"),
            "latitude": data.get("lat"),
            "longitude": data.get("lon"),
            "altitude": data.get("alt"),
            "rssi": data.get("rssi"),
            "snr": data.get("snr"),
            "freq_error": data.get("freq_error"),
        }


# TODO: add more adapters with the same contract
