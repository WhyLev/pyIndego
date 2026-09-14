"""Calendar and predictive-schedule models."""
from dataclasses import field
from datetime import date, datetime, time, timedelta
from typing import List

from ..const import DAY_MAPPING
from .base import indego_dataclass


@indego_dataclass
class CalendarSlot:
    """A single enabled/disabled time slot within a calendar day."""

    En: bool = None
    StHr: int = None
    StMin: int = None
    EnHr: int = None
    EnMin: int = None
    Attr: str = None
    start: time = None
    end: time = None
    dt: datetime = None

    def __post_init__(self):
        """Convert start and end into time objects."""
        if self.StHr is not None and self.StMin is not None:
            self.start = time(self.StHr, self.StMin)
        if self.EnHr is not None and self.EnMin is not None:
            self.end = time(self.EnHr, self.EnMin)


@indego_dataclass
class CalendarDay:
    """One day of a calendar, made up of (usually two) slots."""

    day: int = None
    day_name: str = None
    slots: List[CalendarSlot] = field(default_factory=list)

    def __post_init__(self):
        """Set the day name and compute the next occurrence datetime for enabled slots."""
        if self.day is not None:
            self.day_name = DAY_MAPPING[self.day]
        if self.slots:
            for slot in self.slots:
                if slot.En:
                    today = date.today().weekday()
                    date_offset = timedelta(
                        days=self.day - today, hours=slot.StHr, minutes=slot.StMin
                    )
                    new_dt = (
                        datetime.now().replace(
                            hour=0, minute=0, second=0, microsecond=0
                        )
                        + date_offset
                    )
                    if new_dt.date() < date.today():
                        new_dt = new_dt + timedelta(days=7)
                    slot.dt = new_dt


@indego_dataclass
class Calendar:
    """A full calendar (7 days) of mowing slots."""

    cal: int = None
    days: List[CalendarDay] = field(default_factory=list)


@indego_dataclass
class PredictiveSchedule:
    """SmartMowing's predicted mowing schedule and its exclusion windows."""

    schedule_days: List[CalendarDay] = field(default_factory=list)
    exclusion_days: List[CalendarDay] = field(default_factory=list)
