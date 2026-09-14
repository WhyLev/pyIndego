"""Data models returned by the Bosch Indego API, as used by pyIndego."""
from .alert import Alert
from .automatic_update import AutomaticUpdate
from .base import generate_update, indego_dataclass, nested_dataclass
from .calendar import Calendar, CalendarDay, CalendarSlot, PredictiveSchedule
from .config import Config, Security, Setup
from .mower import (
    MOWER_MODEL_VOLTAGE,
    Battery,
    Garden,
    GenericData,
    ModelVoltage,
    OperatingData,
    Runtime,
    RuntimeDetail,
    State,
)
from .network import Location, Network
from .predictive_setup import GardenLocation, PredictiveSetup
from .user import User
from .weather import Weather, WeatherForecast, WeatherInterval, WeatherLocation

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
    "generate_update",
    "indego_dataclass",
    "nested_dataclass",
]
