"""Alert model."""
from dataclasses import field
from datetime import datetime

from ..const import ALERT_ERROR_CODE, DEFAULT_LOOKUP_VALUE
from ..helpers import convert_bosch_datetime
from .base import indego_dataclass


@indego_dataclass
class Alert:
    """A single mower alert/notification."""

    alm_sn: str = field(repr=False, default=None)
    alert_id: str = None
    error_code: str = None
    headline: str = None
    date: datetime = None
    message: str = None
    read_status: str = None
    flag: str = None
    push: bool = None
    alert_description: str = None

    def __post_init__(self):
        """Set alert description and parse the date."""
        self.alert_description = ALERT_ERROR_CODE.get(
            self.error_code, DEFAULT_LOOKUP_VALUE
        )
        self.date = convert_bosch_datetime(self.date)
