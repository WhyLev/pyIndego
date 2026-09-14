"""Predictive/SmartMowing setup model.

Mirrors the response of GET alms/{serial}/predictive/setup, previously
undocumented and unimplemented in pyIndego (consumers had to call the raw
``get()``/``put()`` endpoints themselves).
"""
from dataclasses import field
from typing import List

from .base import indego_dataclass
from .calendar import CalendarDay


@indego_dataclass
class GardenLocation:
    """Garden location as known to the predictive/SmartMowing feature."""

    latitude: float = None
    longitude: float = None
    timezone: str = None
    name: str = None
    country: str = None


@indego_dataclass
class PredictiveSetup:
    """SmartMowing configuration: garden size, mowing duration and weather sensitivity."""

    garden_size: int = None
    mowing_duration: int = None
    rain_factor: float = None
    temperature_factor: float = None
    garden_location: GardenLocation = field(default_factory=GardenLocation)
    full_cuts: int = None
    avoid_rain: bool = None
    avoid_temperature: bool = None
    use_grass_growth: bool = None
    no_mow_calendar_days: List[CalendarDay] = field(default_factory=list)
