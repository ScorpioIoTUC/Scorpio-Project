from .geospatial_client_contract import GeospatialClientContract
from .types import Geodetic2AerArgs
from .clients import Pymap3dClient


class GeospatialClient(GeospatialClientContract):
    CLIENTS = {"pymap3d"}

    def __init__(self, client_name: str = "pymap3d") -> None:
        if client_name not in GeospatialClient.CLIENTS:
            msg = f"Unsupported client {client_name}"
            raise KeyError(msg)
        if client_name == "pymap3d":
            self.client_obj = Pymap3dClient()
        self.client_name = client_name

    def get_elevation_angle(self, args: Geodetic2AerArgs) -> float:
        return self.client_obj.get_elevation_angle(args)

    def get_slant_range(self, args: Geodetic2AerArgs) -> float:
        return self.client_obj.get_slant_range(args)
