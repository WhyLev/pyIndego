"""Location and mobile-network models."""
from typing import List

from .base import indego_dataclass


@indego_dataclass
class Location:
    """Garden GPS location."""

    latitude: float = None
    longitude: float = None
    timezone: str = None


@indego_dataclass
class Network:
    """Mobile network the mower is connected through."""

    mcc: int = None
    mnc: int = None
    rssi: int = None
    currMode: str = None
    configMode: str = None
    steeredRssi: int = None
    networkCount: int = None
    networks: List[int] = None
