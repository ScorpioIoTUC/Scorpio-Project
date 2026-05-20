from abc import ABC, abstractmethod

from .types import Geodetic2AerArgs


class GeospatialClientContract(ABC):
    @abstractmethod
    def get_elevation_angle(self, args: Geodetic2AerArgs) -> float:
        pass

    @abstractmethod
    def get_slant_range(self, args: Geodetic2AerArgs) -> float:
        pass
