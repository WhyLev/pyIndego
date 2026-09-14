"""Models describing the mower itself: identity, battery, garden and state."""
from dataclasses import field
from datetime import datetime
from typing import Dict

from ..const import DEFAULT_LOOKUP_VALUE, MOWER_MODEL_DESCRIPTION, MOWING_MODE_DESCRIPTION
from ..helpers import convert_bosch_datetime
from .base import indego_dataclass


@indego_dataclass
class ModelVoltage:
    """Min/max battery voltage for a given mower model, used to compute an adjusted percentage."""

    min: int = None
    max: int = None


MOWER_MODEL_VOLTAGE: Dict[str, ModelVoltage] = {
    "3600HA2300": ModelVoltage(min=285, max=369),  # Indego 1000
    "3600HA2301": ModelVoltage(min=285, max=369),  # Indego 1200
    "3600HA2302": ModelVoltage(min=285, max=369),  # Indego 1100
    "3600HA2303": ModelVoltage(min=285, max=369),  # Indego 13C
    "3600HA2304": ModelVoltage(min=285, max=369),  # Indego 10C
    "3600HB0100": ModelVoltage(min=0, max=100),  # Indego 350
    "3600HB0101": ModelVoltage(min=0, max=100),  # Indego 400
    "3600HB0102": ModelVoltage(min=0, max=100),  # Indego S+ 350 1gen
    "3600HB0103": ModelVoltage(min=0, max=100),  # Indego S+ 400 1gen
    "3600HB0105": ModelVoltage(min=0, max=100),  # Indego S+ 350 2gen
    "3600HB0106": ModelVoltage(min=0, max=100),  # Indego S+ 400 2gen
    "3600HB0302": ModelVoltage(min=0, max=100),  # Indego S+ 500
    "3600HB0301": ModelVoltage(min=0, max=100),  # Indego M+ 700 1gen
    "3600HB0303": ModelVoltage(min=0, max=100),  # Indego M+ 700 gen2
}


@indego_dataclass
class Battery:
    """Battery status."""

    percent: int = None
    voltage: float = None
    cycles: int = None
    discharge: float = None
    ambient_temp: int = None
    battery_temp: int = None
    percent_adjusted: int = None

    def update_percent_adjusted(self, voltage: ModelVoltage):
        """Set percent_adjusted, the model-voltage-adjusted battery percentage."""
        if self.percent:
            self.percent_adjusted = round(
                (int(self.percent) - voltage.min) / ((voltage.max - voltage.min) / 100)
            )


@indego_dataclass
class Garden:
    """Garden/lawn statistics as tracked by the mower."""

    id: int = None
    name: int = None
    signal_id: int = None
    size: int = None
    inner_bounds: int = None
    cuts: int = None
    runtime: int = None
    charge: int = None
    bumps: int = None
    stops: int = None
    last_mow: int = None
    map_cell_size: int = None


@indego_dataclass
class RuntimeDetail:
    """Operate/charge/cut minutes for either a session or a lifetime total."""

    operate: int = None
    charge: int = None
    cut: int = field(init=False, default=None)

    def update_cut(self):
        """Compute cut (mowing) time as operate time minus charge time."""
        self.cut = round(self.operate - self.charge)


@indego_dataclass
class Runtime:  # pylint: disable=no-member,assigning-non-slot
    """Session and lifetime-total runtime."""

    total: RuntimeDetail = field(default_factory=RuntimeDetail)
    session: RuntimeDetail = field(default_factory=RuntimeDetail)

    def __post_init__(self):
        """Normalize totals (Bosch reports them in centiseconds-ish units) and compute cut times."""
        if self.total.charge:
            self.total.charge = round(self.total.charge / 100)
        if self.total.operate:
            self.total.operate = round(self.total.operate / 100)
        if self.total.charge:
            self.total.update_cut()
        if self.session.charge:
            self.session.update_cut()
        else:
            self.session.cut = 0


@indego_dataclass
class GenericData:
    """Mower identity: name, serial, firmware, model and mowing mode."""

    alm_name: str = None
    alm_sn: str = None
    service_counter: int = None
    needs_service: bool = None
    alm_mode: str = None
    bareToolnumber: str = None
    alm_firmware_version: str = None
    model_description: str = None
    model_voltage: ModelVoltage = field(default_factory=ModelVoltage)
    mowing_mode_description: str = None
    renew_date: datetime = None

    def __post_init__(self):
        """Set model description, voltage limits and mowing-mode description."""
        self.model_description = MOWER_MODEL_DESCRIPTION.get(
            self.bareToolnumber, DEFAULT_LOOKUP_VALUE
        )
        self.model_voltage = MOWER_MODEL_VOLTAGE.get(
            self.bareToolnumber, ModelVoltage()
        )
        self.mowing_mode_description = MOWING_MODE_DESCRIPTION.get(
            self.alm_mode, DEFAULT_LOOKUP_VALUE
        )
        self.renew_date = convert_bosch_datetime(self.renew_date)


@indego_dataclass
class OperatingData:
    """Battery, garden and runtime data as of the last state refresh."""

    hmiKeys: str = None
    battery: Battery = field(default_factory=Battery)
    garden: Garden = field(default_factory=Garden)
    runtime: Runtime = field(default_factory=Runtime)


@indego_dataclass
class State:
    """Current mower state: status code, position, progress and runtime."""

    state: int = None
    map_update_available: bool = None
    mowed: int = None
    mowmode: int = None
    error: int = None
    xPos: int = None
    yPos: int = None
    charge: int = None
    operate: int = None
    runtime: Runtime = field(default_factory=Runtime)
    mapsvgcache_ts: int = None
    svg_xPos: int = None
    svg_yPos: int = None
    config_change: bool = None
    mow_trig: bool = None
    enabled: bool = None
