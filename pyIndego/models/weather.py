"""Predictive/SmartMowing weather forecast model.

Mirrors the response of GET alms/{serial}/predictive/weather (top-level key
``LocationWeather``), previously undocumented and unimplemented in pyIndego.
"""
from dataclasses import field
from typing import List

from .base import indego_dataclass


@indego_dataclass
class WeatherLocation:
    """Location the forecast applies to."""

    name: str = None
    country: str = None


@indego_dataclass
class WeatherInterval:
    """A single forecast interval."""

    dateTime: str = None
    intervalLength: int = None
    tt: float = None
    wwsymbol_mg2008: int = None
    prrr: float = None
    rrr: float = None


@indego_dataclass
class WeatherForecast:
    """A series of forecast intervals."""

    intervals: List[WeatherInterval] = field(default_factory=list)


@indego_dataclass
class Weather:
    """Weather forecast for the garden location, used by SmartMowing."""

    location: WeatherLocation = field(default_factory=WeatherLocation)
    forecast: WeatherForecast = field(default_factory=WeatherForecast)
