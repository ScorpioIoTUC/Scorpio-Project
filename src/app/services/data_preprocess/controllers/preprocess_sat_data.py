from src.domain.exceptions.app_error import AppError
from src.infra import Logging, MQTT, Geospatial
import configs.entrypoints.data_preprocess as config
from src.app.services.data_preprocess.usecases.preprocess_sat_data import (
    PreprocessSatDataUseCase,
)


class PreprocessSatDataController:
    def __init__(self, mqtt_client: MQTT) -> None:
        self.logger = Logging("preprocess_sat_data")
        self.station_location = {
            "longitude": config.STATION_LON,
            "latitude": config.STATION_LAT,
            "altitude": config.STATION_ALT,
        }
        self.geospatial_client = Geospatial()
        self.use_case = PreprocessSatDataUseCase(
            mqtt_client,
            geospatial_client=self.geospatial_client,
            topic_to_publish=config.MQTT_PUB_TOPIC_1,
            station_location=self.station_location,
        )

    async def handle(self, payload: str) -> dict:
        self.logger.info(f"Preprocessing message from '{config.MQTT_SUB_TOPIC_1}'")
        try:
            result = await self.use_case.execute(payload)
            crc = result.get("crc", None)
            if crc is not None and not crc:
                self.logger.warning("CRC check failed for received data")
            elif crc is not None and crc:
                self.logger.info("CRC OK and data preprocessed successfully")
            return result
        except AppError as e:
            return {"success": False, **e.to_dict()}
