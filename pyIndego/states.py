"""Backward-compatible import path for pyIndego's data models.

As of the pyIndego.models rework, the model classes live in
``pyIndego.models`` (split by concern across several modules). This module
re-exports them all under their original ``pyIndego.states`` names/location
so existing ``from pyIndego.states import Alert`` style imports keep working
unchanged.
"""
from .models import (  # noqa: F401
    MOWER_MODEL_VOLTAGE,
    Alert,
    AutomaticUpdate,
    Battery,
    Calendar,
    CalendarDay,
    CalendarSlot,
    Config,
    Garden,
    GardenLocation,
    GenericData,
    Location,
    ModelVoltage,
    Network,
    OperatingData,
    PredictiveSchedule,
    PredictiveSetup,
    Runtime,
    RuntimeDetail,
    Security,
    Setup,
    State,
    User,
    Weather,
    WeatherForecast,
    WeatherInterval,
    WeatherLocation,
)

__all__ = [
    "Alert",
    "AutomaticUpdate",
    "Battery",
    "Calendar",
    "CalendarDay",
    "CalendarSlot",
    "Config",
    "Garden",
    "GardenLocation",
    "GenericData",
    "Location",
    "MOWER_MODEL_VOLTAGE",
    "ModelVoltage",
    "Network",
    "OperatingData",
    "PredictiveSchedule",
    "PredictiveSetup",
    "Runtime",
    "RuntimeDetail",
    "Security",
    "Setup",
    "State",
    "User",
    "Weather",
    "WeatherForecast",
    "WeatherInterval",
    "WeatherLocation",
]
