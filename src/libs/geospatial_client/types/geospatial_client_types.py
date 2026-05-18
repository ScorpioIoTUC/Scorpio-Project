from dataclasses import dataclass
from typing import Any


@dataclass
class Geodetic2AerArgs:
    target_latitude: float
    target_longitude: float
    target_altitude: float
    observer_latitude: float
    observer_longitude: float
    observer_altitude: float
    ell: Any = None
    deg: bool = True
