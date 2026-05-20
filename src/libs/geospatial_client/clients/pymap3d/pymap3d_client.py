from pymap3d import geodetic2aer

from ...geospatial_client_contract import GeospatialClientContract
from ...types import Geodetic2AerArgs


class Pymap3dClient(GeospatialClientContract):
    def _get_aer(self, args: Geodetic2AerArgs) -> tuple[float, float, float]:
        return geodetic2aer(
            args.target_latitude,
            args.target_longitude,
            args.target_altitude,
            args.observer_latitude,
            args.observer_longitude,
            args.observer_altitude,
            ell=args.ell,
            deg=args.deg,
        )

    def get_elevation_angle(self, args: Geodetic2AerArgs) -> float:
        _, elevation_angle, _ = self._get_aer(args)
        return elevation_angle

    def get_slant_range(self, args: Geodetic2AerArgs) -> float:
        _, _, slant_range = self._get_aer(args)
        return slant_range
