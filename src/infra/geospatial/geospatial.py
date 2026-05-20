from src.libs.geospatial_client import GeospatialClient, Geodetic2AerArgs


class Geospatial:
    def __init__(self, client_name: str = "pymap3d") -> None:
        self.client = GeospatialClient(client_name=client_name)

    def _build_args(
        self,
        target_latitude: float,
        target_longitude: float,
        target_altitude: float,
        observer_latitude: float,
        observer_longitude: float,
        observer_altitude: float,
        ell=None,
        deg: bool = True,
    ) -> Geodetic2AerArgs:
        return Geodetic2AerArgs(
            target_latitude=target_latitude,
            target_longitude=target_longitude,
            target_altitude=target_altitude,
            observer_latitude=observer_latitude,
            observer_longitude=observer_longitude,
            observer_altitude=observer_altitude,
            ell=ell,
            deg=deg,
        )

    def get_elevation_angle(
        self,
        target_latitude: float,
        target_longitude: float,
        target_altitude: float,
        observer_latitude: float,
        observer_longitude: float,
        observer_altitude: float,
        ell=None,
        deg: bool = True,
    ) -> float:
        args = self._build_args(
            target_latitude,
            target_longitude,
            target_altitude,
            observer_latitude,
            observer_longitude,
            observer_altitude,
            ell=ell,
            deg=deg,
        )
        return self.client.get_elevation_angle(args)

    def get_slant_range(
        self,
        target_latitude: float,
        target_longitude: float,
        target_altitude: float,
        observer_latitude: float,
        observer_longitude: float,
        observer_altitude: float,
        ell=None,
        deg: bool = True,
    ) -> float:
        args = self._build_args(
            target_latitude,
            target_longitude,
            target_altitude,
            observer_latitude,
            observer_longitude,
            observer_altitude,
            ell=ell,
            deg=deg,
        )
        return self.client.get_slant_range(args)
